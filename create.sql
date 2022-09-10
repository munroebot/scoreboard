DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS pins;

CREATE TABLE scores (
    team TEXT,
    label TEXT,
    score INTEGER,
    period TEXT
);

CREATE TABLE pins (
    pin TEXT
);

INSERT INTO scores(team, label, score, period) values ("us","VGK",0,"P1");
INSERT INTO scores(team, label, score, period) values ("them","THEM",0,"P1");
INSERT INTO pins(pin) values ("$2b$12$tZty30ClScRVHIqIGOIBnupMmgNyh9QDPrG5pW88mEG.MIUMIiSrK")
