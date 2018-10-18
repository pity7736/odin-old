\set db_name `echo $DB_NAME`
\set db_user `echo $DB_USER`
DROP DATABASE IF EXISTS :db_name;
CREATE DATABASE :db_name WITH OWNER :db_user;
\c :db_name

BEGIN;

CREATE TABLE IF NOT EXISTS categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  description TEXT NOT NULL
);
CREATE INDEX categories_id_index ON categories(id);
CREATE INDEX categories_name_index ON categories(name);

CREATE TABLE IF NOT EXISTS subcategories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  category_id INTEGER REFERENCES categories ON DELETE CASCADE NOT NULL
);
CREATE INDEX subcategories_id_index ON subcategories(id);
CREATE INDEX subcategories_name_index ON subcategories(name);
CREATE INDEX subcategories_categoryid_index ON subcategories(category_id);

COMMIT;
