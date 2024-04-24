

def createBoard():
    initBoard = []
    for i in range(0,6):
        column = []
        for j in range(0,6):
            column.append("-")
        initBoard.append(column)
    return initBoard


def printBoard(board):
    for i in range(len(board[0])-1,-1,-1):
        printString = "|"
        for j in range(0,len(board)):
            printString = printString + " " + (board[j][i])
        printString = printString + " " + "|"
        print(printString)

def gameHasEnded(board):
    # Check rows
    for row in board:
        for i in range(3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] != '-':
                return row[i]  # Return the winner ('X' or 'O')

    # Check columns
    for col in range(6):
        for i in range(3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] != '-':
                return board[i][col]  # Return the winner ('X' or 'O')

    # Check diagonals (top-left to bottom-right)
    for i in range(3):
        for j in range(3):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] != '-':
                return board[i][j]  # Return the winner ('X' or 'O')

    # Check diagonals (top-right to bottom-left)
    for i in range(3):
        for j in range(3, 6):
            if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] != '-':
                return board[i][j]  # Return the winner ('X' or 'O')

    return False  # No winner yet

def makeMove(board, move, player):
    playerPiece = ""
    if(player == 1):
        playerPiece = "X"
    else:
        playerPiece = "O"

    column = board[move]
    i = 0
    while(column[i] == "X" or column[i] == "O"):
        i += 1
        if(i>5):
            return False
   
    column[i] = playerPiece
    board[move] = column
    return board

def playGame():
    initBoard = createBoard()
    printBoard(initBoard)
    board = initBoard
    turn = 0
    while(True):
        player = 1
        if(turn % 2 == 0):
            player = 1
        else:
            player = 2
        
        while(True):
            move = int(input("Player " + str(player) + " choose a column between 0-5\n"))
            if(move < 0 or move > 5 ):
                print("Please enter a value between 0-5")
                continue
            newBoard = makeMove(board,move, player)
            if(newBoard == False):
                print("Cannot make that move")
                continue
            else:
                board = newBoard
                printBoard(board)
                break
        
        turn+=1
        resultFromMove = gameHasEnded(board)
        if(resultFromMove == False):
            continue
        else:
            print(f"{resultFromMove} wins!")
            break

playGame()