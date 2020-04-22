import random
from battlehack20.stubs import *

DEBUG = 0
def dlog(str):
    if DEBUG > 0:
        log(str)


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
    # dlog('Starting Turn!')
    board_size = get_board_size()

    team = get_team()
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    # dlog('Team: ' + str(team))

    robottype = get_type()
    dlog('Type: ' + str(robottype))

    if robottype == RobotType.PAWN:
        row, col = get_location()
        # dlog('My location is: ' + str(row) + ' ' + str(col))

        if team == Team.WHITE:
            forward = 1
            inLowerHalf = lambda x:x<(board_size//2)+1
            index = 0

        else:
            forward = -1
            inLowerHalf = lambda x:x>=(board_size//2)-1
            index = board_size - 1

        madeMove = False

        if col%2 == 0:
            # move_forward()

            if check_space_wrapper(row + forward, col + 1, board_size) == opp_team: # up and right
                capture(row + forward, col + 1)
                # dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')

            elif check_space_wrapper(row + forward, col - 1, board_size) == opp_team: # up and left
                capture(row + forward, col - 1)
            # dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')
            else:
                if not (check_space_wrapper(row+(2*forward),col+1,board_size) == opp_team or check_space_wrapper(row+(2*forward),col-1,board_size) == opp_team):
                    move_forward()


        

    else: #This is the overlord
        if team == Team.WHITE:
            opp_team = Team.BLACK
            index = 0
            forward = 1
        else:
            opp_team = Team.WHITE
            index = board_size - 1
            forward = -1

        currState = get_board()
        # for row in currState:
        #     dlog(str(row))

        #transpose matrix
        transposedBoard = [[currState[j][i] for j in range(len(currState))] for i in range(len(currState[0]))] 
        countList = [] #number of friendlies in each column
        colDict = {} #col numFriendlies to column idx

        enemyDistList = []
        noGoZone = [] #list of indices where a pawn placed will be immediatly captured
        frienCount = 0

        

        #sensor pre-computing
        for idx,column in enumerate(transposedBoard):
            if idx%2 ==1:
                continue
            numFriendlies = column.count(team)
            
            countList.append((numFriendlies,idx))
            frienCount+=numFriendlies
        
        for _,colDex in sorted(countList):
            if not check_space(index, colDex) and colDex not in noGoZone:
                spawn(index,colDex)
                spawned = True
                log(str(colDex))
                break
        if not spawned:
            for x in range(board_size):
                if not check_space(index, colDex) and colDex not in noGoZone:
                    spawn(index,x)
                    spawned = True
                    break
            
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))