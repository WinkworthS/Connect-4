#setup imports
import pygame
import sys

pygame.init()

#initial variables
grid_size = 100
boundary = 125
column_count = 8
row_count = 7
board = []
num_turns = 0

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


#menu screen
def menu():
    global screen, clock

    half_display_width = screen_width/2
    half_display_height = screen_height/2

    while 1:
        clock.tick(fps)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                game()
        
        screen.fill((255, 255, 255))
        draw_text("Click anywhere on the screen to play!", "Segoe UI", 35, WindowColours.BLACK, half_display_width, half_display_height)

        pygame.display.flip()


#game
#check grid pos
def check_mouse_x():
    mouse_grid_x = pygame.mouse.get_pos()[0] // grid_size
    return mouse_grid_x

#find the next row from the bottom that has a 0, in the column
def find_next_valid_row(c):
    for r in range(row_count-1, -1, -1):
        if board[r][c] == 0:
            return r

#take turn
def take_turn(grid_x):
    global num_turns

    r = find_next_valid_row(grid_x)
    if num_turns % 2 == 0:
        try:
            board[r][grid_x] = 1
        except:
            pass
    else:
        try:
            board[r][grid_x] = 2
        except:
            pass
    num_turns += 1
    
    #print board to console
    for r in board:
        print(r)
    print("\n")

#check if won
def check_win(board, piece):
    #check horizontal locs
    for c in range(column_count-3):
        for r in range(row_count):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    #check vertical locs
    for c in range(column_count):
        for r in range(row_count-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    #check \ locs
    for c in range(column_count-3):
        for r in range(row_count-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    
    #check / locs
    for c in range(column_count-3):
        for r in range(3, row_count):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    
    return False

#check if there is a draw
def check_draw(board):
    for r in board:
        for c in r:
            if c != 0:
                pass
            else:
                return False
    return True

#draw tokens
def draw_tokens():
    colour = WindowColours.BLACK
    for row_num, row in enumerate(board):
        for col_num, col in enumerate(row):
            if col == 1:
                colour = WindowColours.YELLOW
            elif col == 2:
                colour = WindowColours.RED

            centre = (50 + col_num * grid_size, boundary + 50 + row_num * grid_size)
            pygame.draw.circle(screen, WindowColours.BLACK, centre, int(grid_size/2-7))
            if col > 0:
                pygame.draw.circle(screen, colour, centre, int(grid_size/2-10))

#main function
def game():
    global board
    #create board
    board = create_blank_board()

    #main loop
    while 1:
        clock.tick(fps)

        #check for won
        if check_win(board, 1):
            show_win("Yellow")
        elif check_win(board, 2):
            show_win("Red")
        #check for draw
        elif check_draw(board):
            if show_draw_and_go_again():
                game()

        #draw background
        screen.fill(WindowColours.LIGHT_GREY)
        pygame.draw.rect(screen, WindowColours.LIGHT_BLUE, (0, boundary, grid_size*column_count, boundary + grid_size*row_count))

        #find grid mouse is on
        ms_grid_x = check_mouse_x()

        #handle events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                take_turn(ms_grid_x)

        #highlight column mouse is on
        column_rect = pygame.Rect(ms_grid_x*grid_size, boundary, grid_size, grid_size*7)
        pygame.draw.rect(screen, WindowColours.GREY, column_rect)

        #draw tokens
        draw_tokens()

        #draw title text
        draw_text("Connect 4", 'didot.ttc', 108, WindowColours.INDIGO, int(grid_size*column_count/2), int(boundary//2))

        pygame.display.flip()


#if won
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

#if draw
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

if __name__ == '__main__':
    menu()
