import pygame
import time
import random
from Board import Board
from Pieces import Piece
from math import sin, floor


def movePieceAnimation(board, screen, squareSize, piece, initPos, finalPos):    
    if not board.inCheck(piece.color):
        res = 100
        speed = random.randint(9,10)
        x = initPos[0]*squareSize
        y = initPos[1]*squareSize
        r_final = finalPos[0]*squareSize
        c_final = finalPos[1]*squareSize
        x_step = (r_final-x)/res
        y_step = (c_final-y)/res

        for p in range (0, res):
            resetBoardExceptPiece(piece, board, screen, squareSize)
            screen.blit(piece.symbol, (y, x))
            pygame.display.flip()
            x += x_step
            y += y_step
            if p == floor(res - res/10):
                speed = speed / 4
            time.sleep(1/(speed*res))

def resetBoardExceptPiece(piece, board, screen, squareSize):
    #Draw board without this piece
    for r in board.board: #Draw board
        for s in r:
            screen.fill(s.color, s.pygameSquare)
    for c in board.pieces: #Fill in pieces and not movingPiece
        for p in c:
            if p != None:
                if p != piece:
                    screen.blit(p.symbol, (squareSize*c.index(p), squareSize*board.pieces.index(c)))
