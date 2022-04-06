#setup imports
import pygame
import sys
import os

pygame.init()

#variables
grid_size = 100
boundary = 125
column_count = 8
row_count = 7

#screen
screen_width = grid_size*column_count
screen_height = boundary + grid_size*row_count
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Connect Four')

#icon
icon_img = pygame.image.load('connect-four.png')
icon = pygame.display.set_icon(icon_img)

#in-game clock
clock = pygame.time.Clock()
fps = 60

#functions
def draw_text(text, font, size, colour, midx, midy):
    font = pygame.font.SysFont(font, size, True)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.centerx = midx
    text_rect.centery = midy
    screen.blit(text_surface, text_rect)

def create_blank_board():
    board = []
    for _ in range(row_count):
        board.append([0]*column_count)
    return board

def terminate():
    pygame.quit()
    sys.exit()

#colours
class WindowColours:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (173, 216, 230)
    GREY = (128, 128, 128)
    LIGHT_GREY = (220, 220, 220)
    RED = (200, 36, 36)
    YELLOW = (200, 200, 36)
    MAGENTA = (255, 0, 255)
    INDIGO = (75, 0, 130)

if __name__ == '__main__':
    os.system("python3 menu.py")