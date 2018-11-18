from Board import Board
from Control import Control
import random    
import time

class AI_Player:
    def __init__(self, color):
        self.color = color
    
    def moveRand(self, board, screen, control):
        pieces = board.getAllPieces(self.color)
        p = random.randint(0, len(pieces)-1)
        while (len(pieces[p].getValidMoves(board)) == 0):
            p = random.randint(0, len(pieces)-1)
        piece = pieces[p]
        m = random.randint(0, len(piece.getValidMoves(board))-1)
        move = piece.getValidMoves(board)[m]
        control.movingPiece = piece
        #time.sleep(0.1)
        control.movePiece(board = board, screen = screen, finalPos = move)
    
    def moveRandPrioritizeCapture(self, board, screen, control):
        pieces = board.getAllPieces(self.color)
        for p in pieces:
            if p.color == self.color:
                #Find if this piece has a move that captures
                moves = p.getValidMoves(board)
                for m in moves:
                    for r in board.pieces:
                        for p2 in r:
                            if p2 != None:
                                if p2.pos == m and p2.color != self.color:
                                    control.movingPiece = p
                                    control.movePiece(board = board, screen = screen, finalPos = m)
                                    return
        self.moveRand(board, screen, control)
        
    def moveRandPrioritizeCaptureUsingVal(self, board, screen, control):
        pieces = board.getAllPieces(self.color)
        for p in pieces:
            if p.color == self.color:
                #Find if this piece has a move that captures
                moves = p.getValidMoves(board)
                for m in moves:
                    for r in board.pieces:
                        for p2 in r:
                            if p2 != None:
                                if p2.pos == m and p2.color != self.color and p2.value >= p.value:
                                    control.movingPiece = p
                                    control.movePiece(board = board, screen = screen, finalPos = m)
                                    return
        self.moveRand(board, screen, control)
        
        
        