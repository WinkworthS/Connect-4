#imports
import pygame
from main import draw_text, terminate, clock, fps, screen, screen_height, screen_width, WindowColours
from game import game_func

pygame.init()

def display_menu():
    global screen, clock

    half_display_width = screen_width/2
    half_display_height = screen_height/2

    while 1:
        clock.tick(fps)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                game_func()
        
        screen.fill((255, 255, 255))
        draw_text("Click anywhere on the screen to play!", "Segoe UI", 35, WindowColours.BLACK, half_display_width, half_display_height)

        pygame.display.flip()

if __name__ == '__main__':
    display_menu()