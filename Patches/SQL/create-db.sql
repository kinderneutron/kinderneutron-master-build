-- Create tables in a transaction

-- Check if the database exists
CREATE DATABASE kinderneutron_db ;

-- Connect to the new database
\c kinderneutron_db;
BEGIN;
-- Create the User table
CREATE TABLE IF NOT EXISTS "user" (
    id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Log table
CREATE TABLE IF NOT EXISTS error_log (
    id VARCHAR(255) PRIMARY KEY,
    user_id INT,
    error_type VARCHAR(255),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Device table
CREATE TABLE IF NOT EXISTS Device (
    id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255),
    device_name VARCHAR(255),
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Detection table
CREATE TABLE IF NOT EXISTS Detection (
    id VARCHAR(255) PRIMARY KEY,
    timestamp TIMESTAMP,
    result VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE public.user ADD COLUMN auth_token varchar(255);
END;
-- End the transaction
