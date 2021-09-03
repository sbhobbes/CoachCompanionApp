# Author: Seth Hobbes
# Created: 7/17/2021
# Copyright: Springboro Technologies, LLC DBA Monarch Technologies all rights reserved
# Last Modified: 7/17/2021

import sqlite3
from sqlite3 import Error
from random import randint

def CreateConnection(db_file):
    """ create a database connection to the SQLite database specificed by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    
    conn = None
    
    try: 
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        
    return conn

def CreateSchedule(conn, schedule):
    """ Insert a new schedule into the schedule table
    :param conn: database connection
    :param schedule: tuple with the values for the record
    :return: schedule id
    """
    
    sql = ''' INSERT INTO schedule(gameId, playerId, positionId, inningNumber) VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, schedule)
    conn.commit()
    
    # return cur.lastrowid
    
def CreateGame(conn, game):
    """ Insert a new game into the games table
    :param conn: connection to the database
    :param game: tuple with the values for the record
    :return: game id
    """
    
    sql = ''' INSERT INTO games(id, date, vs, startTime, homeFlag) VALUES(?, ?, ?, ?, ?) '''
    
    cur = conn.cursor()
    cur.execute(sql, game)
    conn.commit()
    
    # return cur.lastrowid
    
def CreatePlayer(conn, player):
    """
    Insert a new player into the players table
    :param conn: connection to the database
    :param player:
    :return: player id
    """
    
    sql = ''' INSERT INTO players(firstName, lastName) VALUES(?, ?) '''
    
    cur = conn.cursor()
    cur.execute(sql, player)
    conn.commit()
    
    # return cur.lastrowid
    
def CreatePosition(conn, position):
    """
    Insert a new position into the positions table
    :param conn: connection to the database
    :param position:
    :return: position id
    """
    
    sql = ''' INSERT INTO positions(name, infieldFlag) VALUES(?, ?) '''
    
    cur = conn.cursor()
    cur.execute(sql, position)
    conn.commit()
    
    # return cur.lastrowid
    
def CreatePositionCounter(conn, counter):
    """
    INSERT a new record into the positionCounters table
    :param conn: connection to the database
    :param counter:
    :return: counter id
    """
    
    sql = ''' INSERT INTO positionCounters(playerId, firstBaseCounter, firstBaseLastGame, firstBaseLastInning, secondBaseCounter,
                secondBaseLastGame, secondBaseLastInning, thirdBaseCounter, thirdBaseLastGame, thirdBaseLastInning, shortStopCounter,
                shortStopLastGame, shortStopLastInning, pitcherCounter, pitcherLastGame, pitcherLastInning, rightFieldCounter,
                rightFieldLastGame, rightFieldLastInning, leftFieldCounter, leftFieldLastGame, leftFieldLastInning, centerFieldCounter,
                centerFieldLastGame, centerFieldLastInning, homeRunCounter, homeRunLastGame, homeRunLastInning)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?, ?, ?, ?, ?) ''' 
    
    cur = conn.cursor()
    conn.execute(sql, counter)
    conn.commit()
    
    # return cur.lastrowid

def CreateTempCounter(conn, counter):
    """
    INSERT a new record into the positionCounters table
    :param conn: connection to the database
    :param counter:
    :return: counter id
    """
    
    sql = ''' INSERT INTO tempCounters(playerId, firstBaseCounter, firstBaseLastGame, firstBaseLastInning, secondBaseCounter,
                secondBaseLastGame, secondBaseLastInning, thirdBaseCounter, thirdBaseLastGame, thirdBaseLastInning, shortStopCounter,
                shortStopLastGame, shortStopLastInning, pitcherCounter, pitcherLastGame, pitcherLastInning, rightFieldCounter,
                rightFieldLastGame, rightFieldLastInning, leftFieldCounter, leftFieldLastGame, leftFieldLastInning, centerFieldCounter,
                centerFieldLastGame, centerFieldLastInning, homeRunCounter, homeRunLastGame, homeRunLastInning)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?, ?, ?, ?, ?) ''' 
    
    cur = conn.cursor()
    conn.execute(sql, counter)
    conn.commit()
    
    # return cur.lastrowid

#===============================================================================
# def create_task(conn, task):
#     """
#     Create a new task
#     :param conn:
#     :param task:
#     :return:
#     """
#     
#     sql = ''' INSERT INTO tasks(name,priority, status_id, project_id, begin_date, end_date) VALUES(?, ?, ?, ?, ?, ?) '''
#     cur = conn.cursor()
#     cur.execute(sql, task)
#     conn.commit()
#     
#     return cur.lastrowid
#===============================================================================

def main():
    database = r"C:\sqlite\db\t_ball_db.db"
    
    # create a database connection
    conn = CreateConnection(database)
    with conn:
        
        # Most of this code is commented out so as not to accidentally create new record if this script is executed
        
        # create a new project
        # schedule = (randint(1,6), randint(1,8), randint(1,8), 1);
        # CreateSchedule(conn, schedule)
        
        # create a new game
        # game = (6, "8/21/2021", "Deep Orange", "11:00", 1)
        # CreateGame(conn, game)
        
        # create a player
        # player = ("Cannon", "McDonald")
        # CreatePlayer(conn, player)
        
        # create a position
        # position = ("Center Field", 0)
        # CreatePosition(conn, position)
        
        # create positionCounter
        # counter = (8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        # CreatePositionCounter(conn, counter)
        
        # create tempCounter
        counter = (8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        CreateTempCounter(conn, counter)
        
if __name__ == '__main__':
    main()
    