from Board import Board
from Control import Control
import random    
import time

class AI_Player:
    def __init__(self, color):
        self.color = color
        if (self.color == 'w'):
            self.enemyColor = 'b'
        else:
            self.enemyColor = 'w'
    
    def moveRand(self, board, screen, control):
        pieces = board.getAllPieces(self.color)
        p = random.randint(0, len(pieces)-1)
        while (len(pieces[p].getValidMovesInclCheck(board)) == 0):
            p = random.randint(0, len(pieces)-1)
        piece = pieces[p]
        m = random.randint(0, len(piece.getValidMovesInclCheck(board))-1)
        move = piece.getValidMovesInclCheck(board)[m]
        control.movingPiece = piece
        #time.sleep(0.1)
        control.performMove(board = board, screen = screen, finalPos = move)

    def moveRandPrioritizeCapture(self, board, screen, control):
        pieces = board.getAllPieces(self.color)
        for p in pieces:
            if p.color == self.color:
                #Find if this piece has a move that captures
                moves = p.getValidMovesInclCheck(board)
                for m in moves:
                    for r in board.pieces:
                        for p2 in r:
                            if p2 != None:
                                if p2.pos == m and p2.color != self.color:
                                    control.movingPiece = p
                                    control.performMove(board = board, screen = screen, finalPos = m)
                                    return
        self.moveRand(board, screen, control)
        
    def moveRandPrioritizeCaptureUsingVal(self, board, screen, control):
        pieces = board.getAllPieces(self.color)
        for p in pieces:
            if p.color == self.color:
                #Find if this piece has a move that captures
                moves = p.getValidMovesInclCheck(board)
                for m in moves:
                    for r in board.pieces:
                        for p2 in r:
                            if p2 != None:
                                if p2.pos == m and p2.color != self.color and p2.value >= p.value:
                                    control.movingPiece = p
                                    control.performMove(board = board, screen = screen, finalPos = m)
                                    return
        self.moveRand(board, screen, control)
        
    def moveRandEvaluateIfCapturedOnNewPosUsingVal(self, board, screen, control): #Denne tenker fortsatt ikke på at de tilfeldige flyttene bør unngå at du blir tatt
        pieces = board.getAllPieces(self.color)
        for p in pieces: #Sjekk alle dine brikker
            initPos = p.pos
            if p.color == self.color:
                #Find if this piece has a move that captures
                moves = p.getValidMovesInclCheck(board)
                for m in moves: #move m in this pieces moves
                    for r in board.pieces: #check all rows in board
                        for p2 in r: #for "secondary" pieces in the board
                            if p2 != None:
                                if p2.pos == m and p2.color != self.color: #If m is a capturing move, aupassau not included
                                    #It should only be performed after evaluating the value of the piece you capture and check if you get captured afterwards
                                    myVal = p.value
                                    hisVal = p2.value
                                    
                                    #perform a test move. Really, in this case resetParameters should be done for Rook and King
                                    takenPiece = board.movePiece(p, p.pos, m)
                                    reward = hisVal
                                    if (m in board.getAllMovesInclCheck(self.enemyColor)):
                                        reward = reward - myVal
                                    
                                    board.movePiece(p, p.pos, initPos)
                                    board.pieces[takenPiece.pos[0]][takenPiece.pos[1]] = takenPiece
                                    
                                    if reward >= 0:
                                        control.movingPiece = p
                                        control.performMove(board = board, screen = screen, finalPos = m)
                                        return
                        
        self.moveRand(board, screen, control)

    def smartMove(self, board, screen, control):
        pieces = board.getAllPieces(self.color) 

        #moveList is an array where each element is one of these structures
        #[piece, move, reward]
        #[Queen, [4,4], -3]
        
        moveList = []

        for p in pieces: #Sjekk alle dine brikker
            initPos = p.pos
            if p.color == self.color:
                #Find if this piece has a move that captures
                moves = p.getValidMovesInclCheck(board)
                for m in moves:
                    reward = self.calcReward(p, m, board)
                    moveList.append([p, m, reward])
        

        #Get a random move of the ones with the best reward
        if len(moveList) == 0:
            return
        bestMoveReward = moveList[0][2]
        for moveObject in moveList:
            if moveObject[2] > bestMoveReward:
                bestMoveReward = moveObject[2]
        bestMoves = []
        for moveObject in moveList:
            if moveObject[2] == bestMoveReward:
                bestMoves.append(moveObject)
        
        r = random.randint(0, len(bestMoves)-1)
        
        control.movingPiece = bestMoves[r][0]
        control.performMove(board = board, screen = screen, finalPos = bestMoves[r][1])
        return
        
        
    
    #This function should, the - reward should be the best piece the enemy can capture
    def calcReward(self, piece, move, board):
        initPos = piece.pos
        takenPiece = board.movePiece(piece, initPos, move)
        if takenPiece != None:
            reward = takenPiece.value
        else:
            reward = 0

        bestEnemyCaptureValue = 0
        enemyMoves = board.getAllMovesInclCheck(self.enemyColor)
        for move in enemyMoves:
            p = board.pieces[move[0]][move[1]]
            if p != None:
                if p.color == self.color:
                    if p.value > bestEnemyCaptureValue:
                        bestEnemyCaptureValue = p.value
        
        reward = reward - bestEnemyCaptureValue
        
        board.movePiece(piece, piece.pos, initPos)
        if takenPiece != None:
            board.pieces[takenPiece.pos[0]][takenPiece.pos[1]] = takenPiece
        
        return reward

        