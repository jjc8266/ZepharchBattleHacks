BLACK = "B"
WHITE = "W"
otherTeam = {"B" : "W", "W" : "B"}
def getSelf():
    return (3,2, "W")

def sense():
    return [(2, 2, "B"), (5, 3, "W")]

def copyBoard(board):
    return {tup : board[tup] for tup in board}

def prettyPrint(locations):
    gameboard = [[0 for y in range(5)] for x in range(5)]
    for r, c in locations:
        gameboard[r][c] = locations[(r, c)]
    for r in range(4, -1, -1):
        line = ""
        for c in range(5):
            line += " " + str(gameboard[r][c])
        print(line)
    print()

def getMovesHelper(boards, my_pieces, color):
    if(len(my_pieces) == 0):
        return boards
    newboards = []
    r, c = my_pieces[-1]
    for b in boards:
        newboards.append(copyBoard(b)) #piece doesn't move option
        if color == BLACK:
            if r - 1 >= 0: #not end of board
                if (r - 1, c) not in b: #can move forward
                    new_b = copyBoard(b)
                    del new_b[(r, c)]
                    new_b[(r - 1, c)] = BLACK
                    newboards.append(new_b)
                if c - 1 >= 0 and (r - 1, c - 1) in b and b[(r - 1, c - 1)] == WHITE: #can cap diag
                    new_b = copyBoard(b)
                    del new_b[(r, c)]
                    new_b[(r - 1, c - 1)] = BLACK
                    newboards.append(new_b)
                if c + 1 < 5 and (r - 1, c + 1) in b and b[(r - 1, c + 1)] == WHITE: #can cap other diag
                    new_b = copyBoard(b)
                    del new_b[(r, c)]
                    new_b[(r - 1, c + 1)] = BLACK
                    newboards.append(new_b)
        else: #white
            if r + 1 < 5: #not end of board
                if (r + 1, c) not in b: #can move forward
                    new_b = copyBoard(b)
                    del new_b[(r, c)]
                    new_b[(r + 1, c)] = WHITE
                    newboards.append(new_b)
                if c - 1 >= 0 and (r + 1, c - 1) in b and b[(r + 1, c - 1)] == BLACK: #can cap diag
                    new_b = copyBoard(b)
                    del new_b[(r, c)]
                    new_b[(r + 1, c - 1)] = WHITE
                    newboards.append(new_b)
                if c + 1 < 5 and (r + 1, c + 1) in b and b[(r + 1, c + 1)] == BLACK: #can cap other diag
                    new_b = copyBoard(b)
                    del new_b[(r, c)]
                    new_b[(r + 1, c + 1)] = WHITE
                    newboards.append(new_b)
    my_pieces.pop()
    for b in newboards:
        prettyPrint(b)
    return getMovesHelper(newboards, my_pieces, color)

def getPossibleMoves(board, team, my_location):
    myPieces = []
    oppPieces = []
    for loc in board:
        if board[loc] != team:
            oppPieces.append((r, c))
        elif loc != my_location:
            myPieces.append(loc)
    myPieces.append(my_location) #only append my location at the end
                                 #becuase it means it'll be the first to get popped from stack
    return getMovesHelper([board], myPieces, team)

def eval(board, team):
    return 1 #need heuristic

def minimax(board, team, depth, my_location): #need to track my_location for move ordering purposes
    print("depth is", depth)
    if depth == 0:
        return eval(board, team)
    else:
        newboards = getPossibleMoves(board, team, my_location)
        best_score = -9999 #arbitrary
        best_move = -1
        for b in newboards:
            score = -minimax(b, otherTeam[team], depth - 1, my_location)
            if score > best_score:
                best_score = score
                best_move = b
                #@TODO best_move is currently a board, it needs to be a move
        return best_score

if __name__ == "__main__": #from perspective of a single pawn
    board = dict()
    my_r, my_c, my_team = getSelf()
    for r, c, color in sense():
        board[(r - my_r + 2, c - my_c + 2)] = color
    board[(2, 2)] = my_team
    minimax(board, my_team, 2, (2, 2))
