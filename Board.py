import pygame
from copy import deepcopy
from Pieces import King , Pawn, Rook, Knight, Bishop, Queen

white, black = (255, 255, 255), (0, 0, 0)

dot = pygame.image.load("Pieces/klyse75x75.bmp")
dot.set_colorkey((255,0,255))

class Square:
    def __init__(self, row, col, color, size):
        self.row = row
        self.col = col
        self.color = color
        self.pygameSquare = pygame.Rect(col*size, row*size, size, size)

class Board:
    def __init__(self, squareSize):
        self.squareSize = squareSize
        self.pieces = []
        self.board = []

        j, k, color = 0, 0, 0
        for r in range (0,8):
            self.board.append([])
            self.pieces.append([])
            for c in range (0,8):
                if (j+k) % 2 == 0:
                    color = white
                else:
                    color = black
                self.board[r].append(Square(r,c,color,squareSize))
                self.pieces[r].append(None)
                k += 1
            j += 1
             
    def draw(self, screen):
        #Fill in with "None", for the reset button. if you remove this part, things become interesting
        #for i in range (0, 8):
        #    for j in range (0, 8):
        #        if self.pieces[i][j] != None:
        #            del self.pieces[i][j]
        #            self.pieces[i][j] = None
        
        self.pieces[0][0] = Rook('b', [0,0])
        self.pieces[0][1] = Knight('b', [0, 1])
        self.pieces[0][2] = Bishop('b', [0,2])
        self.pieces[0][3] = Queen('b')
        self.pieces[0][4] = King('b')
        self.pieces[0][5] = Bishop('b', [0,5])
        self.pieces[0][6] = Knight('b', [0,6])
        self.pieces[0][7] = Rook('b', [0,7])
        self.pieces[1][0] = Pawn('b', [1,0])
        self.pieces[1][1] = Pawn('b', [1,1])
        self.pieces[1][2] = Pawn('b', [1,2])
        self.pieces[1][3] = Pawn('b', [1,3])
        self.pieces[1][4] = Pawn('b', [1,4])
        self.pieces[1][5] = Pawn('b', [1,5])
        self.pieces[1][6] = Pawn('b', [1,6])
        self.pieces[1][7] = Pawn('b', [1,7])
        self.pieces[7][0] = Rook('w', [7,0])
        self.pieces[7][1] = Knight('w', [7,1])
        self.pieces[7][2] = Bishop('w', [7,2])
        self.pieces[7][3] = Queen('w')
        self.pieces[7][4] = King('w')
        self.pieces[7][5] = Bishop('w', [7,5])
        self.pieces[7][6] = Knight('w', [7,6])
        self.pieces[7][7] = Rook('w', [7,7])
        self.pieces[6][0] = Pawn('w', [6,0])
        self.pieces[6][1] = Pawn('w', [6,1])
        self.pieces[6][2] = Pawn('w', [6,2])
        self.pieces[6][3] = Pawn('w', [6,3])
        self.pieces[6][4] = Pawn('w', [6,4])
        self.pieces[6][5] = Pawn('w', [6,5])
        self.pieces[6][6] = Pawn('w', [6,6])
        self.pieces[6][7] = Pawn('w', [6,7])        
        
        
        for r in self.board: #Draw board
            for s in r:
                screen.fill(s.color, s.pygameSquare)
        
        for c in self.pieces: #Fill in pieces
            for p in c:
                if p != None:
                    screen.blit(p.symbol, (self.squareSize*c.index(p), self.squareSize*self.pieces.index(c)))
        
    def update(self, screen):
        for r in self.board: #Draw board
            for s in r:
                screen.fill(s.color, s.pygameSquare)
        
        for c in self.pieces: #Fill in pieces
            for p in c:
                if p != None:
                    screen.blit(p.symbol, (self.squareSize*c.index(p), self.squareSize*self.pieces.index(c)))
    
    def posOutOfBounds(self, pos):
        return (pos[0] < 0) or (pos[0] > 7) or (pos[1] < 0) or (pos[1] > 7)
    
    def searchDirection(self, piece, direction): #direction is [1,1], [1,0], [0,1] ... [-1,-1]
        r = piece.pos[0]
        c = piece.pos[1]
        searchPiece = None
        searchPos = [r, c]
        while (searchPiece == None):
            nextPos = [a + b for a, b in zip(searchPos, direction)] #Elementwise addition
            if not self.posOutOfBounds(nextPos):
                searchPos = nextPos
            else:
                break
            searchPiece = self.pieces[searchPos[0]][searchPos[1]]
        return [searchPiece, searchPos]

    def highlightValidMoves(self, piece, screen):
        for pos in piece.getValidMoves(self):
            screen.blit(dot, (pos[1]*self.squareSize, pos[0]*self.squareSize))

    def movePiece(self, piece, initPos, finalPos):
        #Aupassau
        if type(piece) == Pawn and self.pieces[finalPos[0]][finalPos[1]] == None:
            if piece.color == 'w':
                otherPiece = self.pieces[finalPos[0]+1][finalPos[1]]
                if type(otherPiece) == Pawn:
                    if otherPiece.aupassauAvail:
                        self.pieces[finalPos[0]+1][finalPos[1]] = None
            else:
                otherPiece = self.pieces[finalPos[0]-1][finalPos[1]]
                if type(otherPiece) == Pawn:
                    if otherPiece.aupassauAvail:
                        self.pieces[finalPos[0]-1][finalPos[1]] = None
        #Disable aupassau on all other pieces
        for r in self.pieces:
            for p in r:
                if type(p) == Pawn and p != piece:
                    p.aupassauAvail = False
        
        #Castling
        if type(piece) == King and abs(finalPos[1] - initPos[1]) > 1:
            #Right
            if finalPos[1] - initPos[1] > 0:
                rook = self.pieces[piece.pos[0]][7]
                rook.move([piece.pos[0],5])
                self.pieces[piece.pos[0]][5] = rook
                self.pieces[piece.pos[0]][7] = None
            #Left
            else:
                rook = self.pieces[piece.pos[0]][0]
                rook.move([piece.pos[0],3])
                self.pieces[piece.pos[0]][3] = rook
                self.pieces[piece.pos[0]][0] = None
        
        
        takenPiece = self.pieces[finalPos[0]][finalPos[1]]
        self.pieces[finalPos[0]][finalPos[1]] = piece
        self.pieces[initPos[0]][initPos[1]] = None
        piece.move(finalPos)
        
        #Promotion
        if type(piece) == Pawn and (piece.pos[0] == 0 or piece.pos[0] == 7):
            q = Queen(piece.color)
            self.pieces[finalPos[0]][finalPos[1]] = q
            q.move(finalPos)
        return takenPiece
   
    def getAllPieces(self, color):
        list = []
        for r in self.pieces:
            for p in r:
                if p != None:
                    if p.color == color:
                        list.append(p)
        return list
    
    def getAllMoves(self, color):
        list = []
        for r in self.pieces:
            for p in r:
                if p != None:
                    if p.color == color:
                        moveList = p.getValidMoves(self)
                        for x in moveList:
                            list.append(x)
        return list

    def getKing(self, color):
        for r in self.pieces:
            for king in r:
                if (type(king) == King):
                    if (king.color == color):
                        return king
        
    def inCheck(self, color):
        king = self.getKing(color)
        if (color == 'w'):
            enemyColor = 'b'
        else:
            enemyColor = 'w'
        if king.pos in self.getAllMoves(enemyColor):
            return True
        else:
            return False

    def inCheckMate(self, color):
        if self.inCheck(color):
            #Create deep copy of self.pieces
            for r in self.pieces:
                for p in r:
                    if p != None:
                        if p.color == color:
                            moves = p.getValidMoves(self)
                            #Try all these moves and see if not inCheck()
                            for finalPos in moves:
                                initPos = p.pos
                                takenPiece = self.movePiece(p, initPos, finalPos)
                                if not self.inCheck(color):
                                    self.movePiece(p, finalPos, initPos)
                                    if takenPiece != None:
                                        self.pieces[finalPos[0]][finalPos[1]] = takenPiece
                                    return False
                                else:
                                    self.movePiece(p, finalPos, initPos)
                                    if takenPiece != None:
                                        self.pieces[finalPos[0]][finalPos[1]] = takenPiece

            print("Check Mate! {} has lost!".format(color))
            return True
        else:
            return False

        
        
