import pygame

pygame.init()

# We declare some screen constants
WIDTH, HEIGHT = 300, 360
FPS = 240

# Here are some colors
BG_COLOR = 255, 255, 255
LINE_COLOR = 120, 120, 120
PIXEL_ACTIVE_COLOR = 0, 0, 0
BLACK = 0, 0, 0
WHITE = 255, 255, 255

# Below, we declare some data for the canvas
MARGIN_CANVAS_TOP = 40
MARGIN_CANVAS_BOTTOM = 40
MARGIN_CANVAS_SIDES = 10
SPACE_EACH_SQUARE = 10
CANVAS_GRID = True
CANVAS_ROWS = 28
CANVAS_COLS = 28
CANVAS_PAINT_SIZE = 4