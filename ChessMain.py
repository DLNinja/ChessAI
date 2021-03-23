import pygame as p
from ChessEngine import *
from AI import *
import random

DIMENSION = 8
WIDTH = HEIGHT = 512
SQUARE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
PIECES = ['wP', 'wK', 'wQ', 'wB', 'wR', 'wN', 'bP', 'bK', 'bQ', 'bB', 'bR', 'bN']


def load_img():
    for piece in PIECES:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"), (SQUARE, SQUARE))

# PvP Mode

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    load_img()
    state = GameState()
    validMoves = state.getValidMoves()
    moveMade = False
    running = True
    sqSelected = ()
    positions = []
    animate = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                position = p.mouse.get_pos()
                col = position[0]//SQUARE
                row = position[1]//SQUARE
                if sqSelected == (row, col):
                    sqSelected = ()
                    positions = []
                else:
                    sqSelected = (row, col)
                    positions.append(sqSelected)
                if len(positions) == 2:
                    move = Move(positions[0], positions[1], state.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            state.makeMove(move)
                            moveMade = True
                            animate = True
                            sqSelected = ()
                            positions = []
                    if not moveMade:
                        positions = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u: # undo move when key "U" is pressed
                    state.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: # reset game when key "R" is pressed
                    state = GameState()
                    validMoves = state.getValidMoves()
                    sqSelected = ()
                    positions = []
                    animate = False
                    moveMade = False
        if moveMade:
            if animate:
                moveAnimation(state.moveLog[-1], screen, state.board, clock)
            validMoves = state.getValidMoves()
            moveMade = False
        drawGameState(screen, state, positions, validMoves)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, state, positions, moves):
    drawBoard(screen)
    drawPieces(screen, state.board)
    highlightSquares(screen, state.board, positions, moves)

def drawBoard(screen):
    global colors
    colors = [p.Color("gray"), p.Color("dark gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE))

def highlightSquares(screen, board, positions, moves):
    viable = []
    if len(positions) == 1:
        x = positions[0][0]
        y = positions[0][1]
        p.draw.rect(screen, p.Color("red"), p.Rect(y * SQUARE, x * SQUARE, SQUARE, SQUARE), 3)
        for move in moves:
            if (move.startR, move.startC) == (x, y):
                viable.append((move.endR, move.endC))
        for (r, c) in viable:
            p.draw.circle(screen, p.Color("red"), (c * SQUARE + SQUARE // 2, r * SQUARE + SQUARE // 2), SQUARE // 6)

def moveAnimation(move, screen, board, clock):
    global colors
    coordinates = []
    dR = move.endR - move.startR
    dC = move.endC - move.startC
    FPS = 10
    frameCount = (abs(dR) + abs(dC))*FPS
    for frame in range(frameCount + 1):
        x, y = (move.startR + dR*frame/frameCount, move.startC + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endR + move.endC) % 2]
        endSquare = p.Rect(move.endC * SQUARE, move.endR*SQUARE, SQUARE, SQUARE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(y*SQUARE, x*SQUARE, SQUARE, SQUARE))
        p.display.flip()
        clock.tick(60)


def playingvsBot():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    load_img()
    state = GameState()
    validMoves = state.getValidMoves()
    moveMade = False
    running = True
    sqSelected = ()
    positions = []
    animate = False
    bot = RandomBot  # bot takes the type of AI you'll play against, for now only RandomBot is available
    while running:
        if state.whiteMoves:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                        position = p.mouse.get_pos()
                        col = position[0]//SQUARE
                        row = position[1]//SQUARE
                        if sqSelected == (row, col):
                            sqSelected = ()
                            positions = []
                        else:
                            sqSelected = (row, col)
                            positions.append(sqSelected)
                        if len(positions) == 2:
                            move = Move(positions[0], positions[1], state.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    state.makeMove(move)
                                    moveMade = True
                                    sqSelected = ()
                                    positions = []
                                    animate = True
                            if not moveMade:
                                positions = []
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_u:  # undo move when key "U" is pressed
                        state.undoMove()
                        moveMade = True
                        animate = False
                    if e.key == p.K_r:  # reset game when key "R" is pressed
                        state = GameState()
                        validMoves = state.getValidMoves()
                        sqSelected = ()
                        positions = []
                        animate = False
                        moveMade = False
        else:
            index = bot(validMoves)
            state.makeMove(validMoves[index])
            moveMade = True
        if moveMade:
            if animate:
                moveAnimation(state.moveLog[-1], screen, state.board, clock)
            validMoves = state.getValidMoves()
            moveMade = False
        drawGameState(screen, state, positions, validMoves)
        clock.tick(MAX_FPS)
        p.display.flip()


main()
