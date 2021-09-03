# Author: Seth Hobbes
# Created: 7/17/2021
# Copyright: Springboro Technologies, LLC DBA Monarch Technologies all rights reserved
# Last Modified: 8/28/2021

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

def FindNextPlayerForPosition(conn, column1, column2, column3, playerIdList, positionId):
    """ This function takes a list of column names, a list of player IDs, and a position ID and uses
    them to query the database to determine which player from the list should play that position the next inning
    (Note that the inning is defined outside of this function)
    :param conn: database connection object
    :param column1: the first column name for dynamic querying
    :param column2: the second column name for dynamic querying
    :param column3: the third column name for dynamic querying
    :param playerIdList: a list of players for dynamic querying
    :param positionId: the position ID for dynamic querying
    """

    # Create the cursor object for navigating the database
    cur = conn.cursor()
    
    # Instantiate player value to 0; this prevents player from being empty if one is not found in the queries
    player = 0
    
    # error handling
    try:
        
        # The first series of queries below in the conditional statements create temp tables based on a process of elimination
        # to determine which players are eligible to play a given position in the current inning.  The queries executed 
        # after the conditional statements create additional tables to further break down the list of eligible players
        # based on (1) the number of times a player has played a given position, (2) the most recent game they played at
        # that position, and (3) the most recent inning they played that position. 
        
        # Instantiate a tuple and fill it with the list of players; tuple is required for the IN{} clause in the SQL statements
        playerIdTuple = tuple(playerIdList)        
        
        # If more than one player is in the list, then use IN{} clause in the query 
        if len(playerIdList) > 1:
            cur.execute( """CREATE TABLE schedule0_1 AS SELECT * FROM tempCounters WHERE lastPositionId != ?""", (positionId,))
            cur.execute( """CREATE TABLE schedule1 AS SELECT * FROM schedule0_1 WHERE playerId IN {}""".format(playerIdTuple))
            
        # If only one player is in the list, then use an equality operator in the query
        else:
            cur.execute( """CREATE TABLE schedule0_1 AS SELECT * FROM tempCounters WHERE lastPositionId != ?""", (positionId,))
            cur.execute( """CREATE TABLE schedule1 AS SELECT * FROM schedule0_1 WHERE playerId = ?""", (playerIdList))
        
        # If the position ID references an outfield position, then assess whether the players played outfield the previous
        # inning or not; if they played outfield in the previous inning, then they should not have to play outfield
        # again in the current inning
        if positionId > 5:
            cur.execute("""CREATE TABLE schedule1_1 AS SELECT playerId, %s, %s, %s, lastInningOutfieldFlag 
                        FROM schedule1 WHERE lastInningOutfieldFlag == 0""" % (column1, column2, column3))
            cur.execute( """CREATE TABLE schedule2 AS SELECT * FROM schedule1_1 WHERE %s = (SELECT min(%s) FROM schedule1_1)""" 
                         % (column1, column1))
        
        # If the current position is infield, then there's no need to check if the players were in the outfield
        # the previous inning or not.
        else:
            cur.execute( """CREATE TABLE schedule2 AS SELECT * FROM schedule1 WHERE %s = 
                        (SELECT min(%s) FROM schedule1)""" % (column1, column1))
    
        # Evaluate most recent game played at a given position
        cur.execute( """CREATE TABLE schedule3 AS SELECT * FROM schedule2 WHERE %s = (
                    SELECT min(%s) FROM schedule2)""" % (column2, column2))
    
        # Evaluate most recent inning played at a given position
        cur.execute( """CREATE TABLE schedule4 AS SELECT * FROM schedule3 WHERE %s = (
                    SELECT min(%s) FROM schedule3)""" % (column3, column3))
    
        # Query the player IDs remaining from the previous evaluations
        cur.execute( """SELECT playerId FROM schedule4""" )
    
        # Fetch first record from the final query
        row = cur.fetchone()
    
        # If no rows were returned in the query, then choose the only player left from the playerIdList parameter
        if row == None:
            player = playerIdList[0]
        else:
            
        # If any rows were returned in the query, use that player for the function return statement
            for i in row:
                player = int(i)
    
    # Handle any errors and print to console
    except Error as e:
        print(e)
    finally:
        
        # Drop temp tables from the database
        cur.execute( """DROP TABLE IF EXISTS schedule0_1""" )
        cur.execute( """DROP TABLE IF EXISTS schedule1""" )
        cur.execute( """DROP TABLE IF EXISTS schedule1_1""" )
        cur.execute( """DROP TABLE IF EXISTS schedule2""" )
        cur.execute( """DROP TABLE IF EXISTS schedule3""" )
        cur.execute( """DROP TABLE IF EXISTS schedule4""" )
    
    # If player exists, then return that player to the function call
    if player:
        return(player)
    
def UpdateScheduleWithNextPosition(conn, column1, game, column2, player, column3, position, column4, inning):
    """ This function inserts 1 record into the schedule table with the player, position, game, and inning details
    :param conn: database connection object
    :param column1: the first column name for the query
    :param game: the game ID for the new record
    :param column2: the second column name for the query
    :param player: the player ID for the new record
    :param column3: the third column name for the query
    :param position: the position ID for the new record
    :param column4: the fourth column name for the query
    :param inning: the inning number for the new record
    """
    
    # Create the cursor object for table navigation
    cur = conn.cursor()
    
    # Run the SQL statement to insert a new record into the Schedule table 
    cur.execute( """INSERT INTO schedule (%s, %s, %s, %s) VALUES(?, ?, ?, ?)""" %(column1, column2, column3, column4), 
                (game, player, position, inning))
    
    # Commit changes to the database
    conn.commit()
    
def UpdateTempCountersTable(conn, game, player, position, positionId, inning):
        """ This function updates the tempCounters table in the database to track position updates as the program
        calculates and determines each position for the schedule
        :param conn: connection object for the database
        :param game: the game id
        :param player: the player id
        :param position: an array for the column numbers which need to be updated
        :param inning: the inning number
        """
        
        # Create the cursor object to navigate the tables
        cur = conn.cursor()
        
        # Call the GetCurrentCounters function and store returned value in the sqlValue variable
        sqlValue = GetCurrentCounters(conn, player, position)
        
        # instantiate flag variable to 0; flag value will be used to indicate infield vs. outfield
        positionFlag = 0
        
        # If the position is greater than or equal to 5 that means it's an outfield position, so set the flag to true
        if positionId >= 5:
            positionFlag = 1
        
        # If the position is less than 5 that means it's an infield position, so set the flag to false
        else: positionFlag = 0 
        
        # Execute the SQL statement to update the tempCounters table
        cur.execute( """UPDATE tempCounters SET %s = ?, %s = ?, %s = ?, %s = ?, %s = ? WHERE playerId = ?""" 
                         %(position[0], position[1], position[2], "lastInningOutfieldFlag", "lastPositionId"), 
                         ((sqlValue[0] + 1), game, inning, positionFlag, (positionId + 1), player))
        
        # Commit changes to the database
        conn.commit()
        
def GetCurrentCounters(conn, player, position):
        """ This function grabs the current values from tempCounters table based on player ID and column name
        :param conn: database connection object
        :param player: player id
        :param position: a list of the column names to use in the query
        return value from table
        """
        
        # Create a cursor object to navigate the tables
        cur = conn.cursor()
        
        # Instantiate a new empty list for holding the values returned from the query 
        valueList = []
        
        # Loop through the column names in the position list
        for i in position:
            
            # Query to find the value from the given column name and player ID
            cur.execute( """SELECT %s FROM tempCounters WHERE playerId = ?""" %(i), (player,))
            
            # Update the value list with the value retrieved from the query 
            valueList.append(cur.fetchone())

        # Instantiate a new empty list to hold the individual integer values 
        returnList = []
        
        # Loop through the multi-dimensional list from the SQL statements, convert value to integer,
        # and store it in the new list
        for i in valueList:
            for j in i:
                returnList.append(int(j))
                
        # Return the list of integer values to the function call
        return returnList
        
    
def UpdateEntireSchedule(conn, playerCount, gameNumber, inningCount):
    """ This function is the main hub for building the schedule table; it holds the calls to the other
    functions as well as the logic for navigating players, games, innings, etc.
    :param conn: database connection object
    :param playerCount: the number of players available to be scheduled
    :param gameNumber: the game ID
    :param inningCount: the number of innings to be scheduled
    """
    
    # List of column names to be passed dynamically to various function calls
    posArr = [
                ["firstBaseCounter", "firstBaseLastGame", "firstBaseLastInning"],
                ["secondBaseCounter", "secondBaseLastGame", "secondBaseLastInning"],
                ["thirdBaseCounter", "thirdBaseLastGame", "thirdBaseLastInning"],
                ["shortStopCounter", "shortStopLastGame", "shortStopLastInning"],
                ["pitcherCounter", "pitcherLastGame", "pitcherLastInning"],
                ["rightFieldCounter", "rightFieldLastGame", "rightFieldLastInning"],
                ["leftFieldCounter", "leftFieldLastGame", "leftFieldLastInning"],
                ["centerFieldCounter", "centerFieldLastGame", "centerFieldLastInning"]
            ]
    
    # Instantiate variables
    inningNumber = 1    # variable to increment through the innings in the loops
    playerIdList = [1, 2, 3, 4, 8]     # temporary list for players present, will be replaced by user input 
    tempList = []   # a temporary list that gets used and reused throughout the loops
    
    # Populate the temp list with all of the available players
    for i in playerIdList:
        tempList.append(i)
    
    # Loop through each inning
    while inningNumber <= inningCount:
        
        # Loop through the positions list in reverse order (Starting with outfield positions first)
        for i in reversed(range(len(posArr))):
            
            # As long as there are players left to schedule, this block will execute
            if i < playerCount:
                
                # Loop through each position
                for j in range(len(posArr[i])):
                    
                    # If the position ID is 0 (This is the 'column' within the list; the idea is that this block
                    # will only execute on the 'Counter' columns and not the 'last game' or 'last inning' columns)
                    # then run the block of code 
                    if j == 0:
                        
                        # Call the find next player function passing the connection, 3 column names, list of available
                        # players, and the position ID; store returned value in the playerForPosition variable
                        playerForPosition = FindNextPlayerForPosition(conn, posArr[i][j], posArr[i][j+1], posArr[i][j+2], tempList, 
                                            (posArr.index(posArr[i])+1))
                        
                        # Logic validation
                        assert playerForPosition != None
                        
                        # Call the update schedule function passing the connection, column names and values for those columns
                        UpdateScheduleWithNextPosition(conn, "gameId", gameNumber, "playerId", playerForPosition, "positionId", (i+1), "inningNumber", inningNumber)
                        
                        # Update tempCounters table so count = count + 1, last game = gameNumber, and last inning = inningNumber
                        UpdateTempCountersTable(conn, gameNumber, playerForPosition, posArr[i], i, inningNumber)
                        
                        # Remove the player returned from the find next player function from the remp list of
                        # available players; this prevents a player from inadvertently being scheduled two positions
                        # within the same inning 
                        tempList.remove(playerForPosition)
                        
                        # Prints results of each schedule record to the console for live feedback/code troubleshooting
                        print("Inning: " + str(inningNumber) + ", Player: " + str(playerForPosition) + ", Position: " + str(posArr[i][j]))
        
        # Increment the inning by 1; i.e. inning 1 becomes inning 2 and the process repeats
        inningNumber += 1
        
        # Repopulate the temp list with the list of available players; each player should be schedule one
        # time per inning.
        for i in playerIdList:
            tempList.append(i)

def main():
    """ Main program code
    """
    
    # Path to database file
    database = r"C:\sqlite\db\t_ball_db.db"
    
    # Call the create connection function passing the database path; return the connection object and 
    # store it in the conn variable for use throughout the program
    conn = CreateConnection(database)
    
    # Call the update entire schedule function that generates the schedule for the given game; pass
    # the connection object, the game ID, the number of players available, and the number of innings
    # to schedule to the function
    UpdateEntireSchedule(conn, 5, 6, 4)

if __name__ == '__main__':
    main()
    
    
    
    # AUTHOR NOTES FOR FURTHER DEVELOPMENT
    ##########
    # still need to add function(s) to commit changes to the primary positionCounters table.
    # can I come up with a recursive model to look ahead and see if I'm trapping myself into 0 players being available
    # for the last position and then having a player in the same position 2 innings in a row?
    #
    # Need to improve the algorithm; currently it will allow a player to be at first base multiple innings in a row just because
    # of the way that it prioritizes bases and POE for the remaining players who haven't been assigned a position yet for that
    # inning.  The algorithm also does a great job of ensuring that players don't get stuck in undesirable outfield positions
    # an unfair number of times, because it chooses those positions first; the further down the list of positions you go the more
    # unfair the algorithm is because of the POE and the fact that players miss random games; should probably find a way to track
    # missed games as well so a better fairness model can be built...
    #
    # Could dramatically improve performance by modifying the SQL to pull relevant data into Pandas dataframes for ease of manipulation
    # and evaluation.
    ##########