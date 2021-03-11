class GameState:
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

        self.moveFunctions = {"P": self.getPawnMoves, "R": self.getRookMoves, "B": self.getBishopMoves,
                              "N": self.getKnightMoves, "K": self.getKingMoves, "Q": self.getQueenMoves}

        self.moveLog = []
        self.whiteMoves = True
        self.wKing = (7, 4)
        self.bKing = (0, 4)
        self.inCheck = False
        self.checks = []
        self.pins = []

    def makeMove(self, move):
        self.board[move.startR][move.startC] = '--'
        self.board[move.endR][move.endC] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteMoves = not self.whiteMoves
        if move.pieceMoved == "wK":
            self.wKing = (move.endR, move.endC)
        elif move.pieceMoved == "bK":
            self.bKing = (move.endR, move.endC)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startR][move.startC] = move.pieceMoved
            self.board[move.endR][move.endC] = move.pieceCaptured
            self.whiteMoves = not self.whiteMoves
            if move.pieceMoved == "wK":
                self.wKing = (move.startR, move.startC)
            elif move.pieceMoved == "bK":
                self.bKing = (move.startR, move.startC)

    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.pinsAndChecks()
        if self.whiteMoves:
            kingRow = self.wKing[0]
            kingCol = self.wKing[1]
        else:
            kingRow = self.bKing[0]
            kingCol = self.bKing[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for k in range(len(moves)-1, -1, -1):
                    if moves[k].pieceMoved[1] != 'K':
                        if not (moves[k].endR, moves[k].endC) in validSquares:
                            moves.remove(moves[k])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getPossibleMoves()
        return moves

    def inBound(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    def pinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteMoves:
            allyColor = 'w'
            enemyColor = 'b'
            kingRow = self.wKing[0]
            kingCol = self.wKing[1]
        else:
            allyColor = 'b'
            enemyColor = 'w'
            kingRow = self.bKing[0]
            kingCol = self.bKing[1]
        coordinates = [[-1, 0], [0, -1], [0, 1], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]
        for index, (i, j) in enumerate(coordinates):
            possiblePin = ()
            for k in range(1, 8):
                endRow = kingRow + k * i
                endCol = kingCol + k * j
                if self.inBound(endRow, endCol):
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, i, j)
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        piece = endPiece[1]
                        if (0 <= index <= 3 and piece == 'R') or (4 <= index <= 7 and piece == 'B') or \
                                (k == 1 and piece == 'P' and ((enemyColor == 'w' and 6 <= index <= 7) or
                                 (enemyColor == 'b' and 4 <= index <= 5))) or \
                                (piece == 'Q') or (k == 1 and piece == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, i, j))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightC = [[-2, -1], [-1, -2], [-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2]]
        for (i, j) in knightC:
            endRow = kingRow + i
            endCol = kingCol + j
            if self.inBound(endRow, endCol):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, i, j))
        return inCheck, pins, checks

    def getPossibleMoves(self):
        moves = []
        for x in range(0, 8):
            for y in range(0, 8):
                color = self.board[x][y][0]
                if (color == 'w' and self.whiteMoves) or (color == 'b' and not self.whiteMoves):
                    piece = self.board[x][y][1]
                    self.moveFunctions[piece](x, y, moves)
        return moves

    def getKingMoves(self, x, y, moves):
        coordinates = [[-1, 0], [0, -1], [0, 1], [1, 0], [-1, 1], [1, -1], [-1, -1], [1, 1]]
        color = self.board[x][y][0]
        for (i, j) in coordinates:
            if self.inBound(x + i, y + j):
                endPiece = self.board[x+i][y+j]
                if endPiece[0] != color:
                    if color == 'w':
                        self.wKing = (x+i, y+j)
                    else:
                        self.bKing = (x+i, y+j)
                    inCheck, pins, checks = self.pinsAndChecks()
                    if not inCheck:
                        moves.append(Move((x, y), (x + i, y + j), self.board))
                    if color == 'w':
                        self.wKing = (x, y)
                    else:
                        self.bKing = (x, y)

    def getQueenMoves(self, x, y, moves):
        self.getRookMoves(x, y, moves)
        self.getBishopMoves(x, y, moves)

    def getKnightMoves(self, x, y, moves):
        pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == x and self.pins[i][1] == y:
                pinned = True
                self.pins.remove(self.pins[i])
                break
        coordinates = [[-2, -1], [-1, -2], [-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2]]
        for (i, j) in coordinates:
            if self.inBound(x+i, y+j):
                if not pinned:
                    if self.board[x + i][y + j][0] != self.board[x][y][0]:
                        moves.append(Move((x, y), (x+i, y+j), self.board))

    def getRookMoves(self, x, y, moves):
        pinned = False
        direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == x and self.pins[i][1] == y:
                pinned = True
                direction = (self.pins[i][2], self.pins[i][3])
                if self.board[x][y][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        coordinates = [[-1, 0], [0, -1], [0, 1], [1, 0]]
        for (i, j) in coordinates:
            for k in range(1, 8):
                if self.inBound(x + k * i, y + k * j):
                    if not pinned or direction == (i, j) or direction == (-i, -j):
                        if self.board[x + k * i][y + k * j][0] == self.board[x][y][0]:
                            break
                        moves.append(Move((x, y), (x + k * i, y + k * j), self.board))
                        if self.board[x + k * i][y + k * j] != "--":
                            break
                else:
                    break

    def getBishopMoves(self, x, y, moves):
        pinned = False
        direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == x and self.pins[i][1] == y:
                pinned = True
                direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        coordinates = [[-1, 1], [1, -1], [-1, -1], [1, 1]]
        for (i, j) in coordinates:
            for k in range(1, 8):
                if self.inBound(x + k * i, y + k * j):
                    if not pinned or direction == (i, j) or direction == (-i, -j):
                        if self.board[x + k * i][y + k * j][0] == self.board[x][y][0]:
                            break
                        moves.append(Move((x, y), (x + k * i, y + k * j), self.board))
                        if self.board[x + k * i][y + k * j] != "--":
                            break
                else:
                    break

    def getPawnMoves(self, x, y, moves):
        pinned = False
        direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == x and self.pins[i][1] == y:
                pinned = True
                direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteMoves:
            if self.board[x - 1][y] == '--':
                if not pinned or direction == (-1, 0):
                    moves.append(Move((x, y), (x - 1, y), self.board))
                    if x == 6 and self.board[x - 2][y] == '--':
                        moves.append(Move((x, y), (x - 2, y), self.board))
            if y - 1 >= 0:
                if not pinned or direction == (-1, -1):
                    if self.board[x - 1][y - 1][0] == 'b':  # and self.board[x - 1][y - 1] != 'bK':
                        moves.append(Move((x, y), (x - 1, y - 1), self.board))
            if y + 1 <= 7:
                if not pinned or direction == (-1, 1):
                    if self.board[x - 1][y + 1][0] == 'b':  # and self.board[x - 1][y + 1] != 'bK':
                        moves.append(Move((x, y), (x - 1, y + 1), self.board))
        else:
            if self.board[x + 1][y] == '--':
                if not pinned or direction == (1, 0):
                    moves.append(Move((x, y), (x + 1, y), self.board))
                    if x == 1 and self.board[x + 2][y] == '--':
                        moves.append(Move((x, y), (x + 2, y), self.board))
            if y + 1 <= 7:
                if not pinned or direction == (1, 1):
                    if self.board[x + 1][y + 1][0] == 'w':  # and self.board[x + 1][y + 1] != 'wK':
                        moves.append(Move((x, y), (x + 1, y + 1), self.board))
            if y - 1 >= 0:
                if not pinned or direction == (1, -1):
                    if self.board[x + 1][y - 1][0] == 'w':  # and self.board[x + 1][y - 1] != 'wK':
                        moves.append(Move((x, y), (x + 1, y - 1), self.board))


class Move:
    ranksToRows = {'1': 0, '2': 1, '3': 2, '4': 3,
                   '5': 4, '6': 5, '7': 6, '8': 7}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, start, end, board):
        self.startR = start[0]
        self.startC = start[1]
        self.endR = end[0]
        self.endC = end[1]
        self.pieceMoved = board[self.startR][self.startC]
        self.pieceCaptured = board[self.endR][self.endC]
        self.moveID = start[0] * 1000 + start[1] * 100 + end[0] * 10 + end[1]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getNotation(self):
        start = self.colsToFiles[self.startC] + self.rowsToRanks[self.startR]
        end = self.colsToFiles[self.endC] + self.rowsToRanks[self.endR]
        return start + end
