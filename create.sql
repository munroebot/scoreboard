DROP TABLE IF EXISTS scores;

CREATE TABLE scores (
    team TEXT,
    label TEXT,
    score INTEGER
);

INSERT INTO scores(team, label, score) values ("us","VGK",0);
INSERT INTO scores(team, label, score) values ("them","LVSTM",0);