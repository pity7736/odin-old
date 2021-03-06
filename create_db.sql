\set db_name `echo $DB_NAME`
\set db_user `echo $DB_USER`
DROP DATABASE IF EXISTS :db_name;
CREATE DATABASE :db_name WITH OWNER :db_user;
\c :db_name

BEGIN;

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) UNIQUE NOT NULL,
  description TEXT NOT NULL
);
CREATE INDEX categories_name_index ON categories(name);

CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL
);
CREATE INDEX tags_name_index ON tags(name);

CREATE TABLE wallets (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  initial_balance NUMERIC(10, 2) NOT NULL,
  balance NUMERIC(10, 2) NOT NULL,
  created TIMESTAMP WITHOUT TIME ZONE NOT NULL
);
CREATE INDEX wallets_name_index ON wallets(name);

CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  init_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  end_date TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

CREATE TABLE movements (
  id SERIAL PRIMARY KEY,
  type VARCHAR(20) NOT NULL,
  category_id INTEGER REFERENCES categories NOT NULL,
  date DATE NOT NULL,
  value NUMERIC(10, 2) NOT NULL CONSTRAINT movements_value_check CHECK (value > 0),
  note TEXT,
  wallet_id INTEGER REFERENCES wallets NOT NULL,
  event_id INTEGER REFERENCES events
);
CREATE INDEX movements_type_index ON movements(type);
CREATE INDEX movements_category_index ON movements(category_id);
CREATE INDEX movements_date_index ON movements(date);

CREATE TABLE movements_tags (
  id SERIAL PRIMARY KEY,
  tag_id INTEGER REFERENCES tags NOT NULL,
  movement_id INTEGER REFERENCES movements NOT NULL
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(200) NOT NULL UNIQUE,
  password VARCHAR(150) NOT NULL,
  first_name VARCHAR(300) NULL,
  last_name VARCHAR(300) NULL,
  created TIMESTAMP WITHOUT TIME ZONE
);


COMMIT;
