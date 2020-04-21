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

    dlog('Starting Turn!')
    board_size = get_board_size()
    team = get_team()
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    dlog('Team: ' + str(team))
    robottype = get_type()
    dlog('Type: ' + str(robottype))

    if robottype == RobotType.PAWN:
        #keep demo's pawn code
        row, col = get_location()
        dlog('My location is: ' + str(row) + ' ' + str(col))
        if team == Team.WHITE:
            forward = 1
        else:
            forward = -1
        if check_space_wrapper(row + forward, col + 1, board_size) == opp_team: # up and right
            capture(row + forward, col + 1)
            dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')
        elif check_space_wrapper(row + forward, col - 1, board_size) == opp_team: # up and left
            capture(row + forward, col - 1)
            dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')
        # otherwise try to move forward
        elif row + forward != -1 and row + forward != board_size and not check_space_wrapper(row + forward, col, board_size):
            #               ^  not off the board    ^            and    ^ directly forward is empty
            move_forward()
            dlog('Moved forward!')
    else:
        if team == Team.WHITE:
            index = 0
        else:
            index = board_size - 1
        #search for places where pawns are needed to defend
        hasPlaced = False
        defendLocations = []
        emptyLocations = []
        otherLocations = []
        for c in range(board_size):
            if(check_space(index, c) != False): continue #don't check if we can't place anyways
            presentTeams = set()
            for r in range(1, board_size):
                result = check_space(r, c)
                if result != False:
                    presentTeams.add(result)
            if len(presentTeams) == 1 and opp_team in presentTeams: #meaning only an opponent is in the column
                defendLocations.append(c)
            elif len(presentTeams) == 1:
                otherLocations.append(c) 
            elif len(presentTeams) == 0:
                emptyLocations.append(c)
        if len(defendLocations) > 0:
            spawn(index, defendLocations[0])
        elif len(emptyLocations) > 0:
            spawn(index, emptyLocations[0])
        elif len(otherLocations) > 0:
            spawn(index, otherLocations[0])
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))

