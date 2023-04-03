CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123'; -- password Auth123
CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON  auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('georgio@email.com', 'Admin123');

-- to source this script type mysql -uroot < init.sql
-- mysql -uroot -e "DROP DATABASE auth; DROP USER auth_user@localhost"
-- inside the database: show databases; use auth; show tables; describe user; select * from user;