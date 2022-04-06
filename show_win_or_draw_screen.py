#setup
import pygame
from main import draw_text, terminate, clock, fps, screen, screen_height, screen_width, WindowColours

#win function
def show_win(colour):
    #declare guideline vars
    half_display_width = screen_width/2
    half_display_height = screen_height/2

    #set background colour
    if colour == "Yellow":
        bg = WindowColours.YELLOW
    else:
        bg = WindowColours.RED

    #main loop
    while 1:
        clock.tick(fps)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                terminate()

        screen.fill(bg)
        draw_text(f"{colour} Wins!", "ubuntu.ttf", 140, WindowColours.BLACK, half_display_width, half_display_height-40)
        draw_text("Click to exit", "ubuntu.ttf", 56, WindowColours.BLACK, half_display_width, half_display_height+40)

        pygame.display.flip()

def show_draw_and_go_again():
    #declare guideline vars
    half_display_width = screen_width/2
    half_display_height = screen_height/2

    #set background colour
    bg = WindowColours.GREY

    #main loop
    while 1:
        clock.tick(fps)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                return True

        screen.fill(bg)
        draw_text("It is a draw!", "ubuntu.ttf", 140, WindowColours.WHITE, half_display_width, half_display_height-40)
        draw_text("Click to play again", "ubuntu.ttf", 56, WindowColours.WHITE, half_display_width, half_display_height+40)

        pygame.display.flip()