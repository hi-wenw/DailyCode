import pygame
import sys

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((300, 300))

    pygame.display.set_caption('baozi6')

    f = pygame.font.Font('C:/Windows/Fonts/Candara.ttf', 50)

    text = f.render("baozi666", True, (255, 0, 0), (0, 0, 0))

    textRect = text.get_rect()

    textRect.center = (150,150)

    screen.blit(text, textRect)


