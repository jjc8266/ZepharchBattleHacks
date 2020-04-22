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

        #variable for if we can move forward
        canMoveForward = check_is_oob(row + forward, col) == False and check_space(row + forward, col) == False

        enemyDefForward =   (check_space_wrapper(row + (2*forward), col - 1, board_size) == opp_team)\
                                    +(check_space_wrapper(row + (2*forward), col + 1, board_size) == opp_team)

        #move forward if we can and we won't be captured for doing so
        if canMoveForward and enemyDefForward == 0:
            #if this pawn is acting as an "ally" pawn for another, don't move
            #left side check
            if check_is_oob(row + forward, col - 1) == False and check_space(row + forward, col - 1) == team:
                #there is an ally here, are they under attack?
                if check_is_oob(row + 2*forward, col) == False and check_space(row + 2*forward, col) == opp_team:
                    return #don't move!
                elif check_is_oob(row + 2*forward, col - 2) == False and check_space(row + 2*forward, col - 2) == opp_team:
                    return #don't move!
            #right side check
            if check_is_oob(row + forward, col + 1) == False and check_space(row + forward, col + 1) == team:
                #there is an ally here, are they under attack?
                if check_is_oob(row + 2*forward, col) == False and check_space(row + 2*forward, col) == opp_team:
                    return #don't move!
                elif check_is_oob(row + 2*forward, col + 2) == False and check_space(row + 2*forward, col + 2) == opp_team:
                    return #don't move!
            #if we've reached this point, then it's not helping another pawn defend
            move_forward()
            return
        

        #if we're at this point, we either can't move forward (for threat of capture) or we're helping another pawn defend
        #but if we're under attack, self-defense takes precedent
        #capture if possible
        toCapture = []
        if check_is_oob(row + forward, col + 1) == False and check_space(row + forward, col + 1) == opp_team:
            toCapture.append((row + forward, col + 1))
        if check_is_oob(row + forward, col - 1) == False and check_space(row + forward, col - 1) == opp_team:
            toCapture.append((row + forward, col - 1))
        if len(toCapture) != 0:
            move_r, move_c = random.choice(toCapture)
            capture(move_r, move_c)
            return
        
        #if we're at this point, we can't capture and there should be a threat preventing us from moving fwd
        friendDefSide = (check_space_wrapper(row, col - 1, board_size) == team)\
                                    +(check_space_wrapper(row, col + 1, board_size) == team)
        if canMoveForward and friendDefSide > enemyDefForward:
            if random.random() < 0.4:
                log("I am defended!")
                move_forward()
                return
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