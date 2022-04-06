#imports
import pygame
from main import create_blank_board, draw_text, terminate, boundary, column_count, clock, fps, grid_size, row_count, screen, WindowColours
from show_win_or_draw_screen import show_win, show_draw_and_go_again

#setup game variables
num_turns = 0
board = create_blank_board()

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
def game_func():
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
                game_func()

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