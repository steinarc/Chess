import pygame
from Pieces import King , Pawn, Rook, Knight, Bishop

white, black = (255, 255, 255), (0, 0, 0)

dot = pygame.image.load("Pieces/dot.bmp")
dot.set_colorkey((255,0,255))

class Square:
    def __init__(self, row, col, color, size):
        self.row = row
        self.col = col
        self.color = color
        self.pygameSquare = pygame.Rect(col*50, row*50, size, size)

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
        self.pieces[0][0] = Rook('b', [0,0])
        self.pieces[0][1] = Knight('b', [0, 1])
        self.pieces[0][2] = Bishop('b', [0,2])
        #self.pieces[0][3] = Queen('b')
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
        #self.pieces[0][3] = Queen('w')
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
            screen.blit(dot, (pos[1]*50, pos[0]*50))

    def movePiece(self, piece, initPos, finalPos):
        self.pieces[finalPos[0]][finalPos[1]] = piece
        self.pieces[initPos[0]][initPos[1]] = None
        piece.move(finalPos)

    def inCheck(self, color):
        kingPos = None
        for r in self.pieces:
            for king in r:
                if (type(king) == King):
                    if (king.color == color):
                        for r2 in self.pieces:
                            for p2 in r2:
                                if p2 != None:
                                    if king.pos in p2.getValidMoves(self):
                                        return True
         
        return False

