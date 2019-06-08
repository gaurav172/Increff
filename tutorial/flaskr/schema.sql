-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS meal;
DROP TABLE IF EXISTS sell;
DROP TABLE IF EXISTS buffetdishes;
DROP TABLE IF EXISTS dishhistory;
DROP TABLE IF EXISTS buffethistory;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  password TEXT NOT NULL,
  address TEXT NOT NULL,
  locality TEXT NOT NULL,
  ratingSum INTEGER,
  totRatings INTEGER,
  contact TEXT NOT NULL
  -- description TEXT NOT NULL
);

CREATE TABLE item (
  name TEXT NOT NULL,
  sellerUsername TEXT NOT NULL,
  price INTEGER,
  description TEXT,
  type TEXT,
  PRIMARY KEY(name,sellerusername)
);

CREATE TABLE sell (
  name TEXT NOT NULL,
  sellerUsername TEXT NOT NULL,
  price INTEGER ,
  qAvail INTEGER,
  readyTime TEXT,
  sellingTill TEXT,
  description TEXT,
  type TEXT,
  PRIMARY KEY(name,sellerusername)
);

CREATE TABLE meal (
  buffetNo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  inviterName TEXT NOT NULL,
  price INTEGER NOT NULL,
  startTime TEXT NOT NULL,
  endTime TEXT NOT NULL,
  seatAvail INTEGER NOT NULL,
  type TEXT NOT NULL
);

CREATE TABLE buffetdishes(
  buffetNo INTEGER NOT NULL,
  itemName TEXT NOT NULL,
  type TEXT NOT NULL,
  PRIMARY KEY(buffetno,itemname)
);

CREATE TABLE orderhistory(
  orderid INTEGER PRIMARY KEY AUTOINCREMENT,
  buyerName TEXT NOT NULL,
  sellerName TEXT NOT NULL,
  status TEXT NOT NULL,
  date TEXT NOT NULL,
  time TEXT NOT NULL
);

CREATE TABLE orderdish(
  orderid INTEGER NOT NULL,
  itemName TEXT NOT NULL
  qty INTEGER NOT NULL,
);

CREATE TABLE buffethistory(
  tid INTEGER PRIMARY KEY AUTOINCREMENT,
  invName TEXT NOT NULL,
  joName TEXT NOT NULL,
  total INTEGER NOT NULL,
  date TEXT NOT NULL,
  time TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
