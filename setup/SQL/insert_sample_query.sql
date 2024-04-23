BEGIN;
INSERT INTO "user" (username, email, password)
VALUES
    ('john_doe', 'john.doe@example.com', 'password123'),
    ('jane_smith', 'jane.smith@example.com', 'securepassword'),
    ('alice_wonderland', 'alice.wonderland@example.com', 'wonderland123');

INSERT INTO error_log (user_id, error_type, message)
VALUES
    (1, 'Runtime Error', 'Division by zero'),
    (2, 'Syntax Error', 'Missing semicolon'),
    (3, 'Type Error', 'Unexpected type conversion');
-- Insert a sample detection record
INSERT INTO Detection (timestamp, result)
VALUES ('2024-03-29 12:00:00', 'Suspicious activity detected');

-- Insert another sample detection record
INSERT INTO Detection (timestamp, result)
VALUES ('2024-03-30 10:30:00', 'Unauthorized access attempt detected');

-- Insert one more sample detection record
INSERT INTO Detection (timestamp, result)
VALUES ('2024-03-31 15:45:00', 'Malware detected in system');
-- Insert a sample device record
INSERT INTO Device (username, device_name, login_time)
VALUES ('john_doe', 'Laptop', '2024-03-29 08:00:00');

-- Insert another sample device record
INSERT INTO Device (username, device_name, login_time)
VALUES ('jane_smith', 'Smartphone', '2024-03-30 13:30:00');

-- Insert one more sample device record
INSERT INTO Device (username, device_name, login_time)
VALUES ('admin_user', 'Workstation', '2024-03-31 10:15:00');

END;

