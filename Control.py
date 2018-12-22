import pygame
from Pieces import King, Rook
import Animation
import time

class Control:
    def __init__(self, squareSize):
        self.moveMode = False
        self.movingPiece = None
        self.squareSize = squareSize
        self.turn = 'w'

    def getCoord(self, board, pos):
        for r in range (0,8):
            for c in range (0,8):
                if board.board[r][c].pygameSquare.collidepoint(pos):
                    return [r, c]
        return [-1, -1]

    def mouseClick(self, board, pos, screen):
        if (not self.moveMode): #Highlight piece
            cord = self.getCoord(board, pos)
            if not board.posOutOfBounds(cord):
                piece = board.pieces[cord[0]][cord[1]]
                if (piece != None):
                    if (piece.color == self.turn):
                        self.movingPiece = board.pieces[cord[0]][cord[1]]
                        if (self.movingPiece != None):
                            self.moveMode = True
                            board.highlightValidMoves(self.movingPiece, screen)

        else:                   #Move highlighted piece
            self.performMove(board = board, pos = pos, screen = screen)
    
    def performMove(self, board, screen, pos = None, finalPos = None):
        self.moveMode = False
        if finalPos == None:
            finalPos = self.getCoord(board, pos)
        initPos = self.movingPiece.pos

        if (finalPos in self.movingPiece.getValidMovesInclCheck(board)):
            board.movePiece(self.movingPiece, initPos, finalPos)
            if (self.turn == 'w'):
                self.turn = 'b'
            else:
                self.turn = 'w'
        Animation.movePieceAnimation(board, screen, self.squareSize, self.movingPiece, initPos, finalPos)
        board.update(screen)
        self.movingPiece = None
        if board.inCheckMate(self.turn):
            pygame.font.init()
            myfont = pygame.font.SysFont('Comic Sans MS', 110)
            textsurface = myfont.render('Tjakk matt', False, (0, 155, 0))
            screen.blit(textsurface,(0,3*self.squareSize))
            #time.sleep(1000)
            
            


    #def drawButtons(self, screen, squareSize):
    #    self.resetButton = pygame.Rect(squareSize, 8.5*squareSize, 2*squareSize, squareSize)
    #    screen.fill((255,0,0), self.resetButton)
