import pygame
from Control import Control
from Board import Board


if __name__ == "__main__":
    
    squareSize = 50

    pygame.init()
    screen = pygame.display.set_mode((8*squareSize, 8*squareSize),0,32)
    clock = pygame.time.Clock()
    
    board = Board(squareSize)
    board.draw(screen)
    control = Control()
    
    while True:
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  #left mouse button
                    control.mouseClick(board, event.pos, screen)
                    
    




