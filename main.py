"""Setup"""

# Imports
import sys
import pygame
pygame.init()

# Initial variables
grid_size = 80
half_grid_size = grid_size/2
boundary_y = int(grid_size*1.25)
boundary_x = grid_size//8
column_count = 8
row_count = 7
board = []
num_turns = 0
score = {
    "Yellow":0,
    "Red":0
}


# Screen
screen_width = boundary_x + grid_size*column_count + boundary_x
screen_height = boundary_y + grid_size*row_count + boundary_y
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Connect Four')


# Icon & images & sound 
icon_img = pygame.image.load('icon.png')
icon = pygame.display.set_icon(icon_img)
grid_box = pygame.image.load('grid-box-2.png').convert_alpha()
grid_box = pygame.transform.scale(grid_box, (grid_size, grid_size))
highlighted_grid_box = pygame.image.load('grid-box-1.png').convert_alpha()
highlighted_grid_box = pygame.transform.scale(highlighted_grid_box, (grid_size, grid_size))
drop_sound = pygame.mixer.Sound('token-drop.mp3')
music = pygame.mixer.music.load('background.mp3')

# In-game clock
clock = pygame.time.Clock()
fps = 60


# Terminate program
def terminate():
    print("Final score is..\n\033[33mYellow\033[0m        :         \033[31mRed\033[0m\n  {}           :          {}".format(score["Yellow"], score["Red"]))
    pygame.quit()
    sys.exit()


# Colours
class colours:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (173, 216, 230)
    GREY = (192, 192, 192)
    LIGHT_GREY = (220, 220, 220)
    RED = (235, 64, 64)
    YELLOW = (241, 196, 15)
    MAGENTA = (255, 0, 255)
    INDIGO = (75, 0, 130)
    NEXTYELLOW = (139, 128, 0)
    NEXTRED = (139, 0, 0)


# Draw text onto screen
def draw_text(text, font, size, colour, midx, midy):
    font = pygame.font.SysFont(font, size, True)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.centerx = midx
    text_rect.centery = midy
    screen.blit(text_surface, text_rect)


# Create a 2D blank board of 0s
def create_blank_board():
    board = []
    for _ in range(row_count):
        board.append([0]*column_count)
    return board



"""Menu"""

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
        
        screen.fill(colours.WHITE)
        mes = "Click anywhere on the screen to play a friend!"
        mes_array = [char for char in mes]
        if len(mes_array) > 30:
            for l in range(len(mes_array)-1, -1, -1):
                if l < 40:
                    if mes_array[l] == " ":
                        mes_1 = mes_array[:l]
                        mes_2 = mes_array[l:]
                        break
        mes_1 = "".join(mes_1)
        mes_2 = "".join(mes_2)
        draw_text(mes_1, "Segoe UI", 35, colours.BLACK, half_display_width, half_display_height - 30)
        draw_text(mes_2, "Segoe UI", 35, colours.BLACK, half_display_width, half_display_height + 30)

        pygame.display.flip()



"""Game functions"""

# Check grid position
def check_mouse_x():
    mouse_grid_x = (pygame.mouse.get_pos()[0] - boundary_x) // grid_size
    return mouse_grid_x


# Find the next row from the bottom that has a 0
def find_next_valid_row(c):
    for r in range(row_count-1, -1, -1):
        try:
            if board[r][c] == 0:
                return r
        except:
            continue


# Take turn
def take_turn(grid_x):
    global num_turns
    r = find_next_valid_row(grid_x)
    mouse_pos = pygame.mouse.get_pos()
    # If mouse position is in area
    if mouse_pos[1] > boundary_y and mouse_pos[1] < screen_height - boundary_y:
        if mouse_pos[0] > boundary_x and mouse_pos[0] < screen_width - boundary_x:
            pygame.mixer.Sound.play(drop_sound)
            if num_turns % 2 == 0:
                go = 1
            else:
                go = 2
            try:
                board[r][grid_x] = go
            except:
                pass
            num_turns += 1
    
        # Print board to console
        for r in board:
            print(r)
        print("\n")



"""End game logic"""

# Check if won
def check_win(board, piece):
    # Check horizontal locationss
    for c in range(column_count-3):
        for r in range(row_count):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                if piece == 1:
                    score["Yellow"] += 1
                else:
                    score["Red"] += 1
                return True

    # Check vertical locations
    for c in range(column_count):
        for r in range(row_count-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                if piece == 1:
                    score["Yellow"] += 1
                else:
                    score["Red"] += 1
                return True

    # Check \ locations
    for c in range(column_count-3):
        for r in range(row_count-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                if piece == 1:
                    score["Yellow"] += 1
                else:
                    score["Red"] += 1
                return True
    
    # Check / locations
    for c in range(column_count-3):
        for r in range(3, row_count):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                if piece == 1:
                    score["Yellow"] += 1
                else:
                    score["Red"] += 1
                return True
    
    return False


# Check if draw
def check_draw(board):
    for r in board:
        for c in r:
            if c != 0:
                pass
            else:
                return False
    return True


"""Drawing"""

# Draw grid & highlight
def draw_grid(grid_x):
    # Draw grid boxes
    for row_num, row in enumerate(board):
        for col_num, _ in enumerate(row):
            if col_num == grid_x:
                box = highlighted_grid_box
            else:
                box = grid_box
            screen.blit(box, (boundary_x + col_num*grid_size, boundary_y + row_num*grid_size))

    # Draw lines surrounding grid
    width = 3
    pygame.draw.line(screen, colours.BLACK, (boundary_x, boundary_y), (screen_width - boundary_x, boundary_y), width)
    pygame.draw.line(screen, colours.BLACK, (screen_width - boundary_x, boundary_y), (screen_width - boundary_x, screen_height - boundary_y), width)
    pygame.draw.line(screen, colours.BLACK, (screen_width - boundary_x, screen_height - boundary_y), (boundary_x, screen_height - boundary_y), width)
    pygame.draw.line(screen, colours.BLACK, (boundary_x, screen_height - boundary_y), (boundary_x, boundary_y), width)


# Draw tokens
def draw_tokens():
    colour = colours.BLACK
    for row_num, row in enumerate(board):
        for col_num, col in enumerate(row):
            if col == 1:
                colour = colours.YELLOW
            elif col == 2:
                colour = colours.RED
            centre = (boundary_x + 1 + half_grid_size + col_num * grid_size, boundary_y + 1 + half_grid_size + row_num * grid_size)
            if col > 0:
                pygame.draw.circle(screen, colour, centre, int(grid_size/2-10))


"""Main game"""

def game():
    # Create a blank board
    global board
    board = create_blank_board()

    while 1:
        clock.tick(fps)

        ### Check if game has ended
        # Check for win
        if check_win(board, 1):
            show_win("Yellow")
        elif check_win(board, 2):
            show_win("Red")
        # Check for draw
        elif check_draw(board):
            show_draw()

        # Find the grid that the mouse is on
        ms_grid_x = check_mouse_x()
        if ms_grid_x < 0:
            ms_grid_x = 0
        if ms_grid_x > 7:
            ms_grid_x = 7

        # Handle events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                take_turn(ms_grid_x)

        ### Draw to the screen
        # Draw background
        screen.fill(colours.LIGHT_BLUE)
        # Draw grid
        draw_grid(ms_grid_x)
        # Draw tokens
        draw_tokens()
        # Draw next grid place
        if num_turns % 2 == 0:
            colour = colours.NEXTYELLOW
        else:
            colour = colours.NEXTRED
        row = find_next_valid_row(ms_grid_x)
        try:
            pygame.draw.circle(screen, colour, (boundary_x + 1 + grid_size/2 + ms_grid_x*grid_size, boundary_y + 1 + grid_size/2 + grid_size*row), half_grid_size - 10)
        except:
            pass

        # Draw texts
        draw_text("Connect 4", 'didot.ttc', int(grid_size*1.08), colours.INDIGO, int(screen_width/2), int(boundary_y//2))
        draw_text("Yellow: {}".format(score["Yellow"]), 'arial.ttf', int(grid_size//2.5), colours.MAGENTA, boundary_x + grid_size*0.8, boundary_y + row_count*grid_size + boundary_y//4)
        draw_text("Red: {}".format(score["Red"]), 'arial.ttf', int(grid_size//2.5), colours.MAGENTA, screen_width - grid_size*0.8, boundary_y + row_count*grid_size + boundary_y//4)

        pygame.display.flip()


"""After game screens"""

# Win screen
def show_win(win):
    # Declare guideline vars
    half_display_width = screen_width/2
    half_display_height = screen_height/2

    # Set background colour
    if win == "Yellow":
        bg = colours.YELLOW
        first = "Yellow"
        first_score = score["Yellow"]
        second = "Red"
        second_score = score["Red"]
    else:
        bg = colours.RED
        first = "Red"
        first_score = score["Red"]
        second = "Yellow"
        second_score = score["Yellow"]

    while 1:
        clock.tick(fps)

        # Handle events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                game()

        # Draw to screen
        screen.fill(bg)
        draw_text(f"{first} : {first_score}      {second} : {second_score}", "ubuntu.ttf", int(grid_size//1.3), colours.BLACK, half_display_width, grid_size*0.5)
        draw_text(f"{win} Wins!", "ubuntu.ttf", int(grid_size*1.5), colours.BLACK, half_display_width, half_display_height-40)
        draw_text("Click to play again", "ubuntu.ttf", int(grid_size//1.8), colours.BLACK, half_display_width, half_display_height+60)
        draw_text("or press escape to leave", "ubuntu.ttf", int(grid_size//1.8), colours.BLACK, half_display_width, half_display_height+100)

        pygame.display.flip()


# Draw screen
def show_draw():
    # Declare guideline vars
    half_display_width = screen_width/2
    half_display_height = screen_height/2

    # Set background colour
    bg = colours.GREY

    while 1:
        clock.tick(fps)

        # Handle events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                game()

        # Draw to screen
        screen.fill(bg)
        draw_text("It is a draw!", "ubuntu.ttf", int(grid_size*1.4), colours.BLACK, half_display_width, half_display_height - 40)
        draw_text("Click to play again", "ubuntu.ttf", int(grid_size//1.8), colours.WHITE, half_display_width, half_display_height + 40)
        draw_text("or press escape to leave", "ubuntu.ttf", int(grid_size//1.8), colours.WHITE, half_display_width, half_display_height + 80)

        pygame.display.flip()


"""Run program"""

if __name__ == '__main__':
    pygame.mixer.music.play(-1)
    menu()