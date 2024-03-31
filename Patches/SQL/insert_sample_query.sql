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

INSERT INTO error_log (user_id, error_type, message)
VALUES
    (1, 'Runtime Error', 'Division by zero'),
    (2, 'Syntax Error', 'Missing semicolon'),
    (3, 'Type Error', 'Unexpected type conversion');

INSERT INTO error_log (user_id, error_type, message)
VALUES
    (1, 'Runtime Error', 'Division by zero'),
    (2, 'Syntax Error', 'Missing semicolon'),
    (3, 'Type Error', 'Unexpected type conversion');
END;

