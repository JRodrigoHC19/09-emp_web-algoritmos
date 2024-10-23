CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genres VARCHAR(255)
);

CREATE TABLE ratings (
    user_id INT,
    movie_id INT,
    rating DECIMAL(2, 1) NOT NULL,
    timestamp BIGINT NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    gender CHAR(1),
    age INT,
    occupation VARCHAR(255),
    zip_code VARCHAR(10)
);