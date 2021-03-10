import pygame as p
from ChessEngine import *

DIMENSION = 8
WIDTH = HEIGHT = 512
SQUARE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
PIECES = ['wP', 'wK', 'wQ', 'wB', 'wR', 'wN', 'bP', 'bK', 'bQ', 'bB', 'bR', 'bN']


def load_img():
    for piece in PIECES:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"), (SQUARE, SQUARE))


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
                    # if len(positions) == 0 and (state.board[row][col][0] == 'w' and state.whiteMoves) or (state.board[row][col][0] == 'b' and not state.whiteMoves):
                    positions.append(sqSelected)
                if len(positions) == 2:
                    move = Move(positions[0], positions[1], state.board)
                    print(move.getNotation())
                    if move in validMoves:
                        state.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        positions = []
                    else:
                        positions = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_r:
                    state.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = state.getValidMoves()
            moveMade = False
        drawGameState(screen, state, positions, validMoves)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, state, positions, moves):
    drawBoard(screen)
    drawPieces(screen, state.board, positions, moves)

def drawBoard(screen):
    colors = [p.Color("gray"), p.Color("dark gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE))

def drawPieces(screen, board, positions, moves):
    viable = []
    if len(positions) == 1:
        x = positions[0][0]
        y = positions[0][1]
        p.draw.rect(screen, p.Color("red"), p.Rect(y * SQUARE, x * SQUARE, SQUARE, SQUARE), 3)
        for move in moves:
            if (move.startR, move.startC) == (x, y):
                viable.append((move.endR, move.endC))
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE))
            if (r, c) in viable:
                p.draw.circle(screen, p.Color("red"), (c * SQUARE + SQUARE // 2, r * SQUARE + SQUARE // 2), SQUARE // 6)


if __name__ == '__main__':
    main()