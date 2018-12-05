import pygame
from Pieces import King, Rook
import Animation

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
            #print("({}, {})".format(cord[0], cord[1]))
            
        else:                   #Move highlighted piece
            self.movePiece(board = board, pos = pos, screen = screen)
    
    def movePiece(self, board, screen, pos = None, finalPos = None):
        self.moveMode = False
        if finalPos == None:
            finalPos = self.getCoord(board, pos)
        initPos = self.movingPiece.pos
        resetParameters = False
        if type(self.movingPiece) == King or type(self.movingPiece) == Rook:
            if not self.movingPiece.hasMoved:
                resetParameters = True

        if (finalPos in self.movingPiece.getValidMovesInclCheck(board)):
            #Before update, check if last mover is in check, if he is, then don't do the move and give a message
            takenPiece = board.movePiece(self.movingPiece, initPos, finalPos)
            if board.inCheck(self.turn):
                board.movePiece(self.movingPiece, finalPos, initPos)
                if resetParameters:
                    self.movingPiece.hasMoved = False
                if takenPiece != None:
                    board.pieces[takenPiece.pos[0]][takenPiece.pos[1]] = takenPiece
                print("In check!")
            else:
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
            
        #If a button is pressed
        """if self.resetButton.collidepoint(pos):
            print("Reset button pressed")
            board.draw(screen)
        """



    def drawButtons(self, screen, squareSize):
        self.resetButton = pygame.Rect(squareSize, 8.5*squareSize, 2*squareSize, squareSize)
        screen.fill((255,0,0), self.resetButton)
