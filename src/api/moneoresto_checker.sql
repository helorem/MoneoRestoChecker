CREATE TABLE transaction (
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


