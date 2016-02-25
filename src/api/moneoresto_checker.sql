CREATE TABLE transact (
	id INTEGER PRIMARY KEY,
	name TEXT,
	amount INTEGER,
	dt DATE
);

CREATE TABLE balance (
	id INTEGER PRIMARY KEY,
	amount INTEGER,
	validity DATE
);

CREATE TABLE user (
	id INTEGER PRIMARY KEY,
	username TEXT,
	password TEXT
);

INSERT INTO user (username, password) VALUES ("admin", "9cf95dacd226dcf43da376cdb6cbba7035218921");
