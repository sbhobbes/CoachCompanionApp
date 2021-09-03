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


def CreateView(conn, create_view_sql):
    """ create a view from the create_view_sql statement
    :param conn: Connection object
    :param create_view_sql: a CREATE VIEW statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_view_sql)
    except Error as e:
        print(e)


def main():
    database = r"C:\sqlite\db\t_ball_db.db"

    # SQL to create a view called schedule view which will be used as the output
    # for game-time line-ups.
    sql_create_scheduleView_view = """CREATE VIEW scheduleView AS 
                                        SELECT
                                            schedule.id AS 'ID',
                                            games.date AS 'Date',
                                            schedule.inningNumber AS 'Inning',
                                            positions.name AS 'Position',
                                            players.firstName AS 'Player'
                                        FROM
                                            schedule
                                        INNER JOIN games ON games.id = schedule.gameId
                                        INNER JOIN positions ON positions.id = schedule.positionId
                                        INNER JOIN players ON players.id = schedule.playerId
                                    ;"""

    # create a database connection
    conn = CreateConnection(database)

    # create views
    if conn is not None:
        # create scheduleView view
        CreateView(conn, sql_create_scheduleView_view)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()