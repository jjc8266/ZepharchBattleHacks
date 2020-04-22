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
    # dlog('Starting Turn!')
    board_size = get_board_size()

    team = get_team()
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    # dlog('Team: ' + str(team))

    robottype = get_type()
    dlog('Type: ' + str(robottype))

    if robottype == RobotType.PAWN:
        log("Starting zepharch pawn move-----------------------------------------------------------------------")
        row, col = get_location()
        # dlog('My location is: ' + str(row) + ' ' + str(col))

        if team == Team.WHITE:
            forward = 1
            inLowerHalf = lambda x:x<(board_size//2)
            index = 0

        else:
            forward = -1
            inLowerHalf = lambda x:x>=(board_size//2)
            index = board_size - 1

        madeMove = False

        if False:#col<3: #offensive pawns thar attempt to "laser" their way through a small section
            # log("im an offensive pawn ------------------------------------------------------------------------------------")
            log("started offensive pawn turn------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        
            if True:#not check_space_wrapper(row + (forward), col, board_size):
                #detect pawns defending spot row+forward,col                
                #enemy check:
                # log(str((check_space_wrapper(row + (2*forward), col - 1, board_size) == opp_team)+(check_space_wrapper(row + (2*forward), col + 1, board_size) == opp_team))+"--------------------------------------------------------")
                enemyDefForward =   (check_space_wrapper(row + (2*forward), col - 1, board_size) == opp_team)\
                                    +(check_space_wrapper(row + (2*forward), col + 1, board_size) == opp_team)
                

                #friendly check
                # frienDefForward = (check_space_wrapper(row, col - 1, board_size) == team)\
                #                     +(check_space_wrapper(row, col + 1, board_size) == team)
                if enemyDefForward == 0:
                    madeMove = True
                    move_forward()
                else:
                    frienDefForward = 0
                    if not check_space_wrapper(row+forward,col-1,board_size):
                        frienDefForward+= (check_space_wrapper(row-forward,col-1,board_size) == team)
                    else:
                        frienDefForward+= ((check_space_wrapper(row-forward,col-1,board_size) == team)+(check_space_wrapper(row,col-1,board_size) == team))

                    if not check_space_wrapper(row+forward,col+1,board_size):
                        frienDefForward+= (check_space_wrapper(row-forward,col+1,board_size) == team)
                    else:
                        frienDefForward+= ((check_space_wrapper(row-forward,col+1,board_size) == team)+(check_space_wrapper(row,col+1,board_size) == team))

                    log("pawntrade result:"+str(frienDefForward-enemyDefForward))
                    if frienDefForward-enemyDefForward>0 and check_space_wrapper(row-forward,col,board_size) == team:
                        madeMove = True
                        move_forward()
            
            #check if you can make a capture to the right
            if not madeMove and check_space_wrapper(row + (forward), col+1, board_size) == opp_team:
                #detect pawns defending spot row+forward,col+1
                #enemy check:
                enemyDefForwardCapRight =   (check_space_wrapper(row + (2*forward), col , board_size) == opp_team)\
                                    +(check_space_wrapper(row + (2*forward), col + 2, board_size) == opp_team)
                #friendly check
                frienDefForwardCapRight = 1+(check_space_wrapper(row, col + 2, board_size) == team)    
                log("CaptureRightResult:"+str(frienDefForwardCapRight-enemyDefForwardCapRight))
                if frienDefForwardCapRight-enemyDefForwardCapRight>=0:
                    if not (row == index and check_space_wrapper(row+forward,col,board_size) == opp_team):
                        madeMove = True
                        capture(row+forward,col+1)

            #check if you can make a capture to the left
            if not madeMove and check_space_wrapper(row + (forward), col-1, board_size) == opp_team:
                #detect pawns defending spot row+forward,col-1
                #enemy check:
                enemyDefForwardCapLeft =   (check_space_wrapper(row + (2*forward), col , board_size) == opp_team)\
                                    +(check_space_wrapper(row + (2*forward), col - 2, board_size) == opp_team)
                #friendly check
                frienDefForwardCapLeft = 1+(check_space_wrapper(row, col - 2, board_size) == team)
                log("CaptureLeftResult:"+str(frienDefForwardCapLeft-enemyDefForwardCapLeft))
                if frienDefForwardCapLeft-enemyDefForwardCapLeft>=0:
                    if not (row == index and check_space_wrapper(row+forward,col,board_size) == opp_team):
                        madeMove = True
                        capture(row+forward,col-1)
                
            log("done--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        else: #these are defensive pawns whose goal is to give up no ground!
            if check_space_wrapper(row + forward, col + 1, board_size) == opp_team: # up and right
                if not (row == index and check_space_wrapper(row+forward,col,board_size) == opp_team):
                    madeMove = True
                    capture(row + forward, col + 1)
                # dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')

            if not madeMove and check_space_wrapper(row + forward, col - 1, board_size) == opp_team: # up and left
                if not (row == index and check_space_wrapper(row+forward,col,board_size) == opp_team):
                    madeMove = True
                    capture(row + forward, col - 1)
                # dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')
            
            if not madeMove and not (check_space_wrapper(row + (2*forward), col - 1, board_size) == opp_team or check_space_wrapper(row + (2*forward), col + 1, board_size) == opp_team):
                # if not check_space_wrapper(row+forward,col,board_size):
                if inLowerHalf(row):
                    madeMove = True
                    move_forward()
                elif col%2==1:
                    log("move test in odd column---------------------------------------")
                    if not (check_space_wrapper(row+forward,col+1,board_size) == team or check_space_wrapper(row+forward,col-1,board_size) == team):
                        if check_space_wrapper(row+forward,col,board_size) == team or check_space_wrapper(row+(2*forward),col,board_size) == team:
                            madeMove = True
                            move_forward()
                        elif check_space_wrapper(row-forward,col,board_size) == team:
                            madeMove = True
                            move_forward()
                else:
                    log("move test in even column---------------------------------------")
                    if check_space_wrapper(row+forward,col,board_size) == team or check_space_wrapper(row+(2*forward),col,board_size) == team:
                        madeMove = True
                        move_forward()
                    elif check_space_wrapper(row-forward,col,board_size) == team:
                        madeMove = True
                        move_forward()
                    # move_forward()
            if not madeMove and col<board_size and check_space_wrapper(row-forward,col,board_size) == team and check_space_wrapper(row-(2*forward),col,board_size) == team:
                move_forward()
        log("Finished zepharch pawn move-----------------------------------------------------------------------")

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
        spawned = False

        #sensor pre-computing
        for idx,column in enumerate(transposedBoard):
            numFriendlies = column.count(team)
            colDict[numFriendlies] = idx
            countList.append(numFriendlies)
            frienCount+=numFriendlies
            #determine if pawn can be captured next round
            if check_space_wrapper(index + forward, idx - 1, board_size) == opp_team\
                or check_space_wrapper(index + forward, idx + 1, board_size) == opp_team:
                noGoZone.append(idx)

            if opp_team in column:
                if team == team.BLACK:
                    column.reverse()
                dist = column.index(opp_team)               
                blockerCount = column[:dist].count(team)
                enemyDistList.append((blockerCount,dist,idx))
        spawned = False
        def mimick():
            spawned = False
            enemyDistList.sort()
            if enemyDistList:
                for _,_,i in enemyDistList:
                    if not check_space(index, i) and i not in noGoZone:
                        spawn(index, i)
                        dlog('Spawned defensive unit at: (' + str(index) + ', ' + str(i) + ')')
                        spawned = True
                        break
            if not spawned:
                for _ in range(board_size):
                    i = random.randint(0, board_size - 1)
                    if not check_space(index, i):
                        spawn(index, i)
                        spawned = True
                        # dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                        break

        
        if frienCount<board_size: #mimick opponents placement
            # log("numfriendlies:"+str(frienCount)+"adsffffffffffffffffffffffffffffffffffffffffffffffffff")
            spawned = False
            mimick()

        else:
            defenderCount = [a[0] for a in enemyDistList]
            spawned = False
            for x in defenderCount:
                if x<3:
                    mimick()
                    spawned = True
                    break
            laserList = sorted([(transposedBoard[colDex].count(team),colDex) for colDex in range(3)])
            for _,colDex in laserList:
                if not check_space(index, colDex) and colDex not in noGoZone:
                    spawn(index,colDex)
                    spawned = True
                    break
            if not spawned:
                mimick()
            
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))