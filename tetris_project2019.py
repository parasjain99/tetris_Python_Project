import pygame
import random

surface_color = (255,255,255)
pygame.font.init()

# GLOBALS VARS 
s_width = 800   #800
s_height = 700  #700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [[(0, 0), (1, 0), (-1, 1), (0, 1)], [(0, -1), (0, 0), (1, 0), (1, 1)]]
Z = [[(-1, 0), (0, 0), (0, 1), (1, 1)], [(0, -1), (-1, 0), (0, 0), (-1, 1)]]
I = [[(0, -2), (0, -1), (0, 0), (0, 1)], [(-2, -1), (-1, -1), (0, -1), (1, -1)]]
O = [[(-1, 0), (0, 0), (-1, 1), (0, 1)]]
J=[[(-1, -1), (-1, 0), (0, 0), (1, 0)], [(0, -1), (1, -1), (0, 0), (0, 1)], [(-1, 0), (0, 0), (1, 0), (1, 1)], [(0, -1), (0, 0), (-1, 1), (0, 1)]]
L=[[(1, -1), (-1, 0), (0, 0), (1, 0)], [(0, -1), (0, 0), (0, 1), (1, 1)], [(-1, 0), (0, 0), (1, 0), (-1, 1)], [(-1, -1), (0, -1), (0, 0), (0, 1)]]
T=[[(0, -1), (-1, 0), (0, 0), (1, 0)], [(0, -1), (0, 0), (1, 0), (0, 1)], [(-1, 0), (0, 0), (1, 0), (0, 1)], [(0, -1), (-1, 0), (0, 0), (0, 1)]]

# new shape
K = [[(-1, 0), (0, 0), (-1, 1), (0, 1)],[(0, -1), (0, 0), (1, 0), (0, 1)], [(-1, 0), (0, 0), (1, 0), (0, 1)]]

shapes = [S, Z, I, O, J, L, T, K]

shape_colors = [(100, 255, 100), (255, 100, 100), (100, 255, 255), (255, 255, 100), (255, 165, 100), (100, 100, 255), (128, 100, 128)]
# index 0 - 6 represent shape
border_color = (100, 100, 100)

class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3


def create_grid(locked_positions={}):
    # grid = [[(0,0,0) for x in range(10)] for y in range(20)]
    grid = [[surface_color for x in range(10)] for y in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for pos in format:
        positions.append((pos[0]+piece.x,pos[1]+piece.y))

    return positions


def valid_space(shape, grid):
    accepted_positions = [(j, i) for i in range(20) for j in range(10) if grid[i][j] == surface_color]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(size, color, surface,text1, text2="" ):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label1 = font.render(text1, 1, color)
    label2 = font.render(text2,1,color)
    surface.blit(label1, (top_left_x + play_width/2 - (label1.get_width() / 2),top_left_y + play_height/3 - 2*label1.get_height()/2))
    surface.blit(label2, (top_left_x + play_width/2 - (label2.get_width() / 2), top_left_y + play_height/3 + label1.get_height()/2))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, border_color, (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
    for j in range(col):
        pygame.draw.line(surface, border_color, (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines


def clear_rows(grid, locked):
    # print(len(grid))
    # need to see if row is clear the shift every other row above down one
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if surface_color not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):

    # sx = top_left_x + play_width + 50
    # sy = top_left_y + play_height/2 - 100
    sx = top_left_x + play_width + 100
    sy = top_left_y + play_height/2 - 100

    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (0,0,0))
    surface.blit(label, (sx - 2*block_size, sy - 3*block_size))
    
    format = shape.shape[shape.rotation % len(shape.shape)]

    for pos in format:
        pygame.draw.rect(surface, shape.color, (sx + pos[1]*block_size, sy + pos[0]*block_size, block_size, block_size), 0)

def show_score(score, surface):
    sx = 50
    sy = 50 + play_height/2 - 100
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score', 1, (0, 0, 0))
    labe2 = font.render(str(score), 1, (0, 0, 0))
    surface.blit(label, (sx, sy))
    surface.blit(labe2, (sx, sy + block_size))


def draw_window(surface):
    global grid
    surface.fill(surface_color)
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (0,0,0))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    # print(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
            

    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, border_color, (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()


def main():
    global grid
    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_speed = 0.30   #.27
    fall_time = 0
    score = 0
    while run:

        
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    # print(convert_shape_format(current_piece))  # space bar to bump piece down

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            fall_speed-=0.01
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            # score+=1
            change_piece = False

            # call four times to check for multiple clear rows
            score+=10*clear_rows(grid, locked_positions)

        draw_window(win)
        draw_next_shape(next_piece, win)
        show_score(score, win)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    draw_text_middle(40, (0, 0, 0), win,"Game Over" )
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill(surface_color)
        draw_text_middle(60, (0, 0, 0), win,"Made By Paras", "Press any key to begin.")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game
