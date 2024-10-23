from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json
import logging
import psycopg2

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

conn = psycopg2.connect(database = "postgres", 
                        user = "postgres", 
                        host= 'postgres',
                        password = "postgres",
                        port = 5432)


gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

def query_custom(query: str):
    cur = conn.cursor()
    cur.execute(query)
    res =  cur.fetchall()
    return res


def manhattan(rating1, rating2):
    distance = 0
    for i in rating1:
        for j in rating2:
            if i[0] == j[0]:
                distance += abs(i[1] - j[1])
    return distance


def computeNearestNeighbor(user_id, users):
    distances = []
    for user in users:
        if user != user_id:
            distance = manhattan(users[user], users[user_id])
            distances.append((distance, user))
    distances.sort()
    return distances


def recommend(user_id, users):
    """Give list of recommendations"""
    nearest = computeNearestNeighbor(user_id, users)[0][1]
    recommendations = []
    neighborRatings = users[nearest]
    userRatings = users[user_id]

    for i in neighborRatings:
        for j in userRatings:
            if i[0] == j[0]:
                recommendations.append((i[0], i[1]))

    return sorted(
        recommendations,
        key=lambda artistTuple: artistTuple[1],
        reverse = True
    )


@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        app.logger.info('Received vote for %s', vote)
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)
    

    arg_user_id = request.args.get('id')
    if arg_user_id is None:
        arg_user_id = 1
    
    data = {}
    users = [random.randrange(1, 6040) for _ in range(5)]
    users.insert(0, arg_user_id)

    print("usuarios a buscar:", users)

    for id in users:
        statement = f"SELECT movies.title, ratings.rating FROM ratings JOIN movies ON movies.id = ratings.movie_id WHERE ratings.user_id = {id}"
        ratings = query_custom(statement)
        data[id] = ratings

    list_recom = recommend(users[0], data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
        pelis=list_recom
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
