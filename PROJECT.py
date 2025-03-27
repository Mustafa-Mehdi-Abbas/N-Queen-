import pygame
import sys
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()

WIDTH = 700
# Press left click to start execution

# Get user input for the number of queens
ROW = ''
message = ''
input_msg = 'Enter Number of Queens:'
cont_msg = ''
speed = None
heading_msg = 'N-QUEEN PROBLEM SOLVER'
solved = False

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('N-QUEEN SOLVER')


slider = Slider(WIN, 100, 270, 300, 40, min=0, max=100, step=1)
output = TextBox(WIN, 450, 265, 70, 50, fontSize=30)

output.disable()
# white color 
color = (255,255,255) 
  
# light shade of the button 
color_light = (170,170,170) 
  
# dark shade of the button 
color_dark = (100,100,100) 
  
# stores the width of the 
# screen into a variable 
width = WIN.get_width() 
  
# stores the height of the 
# screen into a variable 
height = WIN.get_height() 
  
# defining a font 
smallfont = pygame.font.SysFont('Corbel',35) 
  
# rendering a text written in 
# this font 
text = smallfont.render('Quit' , True , color) 

text2 = smallfont.render('Retry',True,color)

text3 = smallfont.render('Start',True,color)

clock = pygame.time.Clock()
base_font = pygame.font.Font(None,32)
heading_font = pygame.font.Font(None,48)

heading_rect = pygame.Rect(150,30,200,32)
display_rect = pygame.Rect(100,150,140,32)
input_rect = pygame.Rect(140,200,140,32)
error_rect = pygame.Rect(100,450,140,32)
cont_rect = pygame.Rect(100,350,140,32)

color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('gray15')

color = color_passive

active = False



RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.total_rows = total_rows
        self.width = width
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_checking(self):
        return self.color == BLUE

    def is_reset(self):
        return self.color == WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_checking(self):
        self.color = BLUE

    def make_reset(self):
        self.color = WHITE

    def draw(self, win):
        if self.color == BLACK:  # Check if the spot is a barrier
            queen_img = pygame.image.load('nqeen.jpg')
            queen_img = pygame.transform.scale(queen_img, (self.width, self.width))
            win.blit(queen_img, (self.x, self.y))
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
       
    def __lt__(self, other):
        return False


def algorithm(grid):
    global solved
    sol = solveNQUtil(lambda: draw(WIN, grid, int(ROW), WIDTH-50), grid, 0)
    if not sol:
        print("No Solution")
        solved = False
        return False
    else:
        print("Solution Found")
        solved = True
        return True

def isSafe(draw, grid, row, col):
    temp = grid[row][col].color
    grid[row][col].make_open()
    draw()
    # Check this row on left side
    for i in range(col):
        if grid[row][i].is_barrier():
            grid[row][i].make_closed()
            draw()
            grid[row][i].make_barrier()
            draw()
            for j in range(col):
                if j == i:
                    continue
                grid[row][j].make_reset()
            grid[row][col].make_reset()
            return False
        if not grid[row][i].is_open():
            grid[row][i].make_checking()
            draw()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].is_checking():
                grid[i][j].make_reset()

    # Check upper diagonal on left side
    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if grid[i][j].is_barrier():
            grid[i][j].make_closed()
            draw()
            grid[i][j].make_barrier()
            draw()
            for i2, j2 in zip(range(row, -1, -1),
                              range(col, -1, -1)):
                if i2 == i and j2 == j:
                    continue
                grid[i2][j2].make_reset()
            grid[row][col].make_reset()
            return False
        if not grid[i][j].is_open():
            grid[i][j].make_checking()
            draw()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].is_checking():
                grid[i][j].make_reset()

    # Check lower diagonal on left side
    for i, j in zip(range(row, int(ROW), 1),
                    range(col, -1, -1)):
        if grid[i][j].is_barrier():
            grid[i][j].make_closed()
            draw()
            grid[i][j].make_barrier()
            draw()
            for i2, j2 in zip(range(row, int(ROW), 1),
                              range(col, -1, -1)):
                if i2 == i and j2 == j:
                    continue
                grid[i2][j2].make_reset()
                # draw()
            grid[row][col].make_reset()
            return False
        if not grid[i][j].is_open():
            grid[i][j].make_checking()
            draw()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].is_checking():
                grid[i][j].make_reset()
    grid[row][col].color = temp
    return True


def solveNQUtil(draw, grid, col):
    # base case: If all queens are placed
    # then return true
    if col >= int(ROW):
        return True

    # Consider this column and try placing
    # this queen in all rows one by one
    for i in range(int(ROW)):

        if isSafe(draw, grid, i, col):

            # Place this queen in board[i][col]
            grid[i][col].make_barrier()
            draw()
            # recur to place rest of the queens
            if solveNQUtil(draw, grid, col + 1) == True:
                return True

            # If placing queen in board[i][col
            # doesn't lead to a solution, then
            # queen from board[i][col]
            grid[i][col].make_reset()
            draw()

    # if the queen can not be placed in any row in
    # this column col then return false
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    global solved
    win.fill(BLACK)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)

    pygame.display.flip()
    pygame.time.wait(speed)


def main(win, width):

    grid = make_grid(int(ROW), width)
    run = True
    started = False

    draw(win, grid, int(ROW), width)

    global solved

    while True:

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 100 <= mouse[0] <= 100+140 and 655 <= mouse[1] <= 655+40: 
                        pygame.quit() 
                        sys.exit()

                    if 300 <= mouse[0] <= 300+140 and 655 <= mouse[1] <= 655+40: 
                        intro()

                    if solved == False:

                        if 500 <= mouse[0] <= 500+140 and 655 <= mouse[1] <= 655+40: 
                            started = True
                            algorithm(grid)
                        
                if started:
                    continue    
                
            mouse = pygame.mouse.get_pos() 

            if 100 <= mouse[0] <= 100+140 and 655 <= mouse[1] <= 655+40: 
                pygame.draw.rect(win,color_light,[100,655,140,40])
            else: 
                pygame.draw.rect(win,color_dark,[100,655,140,40])

            if 300 <= mouse[0] <= 300+140 and 655 <= mouse[1] <= 655+40: 
                pygame.draw.rect(win,color_light,[300,655,140,40])
            else: 
                pygame.draw.rect(win,color_dark,[300,655,140,40])

            if solved == False:

                if 500 <= mouse[0] <= 500+140 and 655 <= mouse[1] <= 655+40: 
                    pygame.draw.rect(win,color_light,[500,655,140,40])
                else: 
                    pygame.draw.rect(win,color_dark,[500,655,140,40])

                win.blit(text3,(530,660))

            win.blit(text , (130,660))
            win.blit(text2, (330,660))


            pygame.display.flip()

        pygame.quit()
        sys.exit()
    
def intro():
    global ROW
    global active
    global cont_msg
    global input_msg
    global heading_msg
    global message
    global speed
    global solved
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if 100 <= mouse[0] <= 100+140 and 400 <= mouse[1] <= 400+40: 
                    if ROW == '':
                        message = 'Input Can Not Be Empty'
                    elif cont_msg == 'Click Start To Continue':
                        solved = False 
                        main(WIN, WIDTH-50)
                        pygame.quit()
                        sys.exit()
                    
            if event.type == pygame.KEYDOWN:
                if active == True:
                    if event.key == pygame.K_BACKSPACE:
                        message = ''
                        ROW = ROW[:-1]
                        if ROW == '':
                            cont_msg = ''
                        elif int(ROW) <= 100 and int(ROW) >= 4:
                            cont_msg = 'Click Start To Continue'
                        elif int(ROW) > 100:
                            message = 'For Better Experience Make Input <= 100'
                            cont_msg = ''
                        elif int(ROW) < 4:
                            message = 'Input Should be >= 4'
                            cont_msg = ''
                    elif event.key == pygame.K_0 or event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9:
                        message = ''
                        ROW += event.unicode
                        if int(ROW) > 100:
                            message = 'For Better Experience Make Input <= 100'
                            cont_msg = ''
                        elif int(ROW) < 4:
                            message = 'Input Should be >= 4'
                            cont_msg = ''
                        else:
                            message = ''
                            cont_msg = 'Click Start To Continue'
                    else:
                        message = 'Please Enter Any Valid Number'
                        if ROW == '':
                            cont_msg = ''

        WIN.fill((255,255,255))

        if active:
            color = color_active
        else: 
            color = color_passive
        pygame.draw.rect(WIN,color,input_rect,2)

        mouse = pygame.mouse.get_pos() 

        if 100 <= mouse[0] <= 100+140 and 400 <= mouse[1] <= 400+40: 
            pygame.draw.rect(WIN,color_light,[100,400,140,40])
        else: 
            pygame.draw.rect(WIN,color_dark,[100,400,140,40])

        WIN.blit(text3 , (130,405))


        disp_surface = base_font.render(input_msg,True,(0,0,0))
        text_surface = base_font.render(ROW,True,(0,0,0))
        msg_surface = base_font.render(message,True,(255,0,0))
        cont_surface = base_font.render(cont_msg,True,(0,255,0))
        heading_surface = heading_font.render(heading_msg,True,(0,0,0))


        WIN.blit(heading_surface,(heading_rect.x + 5, heading_rect.y + 5))
        WIN.blit(disp_surface,(display_rect.x + 5, display_rect.y + 5))
        WIN.blit(text_surface,(input_rect.x + 5, input_rect.y + 5))
        WIN.blit(msg_surface,(error_rect.x + 5, error_rect.y + 5))
        WIN.blit(cont_surface,(cont_rect.x + 5, cont_rect.y + 5))

        output.setText(slider.getValue())
        speed = slider.getValue()
        pygame_widgets.update(events)


        input_rect.w = max(140, text_surface.get_width() + 10)

        pygame.display.flip()
        clock.tick(60)


intro()