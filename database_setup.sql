-- Create the database
CREATE DATABASE IF NOT EXISTS eco_app;
USE eco_app;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create activities table
CREATE TABLE IF NOT EXISTS activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    caption VARCHAR(500),
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create index on user_id for faster queries
CREATE INDEX idx_user_id ON activities(user_id);

-- Insert test user (password is "password123" hashed with werkzeug)
INSERT INTO users (username, password) VALUES 
('testuser', 'scrypt:32768:8:1$Bwc1jCEgKdAJjqZY$d75a0d41e5efd3ffa2ad1d7a7eea53c0c11e8e8c88d881e2ac5d9c7c5e8d8e7c');
