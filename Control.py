class Control:
    def __init__(self):
        self.moveMode = False
        self.movingPiece = None
        self.turn = 'w'

    def getCoord(self, board, pos):
        for r in range (0,8):
            for c in range (0,8):
                if board.board[r][c].pygameSquare.collidepoint(pos):
                    return [r, c]

    def mouseClick(self, board, pos, screen):    
        if (not self.moveMode): #Highlight piece
            cord = self.getCoord(board, pos)
            piece = board.pieces[cord[0]][cord[1]]
            if (piece != None):
                if (piece.color == self.turn):
                    self.movingPiece = board.pieces[cord[0]][cord[1]]
                    if (self.movingPiece != None):
                        self.moveMode = True
                        board.highlightValidMoves(self.movingPiece, screen)
            #print("({}, {})".format(cord[0], cord[1]))
            
        else:                   #Move highlighted piece
            self.moveMode = False
            finalPos = self.getCoord(board, pos)
            initPos = self.movingPiece.pos
            if (finalPos in self.movingPiece.getValidMoves(board)):
                #Before update, check if last mover is in check, if he is, then don't do the move and give a message
                board.movePiece(self.movingPiece, initPos, finalPos)
                if board.inCheck(self.turn):
                    board.movePiece(self.movingPiece, finalPos, initPos)
                    print("In check!")
                else:
                    if (self.turn == 'w'):
                        self.turn = 'b'
                    else:
                        self.turn = 'w'                    
            #Put some animation here!!
            board.update(screen)
            self.movingPiece = None

