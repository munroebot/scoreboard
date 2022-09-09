DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS pin;

CREATE TABLE scores (
    team TEXT,
    label TEXT,
    score INTEGER,
    period TEXT
);

CREATE TABLE pin (
    pin TEXT
);

INSERT INTO scores(team, label, score, period) values ("us","VGK",0,"P1");
INSERT INTO scores(team, label, score, period) values ("them","THEM",0,"P1");
