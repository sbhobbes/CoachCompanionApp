# Author: Seth Hobbes
# Created: 7/17/2021
# Copyright: Springboro Technologies, LLC DBA Monarch Technologies all rights reserved
# Last Modified: 7/17/2021

import sqlite3
from sqlite3 import Error

def CreateConnection(db_file):
    """ Create a connection to the database 
    :param db_file: database file
    :return: connection object or None
    """
        
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        
    return conn

def CopyTable(conn, tableName):
    """ This function makes a copy of the postionCounters table as a new table
    :param conn: database connection object
    :param tableName: name of the table to create
    """
    
    # SQL statement to copy the table
    sql = ("""CREATE TABLE IF NOT EXISTS %s AS SELECT * FROM positionCounters""" %(tableName))
    
    # Cursor object
    cur = conn.cursor()
    
    # Execute the query
    cur.execute(sql)    
    
def main():
    """ Main function for the module
    """
    
    # Path to the database
    database = r"C:\sqlite\db\t_ball_db.db"
    
    # Call to the create connection function which passes the database path and creates a connection object
    conn = CreateConnection(database)
    
    # Call to the copy table function passing the database connection and the name of the new table
    CopyTable(conn, "tempCounters")
    

if __name__ == '__main__':
    main()