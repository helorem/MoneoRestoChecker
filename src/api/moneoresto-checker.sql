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

CREATE TABLE update_time (
    balance DATE,
    histo DATE,
    request DATE
);

INSERT INTO user (username, password) VALUES ("admin", "9cf95dacd226dcf43da376cdb6cbba7035218921");
INSERT INTO update_time (balance, histo, request) VALUES (null, null, null);
