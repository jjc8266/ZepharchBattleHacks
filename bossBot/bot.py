import random
from battlehack20.stubs import *

DEBUG = 0
def dlog(str):
    if DEBUG > 0:
        log(str)

def check_is_oob(r, c):
    if r < 0 or c < 0 or c >= 16 or r >= 16:
        return True
    return False

def check_space_wrapper(r, c, board_size):
    # check space, except doesn't hit you with game errors
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    try:
        return check_space(r, c)
    except:
        return None

def turn():
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    #some useful stuff
    team = get_team()
    opp_team = Team.BLACK
    index = 0
    forward = 1
    if team == team.BLACK:
        opp_team = Team.WHITE
        index = 15
        forward = -1

    robottype = get_type()
    board_size = get_board_size()
    if robottype == RobotType.PAWN:
        row, col = get_location()
        #store sense results in a default dictionary for convenience
        senseMap = {(row + x, y + col) : None for x in range (-2, 3) for y in range(-2, 3)}
        for r, c, color in sense():
            senseMap[(r, c)] = color

        ###No matter pawn type, see if it's in threat of being captured
        toCapture = []
        log("Checking if I'm in danger!")
        if check_is_oob(row, col + 1) == False and check_space(row + forward, col + 1) == opp_team:
            toCapture.append((row + forward, col + 1))
        if check_is_oob(row, col - 1) == False and check_space(row + forward, col - 1) == opp_team:
            toCapture.append((row + forward, col - 1))
        #choose the only capture position if there's only 1
        #else do coinflip if there are 2
        log("Checking done!")
        if len(toCapture) != 0:
            move_r, move_c = random.choice(toCapture)
            capture(move_r, move_c)
            return
            
        ###These are the zerg rushers
        if col < 3: #Fearless, brave warriors. They risk their lives for the overlord.
            if check_is_oob(row + forward, col) == False and check_space(row + forward, col) == False:
                move_forward()
        
        ###These are normal defensive pawns
        else:
            #get number of possible attackers if moves forward
            numAttackers = 0
            if check_is_oob(row + forward, col + 1) == False and check_space(row + forward, col + 1) == opp_team:
                numAttackers += 1
            if check_is_oob(row + forward, col - 1) == False and check_space(row + forward, col - 1) == opp_team:
                numAttackers += 1
            #get num allies that can cap potential attackers
            numHelpers = 0
            if check_is_oob(row, col + 1) == False and check_space(row, col + 1) == team:
                numHelpers += 1
            if check_is_oob(row, col - 1) == False and check_space(row, col - 1) == team:
                numHelpers += 1
            
            if check_is_oob(row + forward, col) == False and check_space(row + forward, col) == False: #possible to move
                if numAttackers == 0:
                    move_forward()
                if numHelpers > numAttackers:
                    move_forward()

    else: #This is the overlord
        currState = get_board()
        #deploy pawns in defensive columns until there are at least 2 in each
        oppColCounts = [0 for _ in range(16)] #number of enemies in each column
        myColCounts = [0 for _ in range(16)]
        closestOpp = [16 for _ in range(16)] #distance to closest enemy in each col
        for x, row in enumerate(currState): #for each row
            for y, bot in enumerate(currState): #for each col
                if bot == team:
                    myColCounts[y] = myColCounts[y] + 1
                elif bot == opp_team:
                    oppDist = abs(index - x)
                    closestOpp[y] = min(closestOpp[y], oppDist)
                    oppColCounts[y] = oppColCounts[y] + 1
        columns = [x for x in range(16)] #sort this based on closest enemies
        columns.sort(key = lambda x: closestOpp[x]) #sort
        #take defensive action in column if oppPawns / 2 >= myPawns
        #sorted by danger level
        for col in columns:
            if col % 2 == 1: #only deploy in odd columns
                if oppColCounts[col] / 2 > myColCounts[col]:
                    spawn(index, col)
                    return
        #haven't deployed pawns yet? attack time
        attackLocations = []
        for col in range(3):
            if check_space(index, col) == False:
                attackLocations.append(col)
        if len(attackLocations) > 0:
            spawn(index, random.choice(attackLocations))
            return
        #still haven't deployed yet? means that attack columns are backed up
        #so just deploy in whatever column is possible
        for col in columns:
            if check_space(index, col) == False:
                spawn(index, col)
                return


        
        
            
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))