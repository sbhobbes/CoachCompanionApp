# Author: Seth Hobbes
# Created: 7/17/2021
# Copyright: Springboro Technologies, LLC DBA Monarch Technologies all rights reserved
# Last Modified: 7/17/2021

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    
    # Call to the create connectio function passing the database path; if the filename does not
    # exist then the program automatically creates a new database with the specified file name
    create_connection(r"C:\sqlite\db\t_ball_db.db")
