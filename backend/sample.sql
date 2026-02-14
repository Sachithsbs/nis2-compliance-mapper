CREATE TABLE users (
    id INT PRIMARY KEY,
    encrypted_password VARCHAR(255),
    mfa_enabled BOOLEAN,
    last_login_ip TEXT,
    failed_login_attempts INT
);
