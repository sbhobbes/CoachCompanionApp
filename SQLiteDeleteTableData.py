# Author: Seth Hobbes
# Created: 7/17/2021
# Copyright: Springboro Technologies, LLC DBA Monarch Technologies all rights reserved
# Last Modified: 7/17/2021

import sqlite3
from sqlite3 import Error

def CreateConnection(db_file):
    """ create a database connection to the SQLite database specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        
    return conn
    
def DeleteSchedule(conn, id):
    """ This function deletes individual records from the Schedule table
    :param conn: database connection object
    :param id: the ID of the record to delete
    """
    
    sql = 'DELETE FROM schedule WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    
def DeleteAllSchedules(conn):
    """ This function deletes all records from the Schedule table
    """
    
    sql = 'DELETE FROM schedule'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    
def main():
    """ Main code
    """
    
    # Create variable with path to the database
    database = r"C:\sqlite\db\t_ball_db.db"
    
    # create a database connection
    conn = CreateConnection(database)
    
    # Using the database connection, call the following functions; note that the ones
    # you do not want to run can be commented out
    with conn:
        # DeleteSchedule(conn, 2);
        DeleteAllSchedules(conn);
        
if __name__ == '__main__':
    main()