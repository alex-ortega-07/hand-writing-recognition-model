from utils import *
import numpy as np
import pygame

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hand writing recognition model')

clock = pygame.time.Clock()
display.fill(BG_COLOR)


def init_grid(color, rows, cols):
    '''
    Creates two lists where we insert all the pixels values, the grid list contains
    an RGB color format, instead, the grid_ai list contains a value from 0 to 255
    '''
    
    grid = []
    grid_ai = []

    for row in range(rows):
        grid.append([])
        grid_ai.append([])
        for _ in range(cols):
            grid[row].append(list(color))
            grid_ai[row].append(color[0])

    return grid, grid_ai

def draw_grid_lines(color):
    '''
    Creates the line division of the grid
    '''
    
    for i in range(CANVAS_ROWS + 1):
        pygame.draw.line(display, color, (MARGIN_CANVAS_SIDES, i * SPACE_EACH_SQUARE + MARGIN_CANVAS_TOP), (WIDTH - MARGIN_CANVAS_SIDES, i * SPACE_EACH_SQUARE + MARGIN_CANVAS_TOP))

    for i in range(CANVAS_COLS + 1):
        pygame.draw.line(display, color, (i * SPACE_EACH_SQUARE + MARGIN_CANVAS_SIDES, MARGIN_CANVAS_TOP), (i * SPACE_EACH_SQUARE + MARGIN_CANVAS_SIDES, HEIGHT - MARGIN_CANVAS_BOTTOM))

def draw_grid_squares(grid):
    '''
    Displays the pixel colors on the screen
    '''
    
    for i, row in enumerate(grid):
        for j, pixel_color in enumerate(row):
            pygame.draw.rect(display, pixel_color, (MARGIN_CANVAS_SIDES + i * SPACE_EACH_SQUARE, MARGIN_CANVAS_TOP + j * SPACE_EACH_SQUARE, SPACE_EACH_SQUARE, SPACE_EACH_SQUARE))

def draw_grid_pixel(color, grid, posx, posy, size):
    '''
    Paints the corresponding pixels for the position given
    '''
    
    for i, row in enumerate(grid):
        for j, pixel_color in enumerate(row):
            if MARGIN_CANVAS_SIDES + i * SPACE_EACH_SQUARE <= posx < MARGIN_CANVAS_SIDES + i * SPACE_EACH_SQUARE + SPACE_EACH_SQUARE:
                if MARGIN_CANVAS_TOP + j * SPACE_EACH_SQUARE <= posy < MARGIN_CANVAS_TOP + j * SPACE_EACH_SQUARE + SPACE_EACH_SQUARE:
                    if size == 1:
                        grid[i][j] = color
                        grid_ai[i][j] = color[0]
                    
                    elif size == 4:
                        for x in range(2):
                            for y in range(2):
                                try:
                                    grid[i + x][j + y] = color
                                    grid_ai[i + x][j + y] = color[0]
                                except:
                                    pass

grid, grid_ai = init_grid(BG_COLOR, CANVAS_ROWS, CANVAS_COLS)
predicted_value = '---'

while True:
    display.fill(WHITE)

    # We create all the buttons with our class Button
    grid_bt = Button(40, MARGIN_CANVAS_TOP - 10 * 2, MARGIN_CANVAS_SIDES, 10, LINE_COLOR, BLACK, 'Grid')
    grid_bt.create(display)

    size_bt = Button(100, MARGIN_CANVAS_TOP - 10 * 2, MARGIN_CANVAS_SIDES + 50, 10, LINE_COLOR, BLACK, 'Change size')
    size_bt.create(display)

    clear_bt = Button(50, MARGIN_CANVAS_TOP - 10 * 2, MARGIN_CANVAS_SIDES + 160, 10, LINE_COLOR, BLACK, 'Clear')
    clear_bt.create(display)

    prediction_bt = Button(60, MARGIN_CANVAS_TOP - 10 * 2, MARGIN_CANVAS_SIDES + 220, 10, LINE_COLOR, BLACK, 'Predict')
    prediction_bt.create(display)

    prediction_txt = Button(WIDTH - MARGIN_CANVAS_SIDES * 2, MARGIN_CANVAS_BOTTOM - 10 * 2, MARGIN_CANVAS_SIDES, HEIGHT - MARGIN_CANVAS_BOTTOM + 10, BG_COLOR, BLACK, f'Model prediction: {predicted_value}')
    prediction_txt.create(display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if pygame.mouse.get_pressed()[0]:
            draw_grid_pixel(PIXEL_ACTIVE_COLOR, grid, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], CANVAS_PAINT_SIZE)

            # If the grid button is clicked, we set the value of CANVAS_GRID to be the opposite of the current value
            if grid_bt.clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                CANVAS_GRID = not CANVAS_GRID

            # If the size button is clicked, we change the size
            if size_bt.clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                if CANVAS_PAINT_SIZE == 1:
                    CANVAS_PAINT_SIZE = 4

                else:
                    CANVAS_PAINT_SIZE = 1

            # If the clear button is clicked, we initialize the grid
            if clear_bt.clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                grid, grid_ai = init_grid(BG_COLOR, CANVAS_ROWS, CANVAS_COLS)

            # We check if the predict button is clicked, in case the user clicked it, we prepare the data
            if prediction_bt.clicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                img = np.array(grid_ai)
                img = img.transpose()
                img = img.reshape(28, 28, 1)
                img = img.astype('float32')
                img = 255 - img
                img = np.expand_dims(img, axis = 0)

                arr = model.predict(img)
                predicted_value = np.argmax(arr)

        # If you press the right click, we paint the pixels with the background color
        elif pygame.mouse.get_pressed()[2]:
            draw_grid_pixel(BG_COLOR, grid, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], CANVAS_PAINT_SIZE)

    draw_grid_squares(grid)
    if CANVAS_GRID:
        draw_grid_lines(LINE_COLOR)

    else:
        draw_grid_lines(BG_COLOR)

    pygame.display.flip()
    clock.tick(FPS)