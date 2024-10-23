COPY movies(id, title, genres)
FROM '/src/movies.csv'
DELIMITER ','
CSV HEADER;

COPY ratings(user_id, movie_id, rating, timestamp)
FROM '/src/ratings.csv'
DELIMITER ','
CSV HEADER;

COPY users(id, gender, age, occupation, zip_code)
FROM '/src/users.csv'
DELIMITER ','
CSV HEADER;
