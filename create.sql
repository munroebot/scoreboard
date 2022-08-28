DROP TABLE IF EXISTS scores;

CREATE TABLE scores (
    team TEXT,
    label TEXT,
    score INTEGER,
    period TEXT
);

INSERT INTO scores(team, label, score, period) values ("us","VGK",0,"1");
INSERT INTO scores(team, label, score, period) values ("them","LVSTM",0,"1");
