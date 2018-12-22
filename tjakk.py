import pygame
from Control import Control
from Board import Board
from AI import AI_Player

if __name__ == "__main__":
    
    squareSize = 75

    pygame.init()
    screen = pygame.display.set_mode((8*squareSize, 8*squareSize),0,32)
    clock = pygame.time.Clock()
    
    board = Board(squareSize)
    board.draw(screen)
    control = Control(squareSize)
    #control.drawButtons(screen, squareSize)
    
    twoPlayerMode = False

    if not twoPlayerMode:
        ai = AI_Player('b')

    while True:
        pygame.display.update()
        clock.tick(60)
        
        if not twoPlayerMode and control.turn == ai.color:
            #ai.moveRand(board, screen, control)
            #ai.moveRandPrioritizeCaptureUsingVal(board, screen, control)
            #ai.moveRandEvaluateIfCapturedOnNewPosUsingVal(board, screen, control)
            ai.smartMove(board, screen, control)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  #left mouse button
                    control.mouseClick(board, event.pos, screen)
                    
    