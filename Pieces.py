import pygame

class Piece:
    def __init__(self, color, position):
        self.color = color
        self.pos = position
            
    def move(self, finalPos):
        self.pos = finalPos


class King(Piece):
    def __init__(self, color):
        if color == 'w':
            r = 7
        else:
            r = 0
        Piece.__init__(self, color, [r, 4])
        self.symbol = pygame.image.load("Pieces/King{}.bmp".format(color))
        self.symbol.set_colorkey((255,0,255)) #Make pink transparent
    
    def getValidMoves(self, board): #Bruk denne før et flytt
        list = []
        for r in range (self.pos[0]-1, self.pos[0]+2):
            for c in range (self.pos[1]-1, self.pos[1]+2):
                if (r == self.pos[0] and c == self.pos[1]):
                    continue
                elif not board.posOutOfBounds([r,c]):
                    if board.pieces[r][c] != None:
                        if (board.pieces[r][c].color != self.color):
                            list.append([r,c])
                    else:
                        list.append([r,c])
        return list
        


class Pawn(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        self.symbol = pygame.image.load("Pieces/Pawn{}.bmp".format(self.color))
        self.symbol.set_colorkey((255,0,255))
        self.firstMove = True
        
    def getValidMoves(self, board):
        list = []
        r_dir = 0
        if self.color == 'b':
            r_dir = 1
        else:
            r_dir = -1


        nearest = board.searchDirection(self, [r_dir,0]) 
        nearestPiece = nearest[0]
        nearestPos = nearest[1]
        r1 = self.pos[0]
        c1 = self.pos[1]
        r2 = nearestPos[0]
        c2 = nearestPos[1]
        if (abs(r2-r1) > 1): #If no piece is blocking, here there is a weird error, kan ikke flytte til enden av brettet, hvis ja, så kan han også slå ut forover
            list.append([self.pos[0]+r_dir, self.pos[1]])
            if self.firstMove and (abs(r2-r1) > 2):
                list.append([self.pos[0]+2*r_dir, self.pos[1]])
        if board.posOutOfBounds([r1 + 2*r_dir, c1]): #ad hoc dårlig løsning som resulterer i at du kan slå ut deg selv på enden, men du skal bli dronning læll
            list.append([r2,c2])
        if not (board.posOutOfBounds([r1+r_dir,c1+1])) and board.pieces[r1+r_dir][c1+1] != None: #Check if a piece can be captured
            if board.pieces[r1+r_dir][c1+1].color != self.color:
                list.append([r1+r_dir,c1+1])
        if not (board.posOutOfBounds([r1+r_dir,c1-1])) and board.pieces[r1+r_dir][c1-1] != None: #The other side
            if board.pieces[r1+r_dir][c1-1].color != self.color:
                list.append([r1+r_dir,c1-1])
        return list
    
    def move(self, finalPos):
        Piece.move(self, finalPos)
        self.firstMove = False


class Rook(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        self.symbol = pygame.image.load("Pieces/Rook{}.bmp".format(color))
        self.symbol.set_colorkey((255,0,255)) #Make pink transparent
    
    def getValidMoves(self, board): #Bruk denne før et flytt
        list = []
        nearestRight =  board.searchDirection(self, [0, 1])
        nearestLeft =   board.searchDirection(self, [0, -1])
        nearestUp =     board.searchDirection(self, [-1, 0])
        nearestDown =   board.searchDirection(self, [1, 0])
        
        nearestPieces = [nearestRight[0], nearestLeft[0], nearestUp[0], nearestDown[0]]
        nearestPoses = [nearestRight[1], nearestLeft[1], nearestUp[1], nearestDown[1]]        
        
        #up:
        for r in range(nearestPoses[2][0], self.pos[0]):
            list.append([r, self.pos[1]])
        #left:
        for c in range(nearestPoses[1][1], self.pos[1]):
            list.append([self.pos[0], c])
        #right:
        for c in range(self.pos[1]+1, nearestPoses[0][1]+1):
            list.append([self.pos[0], c])
        #down:
        for r in range(self.pos[0]+1, nearestPoses[3][0]+1):
            list.append([r, self.pos[1]])
        
        remove = []
        for i in list:
            p = board.pieces[i[0]][i[1]]
            if p != None:
                if p.color == self.color:
                    remove.append(i)
        for i in remove:
            list.remove(i)        
        return list

        
        
class Knight(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        self.symbol = pygame.image.load("Pieces/Knight{}.bmp".format(self.color))
        self.symbol.set_colorkey((255,0,255))
        self.firstMove = True
        
    def getValidMoves(self, board):
        list = []
        
        list.append([self.pos[0] + 1, self.pos[1] + 2])
        list.append([self.pos[0] + 1, self.pos[1] - 2])
        list.append([self.pos[0] - 1, self.pos[1] + 2])
        list.append([self.pos[0] - 1, self.pos[1] - 2])
        list.append([self.pos[0] + 2, self.pos[1] + 1])
        list.append([self.pos[0] + 2, self.pos[1] - 1])
        list.append([self.pos[0] - 2, self.pos[1] + 1])
        list.append([self.pos[0] - 2, self.pos[1] - 1])        
        
        remove = []
        for i in list:
            if board.posOutOfBounds(i):
                remove.append(i)
            else:
                p = board.pieces[i[0]][i[1]]
                if p != None:
                    if p.color == self.color:
                        remove.append(i)
        for i in remove:
            list.remove(i)        
        return list
        
        
            
class Bishop(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        self.symbol = pygame.image.load("Pieces/Bishop{}.bmp".format(color))
        self.symbol.set_colorkey((255,0,255)) #Make pink transparent
    
    def getValidMoves(self, board): #Bruk denne før et flytt
        list = []
        nearestRight =  board.searchDirection(self, [0, 1])
        nearestLeft =   board.searchDirection(self, [0, -1])
        nearestUp =     board.searchDirection(self, [-1, 0])
        nearestDown =   board.searchDirection(self, [1, 0])
        
        return list
        
        
"""        
class Queen(Piece):
    def __init__(self):

"""    
