CREATE TABLE IF NOT EXISTS "users" (
  "id" SERIAL PRIMARY KEY,
  "username" VARCHAR(255) NOT NULL,
  "password" VARCHAR(255) NOT NULL,
  "email" VARCHAR(255) NOT NULL,
  "description" VARCHAR(255) NOT NULL
);

-- insert 100 random users
CREATE OR REPLACE FUNCTION insert_random_users()
RETURNS VOID AS $$
DECLARE
  i INT := 0;
BEGIN
  WHILE i < 10000 LOOP
    INSERT INTO users (username, password, email, description) VALUES (CONCAT('user', i::TEXT), 'password', CONCAT('user', i::TEXT, '@example.com'), 'description');
    i := i + 1;
  END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT insert_random_users();