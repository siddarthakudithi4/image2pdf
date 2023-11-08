CREATE DATABASE final;


CREATE TABLE users (
id            INT NOT NULL AUTO_INCREMENT,
username      VARCHAR(20) NOT NULL,  
password      VARCHAR(20) NOT NULL,
PRIMARY KEY (username)
);


CREATE DATABASE test_py;


CREATE TABLE USER_2(
firstname   VARCHAR(40) NOT NULL,
lastname    VARCHAR(40) NOT NULL,
email       VARCHAR(40) NOT NULL,
age         INT NOT NULL,
PRIMARY KEY (age)
);
