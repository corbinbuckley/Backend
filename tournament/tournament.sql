-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE DATABASE tournament;
\c tournament;
CREATE TABLE players (ID serial PRIMARY KEY, Name text);

CREATE TABLE matches (ID integer references players(ID), wins integer NOT NULL, nummatch integer NOT NULL)


