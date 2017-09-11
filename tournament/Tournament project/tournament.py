#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2



def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("update players set wins =0;")
    c.execute("update players set nummatch =0;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered.
     *This function should not use the Python len() function;
      it should have the database count the players."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) from players")
    rows = c.fetchall()
    for row in rows:
        return row[0]
    conn.close()



def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    conn = connect()
    c = conn.cursor()
    c.execute("insert into players (name, wins, nummatch) values (%s,0,0);",(name,))

    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    *Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select id, name, wins, nummatch from players;")
    standings = c.fetchall()
    return standings
    conn.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    *Stores the outcome of a single match between two players in the database.
     update players set wins =wins+1 where id=%s;
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("update players set wins =wins+1 where id=%s;",(winner,))
    c.execute("update players set nummatch = nummatch+1 where id = %s or id = %s;",(winner,loser,))
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    select id,name from players where wins >=1 limit 2
    select id,name from players where wins >=1 limit 2 offset 2;
    create view wins0 as select id,name from players where wins=0;
    select id,name
 select a.id, a.name, b.id, b.name from wins0 as a, wins0 as b where a.id < b.id;


    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select distinct on(a.id) a.id, a.name, b.id, b.name from players as a, players as b where a.wins=b.wins and a.id < b.id limit 4;")
    pairings = c.fetchall()
    return pairings
    conn.close()


#print countPlayers()



