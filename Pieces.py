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
        self.value = 99
        self.symbol = pygame.image.load("Pieces/King{}.bmp".format(color))
        self.symbol.set_colorkey((255,0,255)) #Make pink transparent
        self.hasMoved = False
    
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
        
        #Castling
        #Right
        r = board.searchDirection(self, [0, 1])[0]
        if type(r) == Rook:
            if (not self.hasMoved) and (not r.hasMoved):
                list.append([self.pos[0], self.pos[1]+2])
        #Left
        l = board.searchDirection(self, [0, -1])[0]
        if type(l) == Rook:
            if (not self.hasMoved) and (not l.hasMoved):
                list.append([self.pos[0], self.pos[1]-2])

        return list

    def getValidMovesInclCheck(self, board):
        list = self.getValidMoves(board)

        #Remove moves that put you in check
        remove = []
        resetParameters = not self.hasMoved
        initPos = self.pos
        for finalPos in list:
            takenPiece = board.movePiece(self, initPos, finalPos)
            if board.inCheck(self.color):
                remove.append(finalPos)
            board.movePiece(self, finalPos, initPos)
            if resetParameters:
                self.hasMoved = False
            if takenPiece != None:
                board.pieces[takenPiece.pos[0]][takenPiece.pos[1]] = takenPiece
                #FIXME: Må fikses her
            
        for i in remove:
            list.remove(i)
            
        return list

    def move(self, finalPos):
        Piece.move(self, finalPos)
        self.hasMoved = True

        


class Pawn(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        self.value = 1
        self.symbol = pygame.image.load("Pieces/Pawn{}.bmp".format(self.color))
        self.symbol.set_colorkey((255,0,255))
        self.aupassauAvail = False
        
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
            if (self.color == 'w' and self.pos[0] == 6) or (self.color == 'b' and self.pos[0] == 1):
                firstMove = True
            else:
                firstMove = False            
            if firstMove and (abs(r2-r1) > 2):
                list.append([self.pos[0]+2*r_dir, self.pos[1]])
        if board.posOutOfBounds([r1 + 2*r_dir, c1]): #ad hoc dårlig løsning som resulterer i at du kan slå ut deg selv på enden, men du skal bli dronning læll
            list.append([r2,c2])
        if not (board.posOutOfBounds([r1+r_dir,c1+1])) and board.pieces[r1+r_dir][c1+1] != None: #Check if a piece can be captured
            if board.pieces[r1+r_dir][c1+1].color != self.color:
                list.append([r1+r_dir,c1+1])
        if not (board.posOutOfBounds([r1+r_dir,c1-1])) and board.pieces[r1+r_dir][c1-1] != None: #The other side
            if board.pieces[r1+r_dir][c1-1].color != self.color:
                list.append([r1+r_dir,c1-1])
        
        #Aupassau
        #Left
        if not board.posOutOfBounds([r1, c1-1]):
            p = board.pieces[r1][c1-1]
            if p != None:
                if type(p) == Pawn:
                    if p.aupassauAvail:
                        list.append([r1 + r_dir,c1-1])        
        #Right
        if not board.posOutOfBounds([r1, c1+1]):
            p = board.pieces[r1][c1+1]
            if p != None:
                if type(p) == Pawn:
                    if p.aupassauAvail:
                        list.append([r1 + r_dir,c1+1])
        
        return list

    def getValidMovesInclCheck(self, board):
        list = self.getValidMoves(board)

        #Remove moves that put you in check
        remove = []
        initPos = self.pos
        for finalPos in list:
            takenPiece = board.movePiece(self, initPos, finalPos)
            if board.inCheck(self.color):
                remove.append(finalPos)
            board.movePiece(self, finalPos, initPos)
            if takenPiece != None:
                board.pieces[takenPiece.pos[0]][takenPiece.pos[1]] = takenPiece
                #FIXME: Må fikses her
            
        for i in remove:
            list.remove(i)
            
        return list
    
    def move(self, finalPos):
        if (abs(finalPos[0] - self.pos[0]) > 1):
            self.aupassauAvail = True
        else:
            self.aupassauAvail = False
        Piece.move(self, finalPos)
        self.firstMove = False


class Rook(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        self.value = 5
        self.symbol = pygame.image.load("Pieces/Rook{}.bmp".format(color))
        self.symbol.set_colorkey((255,0,255))
        self.hasMoved = False
    
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

    def getValidMovesInclCheck(self, board):
        list = self.getValidMoves(board)

        #Remove moves that put you in check
        remove = []
        initPos = self.pos
        for finalPos in list:
            takenPiece = board.movePiece(self, initPos, finalPos)
            if board.inCheck(self.color):
                remove.append(finalPos)
            board.movePiece(self, finalPos, initPos)
            if takenPiece != None:
                board.pieces[takenPiece.pos[0]][takenPiece.pos[1]] = takenPiece
                #FIXME: Må fikses her
            
        for i in remove:
            list.remove(i)
            
        return list

    def move(self, finalPos):
        Piece.move(self, finalPos)
        self.hasMoved = True
        
        
class Knight(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        self.value = 3
        self.symbol = pygame.image.load("Pieces/Knight{}.bmp".format(self.color))
        self.symbol.set_colorkey((255,0,255))
        
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
        
    def getValidMovesInclCheck(self, board):
        list = self.getValidMoves(board)

        #Remove moves that put you in check
        remove = []
        initPos = self.pos
        for finalPos in list:
            takenPiece = board.movePiece(self, initPos, finalPos)
            if board.inCheck(self.color):
                remove.append(finalPos)
            board.movePiece(self, finalPos, initPos)
            if takenPiece != None:
                board.pieces[takenPiece.pos[0]][takenPiece.pos[1]] = takenPiece
                #FIXME: Må fikses her
            
        for i in remove:
            list.remove(i)
            
        return list
        
            
class Bishop(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        self.value = 3
        self.symbol = pygame.image.load("Pieces/Bishop{}.bmp".format(color))
        self.symbol.set_colorkey((255,0,255)) #Make pink transparent
    
    def getValidMoves(self, board): #Bruk denne før et flytt
        list = []
        nearestUR =  board.searchDirection(self, [-1, 1])
        nearestUL =   board.searchDirection(self, [-1, -1])
        nearestDR =     board.searchDirection(self, [1, 1])
        nearestDL =   board.searchDirection(self, [1, -1])
        
        nearestPieces = [nearestUR[0], nearestUL[0], nearestDR[0], nearestDL[0]]
        nearestPoses = [nearestUR[1], nearestUL[1], nearestDR[1], nearestDL[1]]

        #Up right:
        for r in range (nearestPoses[0][0], self.pos[0]+1):
            c = self.pos[1] + (self.pos[0] - r)
            list.append([r, c])
        #Up left:
        for r in range (nearestPoses[1][0], self.pos[0]+1):
            c = self.pos[1] - (self.pos[0] - r)
            list.append([r, c])        
        #Down right:
        for r in range (self.pos[0], nearestPoses[2][0]+1):
            c = self.pos[1] + (r - self.pos[0])
            list.append([r, c])
        #Down left:
        for r in range (self.pos[0], nearestPoses[3][0]+1):
            c = self.pos[1] - (r - self.pos[0])
            list.append([r, c])
            
        remove = []
        for i in list:
            p = board.pieces[i[0]][i[1]]
            if p != None:
                if p.color == self.color:
                    remove.append(i)
        for i in remove:
            list.remove(i)        
        return list

    def getValidMovesInclCheck(self, board):
        list = self.getValidMoves(board)

        #Remove moves that put you in check
        remove = []
        initPos = self.pos
        for finalPos in list:
            takenPiece = board.movePiece(self, initPos, finalPos)
            if board.inCheck(self.color):
                remove.append(finalPos)
            board.movePiece(self, finalPos, initPos)
            if takenPiece != None:
                board.pieces[takenPiece.pos[0]][takenPiece.pos[1]] = takenPiece
                #FIXME: Må fikses her
            
        for i in remove:
            list.remove(i)
            
        return list

        
class Queen(Piece):
    def __init__(self, color):
        if color == 'w':
            r = 7
        else:
            r = 0
        Piece.__init__(self, color, [r, 3])
        self.value = 10
        self.symbol = pygame.image.load("Pieces/Queen{}.bmp".format(color))
        self.symbol.set_colorkey((255,0,255))

    def getValidMoves(self, board):
        rookMoves = Rook(self.color, self.pos).getValidMoves(board)
        bishopMoves = Bishop(self.color, self.pos).getValidMoves(board)
        
        list = rookMoves
        for m in bishopMoves:
            list.append(m)
        return list

    def getValidMovesInclCheck(self, board):
        list = self.getValidMoves(board)

        #Remove moves that put you in check
        remove = []
        initPos = self.pos
        for finalPos in list:
            takenPiece = board.movePiece(self, initPos, finalPos)
            if board.inCheck(self.color):
                remove.append(finalPos)
            board.movePiece(self, finalPos, initPos)
            if takenPiece != None:
                board.pieces[takenPiece.pos[0]][takenPiece.pos[1]] = takenPiece
                #FIXME: Må fikses her
            
        for i in remove:
            list.remove(i)
            
        return list

    