#setup
import sys
import time
import pygame
pygame.init()

#set up & basic variables
grid_size = 100
boundary = 125
column_count = 8
row_count = 7
screen = pygame.display.set_mode((grid_size*column_count, boundary + grid_size*row_count))
pygame.display.set_caption('Connect Four')
num_turns = 0
finished_animation = True
clock = pygame.time.Clock()

#COLOURS
#window
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
GREY = (128, 128, 128)
LIGHT_GREY = (220, 220, 220)
RED = (200, 36, 36)
YELLOW = (200, 200, 36)
MAGENTA = (255, 0, 255)
INDIGO = (75, 0, 130)
#console
class Colours:
    # predecessor of all ansi codes
    pred = "\033["
    #codes
    red = f"{pred}31m"
    yellow = f"{pred}33m"
    white = f"{pred}37m"
    bold = f"{pred}1m"
    end = f"{pred}0m"


#add circles
board = [[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0]]


#terminate func
def terminate():
    pygame.quit()
    sys.exit()


#wait func
def wait():
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)
    print("End")


#check grid pos
def check_mouse_x():
    mouse_grid_x = pygame.mouse.get_pos()[0] // grid_size
    return mouse_grid_x


#check if turn taken
def check_turn(grid_x, grid_y):
    global num_turns
    for r_num, r in enumerate(board):
        if r_num == grid_y:  
            if r[grid_x] == 0:
                if num_turns % 2 == 0:
                    r[grid_x] = 1
                else:
                    r[grid_x] = 2
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


#check if draw
def check_draw(board):
    for r in board:
        for c in r:
            if c != 0:
                pass
            else:
                return False
    return True


#draw circles
def fall_mechanism():
    t = time.time()

    global finished_animation
    #put items in rows into columns
    col_1 = []
    col_2 = []
    col_3 = []
    col_4 = []
    col_5 = []
    col_6 = []
    col_7 = []
    col_8 = []
    for row in board:
        print(row)
        for col_num, col in enumerate(row):
            if col_num == 0:
                col_1.append(col)
            elif col_num == 1:
                col_2.append(col)
            elif col_num == 2:
                col_3.append(col)
            elif col_num == 3:
                col_4.append(col)
            elif col_num == 4:
                col_5.append(col)
            elif col_num == 5:
                col_6.append(col)
            elif col_num == 6:
                col_7.append(col)
            elif col_num == 7:
                col_8.append(col)
    cols = [col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8]

    #bubble swap algorithm
    for col in cols:
        for i in range(len(col)):
            for j in range(len(col) - 1):
                #if there is a 0 below the column
                if col[j+1] == 0:
                    if col[j] > col[j+1]:
                        #swap
                        col[j], col[j+1] = col[j+1], col[j]
    
    #put items in columns into rows
    for row in board:
        row_1 = []
        row_2 = []
        row_3 = []
        row_4 = []
        row_5 = []
        row_6 = []
        row_7 = []
        for col in cols:
            for row_num, row in enumerate(col):
                if row_num == 0:
                    row_1.append(row)
                elif row_num == 1:
                    row_2.append(row)
                elif row_num == 2:
                    row_3.append(row)
                elif row_num == 3:
                    row_4.append(row)
                elif row_num == 4:
                    row_5.append(row)
                elif row_num == 5:
                    row_6.append(row)
                elif row_num == 6:
                    row_7.append(row)
    rows = [row_1, row_2, row_3, row_4, row_5, row_6, row_7]
    
    #put rows into board
    for i in range(len(rows)):
        board[i] = rows[i]

    finished_animation = True

    time_taken = time.time() - t
    time_taken *= 1000000
    print(f"Time taken was {time_taken} microseconds")


def draw_circles():
    global finished_animation
    colour = BLACK
    for row_num, row in enumerate(board):
        for col_num, col in enumerate(row):
            if col == 1:
                colour = YELLOW
            elif col == 2:
                colour = RED

            centre = (50 + col_num * grid_size, boundary + 50 + row_num * grid_size)
            pygame.draw.circle(screen, BLACK, centre, radius=(grid_size/2-7))
            if col > 0:
                pygame.draw.circle(screen, colour, centre, radius=(grid_size/2-10))

            if not finished_animation:
                fall_mechanism()


#text functions
texts = []
def initialize_text(text, font_size, font, colour, mid_x, mid_y):
    font = pygame.font.SysFont(font, font_size)
    surface = font.render(text, True, colour)
    surface_rect = surface.get_rect()
    surface_rect.centerx = mid_x
    surface_rect.centery = mid_y
    texts.append((surface, surface_rect))

def draw_texts():
    for text in texts:
        screen.blit(text[0], text[1])


#initialize texts
initialize_text("Connect 4", 108, 'didot.ttc', INDIGO, grid_size*column_count/2, boundary//2)
        

#main loop
while True:
    clock.tick(60)

    #check if won
    if check_win(board, 1):
        print(f"\n{Colours.yellow}{Colours.bold}Yellow wins!{Colours.end}")
        wait()
        terminate()

    elif check_win(board, 2):
        print(f"\n{Colours.red}{Colours.bold}Red wins!\033[0m{Colours.end}")
        wait()
        terminate()

    elif check_draw(board):
        print(f"\n{Colours.white}{Colours.bold}It is a draw, all spaces have been used.{Colours.end}")
        wait()
        terminate()

    #draw background
    screen.fill(LIGHT_GREY)
    pygame.draw.rect(screen, LIGHT_BLUE, (0, boundary, grid_size*column_count, boundary + grid_size*row_count))

    #find grid mouse is on
    ms_grid_x = check_mouse_x()

    #handle events
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            terminate()
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            finished_animation = False
            check_turn(ms_grid_x, 0)

    #highlight column mouse is on
    column_rect = pygame.Rect(ms_grid_x*grid_size, boundary, grid_size, grid_size*7)
    pygame.draw.rect(screen, GREY, column_rect)

    #drawing
    #circles
    draw_circles()

    #text
    draw_texts()

    pygame.display.flip()
