DROP DATABASE IF EXISTS test_odin;
CREATE DATABASE test_odin WITH OWNER odin;
\c test_odin
BEGIN;

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL ,
  description TEXT NOT NULL
);

COMMIT;
