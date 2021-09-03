# Author: Seth Hobbes
# Created: 7/17/2021
# Copyright: Springboro Technologies, LLC DBA Monarch Technologies all rights reserved
# Last Modified: 7/17/2021

import sqlite3
from sqlite3 import Error

def CreateConnection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def CreateTable(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    """ Main program code holding the SQL scripts that generate the tables using the Create Table function
    """
    
    # Path to the database
    database = r"C:\sqlite\db\t_ball_db.db"

    # SQL to create a table called Games
    sql_create_games_table = """CREATE TABLE IF NOT EXISTS games (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                        date DATE NOT NULL,
                                        vs TEXT,
                                        startTime TIME,
                                        homeFlag BOOLEAN
                                    );"""

    # SQL to create a table called Players
    sql_create_players_table = """CREATE TABLE IF NOT EXISTS players (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    firstName TEXT,
                                    lastName TEXT,
                                    lastPositionId INTEGER REFERENCES positions (id)
                                );"""
    
    # SQL to create a table called Positions
    sql_create_positions_table = """CREATE TABLE IF NOT EXISTS positions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                    name TEXT NOT NULL UNIQUE,
                                    infieldFlag BOOLEAN
                                );"""
    
    # SQL to create a table called Schedule
    sql_create_schedule_table = """CREATE TABLE IF NOT EXISTS schedule (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                    gameId INTEGER REFERENCES games (id),
                                    playerId INTEGER REFERENCES players (id),
                                    positionId INTEGER REFERENCES positions (id),
                                    inningNumber INTEGER
                                );"""
                                
    # SQL to create a table called Innings
    sql_create_innings_table = """CREATE TABLE IF NOT EXISTS innings (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                    gameId INTEGER NOT NULL REFERENCES games (id),
                                    playerId INTEGER NOT NULL REFERENCES players(id),
                                    positionId INTEGER NOT NULL REFERENCES position (id),
                                    inningNumber INTEGER NOT NULL
                                );"""

    # SQL to create a table called Position Counters
    sql_create_positionCounters_table = """CREATE TABLE IF NOT EXISTS positionCounters (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                            playerId INTEGER NOT NULL REFERENCES players (id),
                                            firstBaseCounter INTEGER NOT NULL DEFAULT 0,
                                            firstBaseLastGame INTEGER NOT NULL DEFAULT 0,
                                            firstBaseLastInning INTEGER NOT NULL DEFAULT 0,
                                            secondBaseCounter INTEGER NOT NULL DEFAULT 0,
                                            secondBaseLastGame INTEGER NOT NULL DEFAULT 0,
                                            secondBaseLastInning INTEGER NOT NULL DEFAULT 0,
                                            thirdBaseCounter INTEGER NOT NULL DEFAULT 0,
                                            thirdBaseLastGame INTEGER NOT NULL DEFAULT 0,
                                            thirdBaseLastInning INTEGER NOT NULL DEFAULT 0,
                                            shortStopCounter INTEGER NOT NULL DEFAULT 0,
                                            shortStopLastGame INTEGER NOT NULL DEFAULT 0,
                                            shortStopLastInning INTEGER NOT NULL DEFAULT 0,
                                            pitcherCounter INTEGER NOT NULL DEFAULT 0,
                                            pitcherLastGame INTEGER NOT NULL DEFAULT 0,
                                            pitcherLastInning INTEGER NOT NULL DEFAULT 0,
                                            rightFieldCounter INTEGER NOT NULL DEFAULT 0,
                                            rightFieldLastGame INTEGER NOT NULL DEFAULT 0,
                                            rightFieldLastInning INTEGER NOT NULL DEFAULT 0,
                                            leftFieldCounter INTEGER NOT NULL DEFAULT 0,
                                            leftFieldLastGame INTEGER NOT NULL DEFAULT 0,
                                            leftFieldLastInning INTEGER NOT NULL DEFAULT 0,
                                            centerFieldCounter INTEGER NOT NULL DEFAULT 0,
                                            centerFieldLastGame INTEGER NOT NULL DEFAULT 0,
                                            centerFieldLastInning INTEGER NOT NULL DEFAULT 0,
                                            homeRunCounter INTEGER NOT NULL DEFAULT 0,
                                            homeRunLastGame INTEGER NOT NULL DEFAULT 0,
                                            homeRunLastInning INTEGER NOT NULL DEFAULT 0,
                                            lastInningOutfieldFlag BOOLEAN NOT NULL DEFAULT 0,
                                            lastPositionId INTEGER REFERENCES positions (id)
                                        );"""

    # SQL to create a table called Temp Counters
    sql_create_tempCounters_table = """CREATE TABLE IF NOT EXISTS tempCounters (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                            playerId INTEGER NOT NULL REFERENCES players (id),
                                            firstBaseCounter INTEGER NOT NULL DEFAULT 0,
                                            firstBaseLastGame INTEGER NOT NULL DEFAULT 0,
                                            firstBaseLastInning INTEGER NOT NULL DEFAULT 0,
                                            secondBaseCounter INTEGER NOT NULL DEFAULT 0,
                                            secondBaseLastGame INTEGER NOT NULL DEFAULT 0,
                                            secondBaseLastInning INTEGER NOT NULL DEFAULT 0,
                                            thirdBaseCounter INTEGER NOT NULL DEFAULT 0,
                                            thirdBaseLastGame INTEGER NOT NULL DEFAULT 0,
                                            thirdBaseLastInning INTEGER NOT NULL DEFAULT 0,
                                            shortStopCounter INTEGER NOT NULL DEFAULT 0,
                                            shortStopLastGame INTEGER NOT NULL DEFAULT 0,
                                            shortStopLastInning INTEGER NOT NULL DEFAULT 0,
                                            pitcherCounter INTEGER NOT NULL DEFAULT 0,
                                            pitcherLastGame INTEGER NOT NULL DEFAULT 0,
                                            pitcherLastInning INTEGER NOT NULL DEFAULT 0,
                                            rightFieldCounter INTEGER NOT NULL DEFAULT 0,
                                            rightFieldLastGame INTEGER NOT NULL DEFAULT 0,
                                            rightFieldLastInning INTEGER NOT NULL DEFAULT 0,
                                            leftFieldCounter INTEGER NOT NULL DEFAULT 0,
                                            leftFieldLastGame INTEGER NOT NULL DEFAULT 0,
                                            leftFieldLastInning INTEGER NOT NULL DEFAULT 0,
                                            centerFieldCounter INTEGER NOT NULL DEFAULT 0,
                                            centerFieldLastGame INTEGER NOT NULL DEFAULT 0,
                                            centerFieldLastInning INTEGER NOT NULL DEFAULT 0,
                                            homeRunCounter INTEGER NOT NULL DEFAULT 0,
                                            homeRunLastGame INTEGER NOT NULL DEFAULT 0,
                                            homeRunLastInning INTEGER NOT NULL DEFAULT 0
                                        );"""

    # create a database connection
    conn = CreateConnection(database)

    # If a connection exists, create the below tables
    if conn is not None:
        # create games table
        CreateTable(conn, sql_create_games_table)

        # create players table
        CreateTable(conn, sql_create_players_table)
        
        # create positions table
        CreateTable(conn, sql_create_positions_table)
        
        # create schedule table
        CreateTable(conn, sql_create_schedule_table)
        
        # create innings table
        CreateTable(conn, sql_create_innings_table)
        
        # create positionCounters table
        CreateTable(conn, sql_create_positionCounters_table)
        
        # create temp counters table
        CreateTable(conn, sql_create_tempCounters_table)
    
    # If no connection to database, print error message to the console
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
