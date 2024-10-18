CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    "key" VARCHAR(255) NOT NULL,
    encrypted_message TEXT NOT NULL
);