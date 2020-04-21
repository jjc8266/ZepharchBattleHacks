import random
from battlehack20.stubs import *

DEBUG = 1
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

        if col<3: #offensive pawns thar attempt to "laser" their way through a small section
            
            if not check_space_wrapper(row + (forward), col, board_size):
                #detect pawns defending spot row+foward,col                
                #enemy check:
                enemyDefForward =   check_space_wrapper(row + (2*forward), col - 1, board_size) == opp_team\
                                    +check_space_wrapper(row + (2*forward), col + 1, board_size) == opp_team
                #friendly check
                frienDefForward = check_space_wrapper(row + (2*forward), col - 1, board_size) == team\
                                    +check_space_wrapper(row + (2*forward), col + 1, board_size) == team

                if frienDefForward-enemyDefForward>=0:
                    madeMove = True
                    move_forward()
            
            #check if you can make a capture to the right
            elif not madeMove and check_space_wrapper(row + (forward), col+1, board_size) == opp_team:
                #detect pawns defending spot row+foward,col+1
                #enemy check:
                enemyDefForwardCapRight =   check_space_wrapper(row + (2*forward), col , board_size) == opp_team\
                                    +check_space_wrapper(row + (2*forward), col + 2, board_size) == opp_team
                #friendly check
                frienDefForwardCapRight = 1+check_space_wrapper(row, col + 2, board_size) == team    
                
                if frienDefForwardCapRight-enemyDefForward>=0:
                    madeMove = True
                    capture(row+forward,col+1)

            #check if you can make a capture to the left
            elif not madeMove and check_space_wrapper(row + (forward), col-1, board_size) == opp_team:
                #detect pawns defending spot row+foward,col-1
                #enemy check:
                enemyDefForwardCapRight =   check_space_wrapper(row + (2*forward), col , board_size) == opp_team\
                                    +check_space_wrapper(row + (2*forward), col - 2, board_size) == opp_team
                #friendly check
                frienDefForwardCapRight = 1+check_space_wrapper(row, col - 2, board_size) == team    
                
                if frienDefForwardCapRight-enemyDefForward>=0:
                    madeMove = True
                    capture(row+forward,col-1)
                

        else: #these are defensive pawns whose goal is to give up no ground!
            if check_space_wrapper(row + forward, col + 1, board_size) == opp_team: # up and right
                if row != index:
                    madeMove = True
                    capture(row + forward, col + 1)
                # dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')

            if not madeMove and check_space_wrapper(row + forward, col - 1, board_size) == opp_team: # up and left
                if row != index:
                    madeMove = True
                    capture(row + forward, col - 1)
                # dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')
            
            if not madeMove and not (check_space_wrapper(row + (2*forward), col - 1, board_size) == opp_team or check_space_wrapper(row + (2*forward), col + 1, board_size) == opp_team):
                if not check_space_wrapper(row+forward,col,board_size):
                    if inLowerHalf(row):
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
        #sensor pre-computing
        for idx,column in enumerate(transposedBoard):
            numFriendlies = column.count(team)
            colDict[numFriendlies] = idx
            countList.append(numFriendlies)
            
            #determine if pawn can be captured next round
            if check_space_wrapper(index + forward, idx - 1, board_size) == opp_team\
                or check_space_wrapper(index + forward, idx + 1, board_size) == opp_team:
                noGoZone.append(idx)

            if opp_team in column:
                if team == team.BLACK:
                    column.reverse()
                dist = column.index(opp_team)               

                if dist<7   :
                    if team not in column[:dist]:
                        enemyDistList.append((dist,idx))

        def offensivePlacement():
            countList.sort() # determins which col has the least frendlies
            spawned = False
            for numFriendlies in countList:
                i = colDict[numFriendlies]
                if not check_space(index, i) and i not in noGoZone:
                    spawn(index, i)
                    dlog('Spawned offensive unit at: (' + str(index) + ', ' + str(i) + ')')
                    spawned = True
                    break
            if not spawned:
                for i in range(board_size):
                    if not check_space(index, i) and i not in noGoZone:
                        spawn(index, i)
                        dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                        break


        if enemyDistList:
            enemyDistList.sort()
            spawned = False
            for _,i in enemyDistList:
                if not check_space(index, i) and i not in noGoZone:
                    spawn(index, i)
                    dlog('Spawned defensive unit at: (' + str(index) + ', ' + str(i) + ')')
                    spawned = True
            if not spawned:
                offensivePlacement() 
        
        else: #offensive placement
            offensivePlacement()
            # count = 0
            # while count<16:
            #     i = random.randint(0, board_size - 1)
            #     if not check_space(index, i) and (team not in transposedBoard[i] or count>=board_size):
            #         spawn(index, i)
            #         dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
            #         break
            #     count+=1

    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))

