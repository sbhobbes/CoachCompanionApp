# Author: Seth Hobbes
# Created: 7/17/2021
# Copyright: Springboro Technologies, LLC DBA Monarch Technologies all rights reserved
# Last Modified: 7/17/2021

import sqlite3
from sqlite3 import Error
from random import randint

def CreateConnection(db_file):
    """ create a database connection to the SQLite database specificied by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        
    return conn

def UpdateSchedule(conn, schedule):
    """ update priority, begin_date, and end date of a task
    :param conn:
    :param schedule:
    """
    
    sql = ''' UPDATE schedule SET gameId = ? , playerId = ? , positionId = ? , inningNumber = ? WHERE id = ? '''
    
    cur = conn.cursor()
    cur.execute(sql, schedule)
    conn.commit()    

def main():
    database = r"C:\sqlite\db\t_ball_db.db"
    
    # create a database connection
    conn = CreateConnection(database)
    with conn:
        UpdateSchedule(conn, (randint(1,6), randint(1,8), randint(1,8), 1, 3))
        
if __name__ == '__main__':
    main()