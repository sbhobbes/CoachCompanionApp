# Author: Seth Hobbes
# Created: 7/17/2021
# Copyright: Springboro Technologies, LLC DBA Monarch Technologies all rights reserved
# Last Modified: 7/17/2021

import sqlite3
from sqlite3 import Error

def CreateConnection(db_file):
    """ Create a database connection to the SQLite database specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        
    return conn

def SelectAllPlayers(conn):
    """
    Query all rows in the players table
    :param conn: the Connection object
    :return:
    """
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM players")
    
    rows = cur.fetchall()
    
    for row in rows:
        print(row)
        
def SelectPlayerById(conn, id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM players WHERE id=?", (id,))
    
    rows = cur.fetchall()
    
    for row in rows:
        print(row)
        
def main():
    database = r"C:\sqlite\db\t_ball_db.db"
    
    # create a database conection
    conn = CreateConnection(database)
    
    with conn:
        print("1. Query player by id:")
        SelectPlayerById(conn, 3)
        
        print("2. Query all players")
        SelectAllPlayers(conn)

if __name__ == '__main__':
    main()