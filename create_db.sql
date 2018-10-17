\set db_name `echo $DB_NAME`
\set db_user `echo $DB_USER`
DROP DATABASE IF EXISTS :db_name;
CREATE DATABASE :db_name WITH OWNER :db_user;
\c :db_name

BEGIN;

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL ,
  description TEXT NOT NULL
);
CREATE INDEX categories_id_index ON categories(id);
CREATE INDEX categories_name_index ON categories(name);

COMMIT;
