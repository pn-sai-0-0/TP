CREATE DATABASE IF NOT EXISTS tree_portal;
USE tree_portal;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    name VARCHAR(100),
    mobile VARCHAR(15),
    address TEXT,
    password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS trees (
    tree_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tree_name VARCHAR(100),
    planted_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS growth (
    growth_id INT AUTO_INCREMENT PRIMARY KEY,
    tree_id INT,
    height FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    area_size FLOAT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tree_id) REFERENCES trees(tree_id)
);

CREATE TABLE IF NOT EXISTS location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    tree_id INT,
    latitude FLOAT,
    longitude FLOAT,
    address TEXT,
    area VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    pincode VARCHAR(10),
    FOREIGN KEY (tree_id) REFERENCES trees(tree_id)
);
