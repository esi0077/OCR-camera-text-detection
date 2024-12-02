-- Create the database for user authentication
CREATE DATABASE IF NOT EXISTS user_auth;

-- Switch to the new database
USE user_auth;

-- Create a table for storing user credentials
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- Unique user ID
    username VARCHAR(50) NOT NULL UNIQUE,    -- Username (must be unique)
    password VARCHAR(100) NOT NULL           -- Hashed password
);

-- Add a salt column to the users table
ALTER TABLE users ADD COLUMN salt VARCHAR(64) AFTER password;
