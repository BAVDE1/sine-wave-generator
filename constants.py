import pygame as pg
from pygame import Vector2 as Vec2


def get_middle(pos, width_1, width_2) -> int:
    return (pos + (width_1 / 2)) - (width_2 / 2)


class CustomEvents:
    DEL_MODAL = pg.event.custom_type()
    CLEAR_MODAL = pg.event.custom_type()


class Texts:
    GENERATOR = 'generator '
    AMP = 'amp'
    FREQ = 'freq'
    PHASE = 'phase'
    ON = ' 1 '
    OFF = ' 0 '
    CLOSE = ' X '
    CLEAR = ' C '
    NEW_SINE = '+ New Sine'
    GRANULARITY = 'Granularity'
    POINT_SIZE = 'Point Size'
    LINE_SIZE = 'Line Size'
    PPF = 'Pixels / Frame'
    PHASE_DIV = 'Phase Division'
    RENDER_PAGE = ' Render: page '
    RENDER_ALL = ' Render: all'


class GameValues:
    FONT = "Times New Roman"

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    RES_MUL = 1

    MODAL_WIDTH = 220
    MODAL_WIDTH_SMALL = 160
    MODAL_HEIGHT = 120

    DISPLAY_WIDTH = 740
    DISPLAY_HEIGHT = 600

    MIN_RADIUS = 20
    MAX_RADIUS = 50

    MIN_GRAN = 1
    MAX_GRAN = 40
    MIN_POINT_SIZ = 0
    MAX_POINT_SIZ = 15
    MIN_LINE_SIZ = 0
    MAX_LINE_SIZ = 15
    MIN_PPF = 1
    MAX_PPF = 40
    MIN_PHASE_DIV = 1
    MAX_PHASE_DIV = 10

    MIN_AMP = 2
    MIN_FREQ = 1
    MIN_PHASE = 0
    MAX_AMP = 260
    MAX_FREQ = 12
    MAX_PHASE = 31

    PAGE_NUMBERS = 8


class Colours:
    BG_COL = (0, 10, 10)
    BG_COL_LIGHT = (0, 15, 15)
    WHITE = (255, 255, 255)
    LIGHT_GREY = (150, 150, 150)
    GREY = (60, 100, 100)
    DARK_GREY = (30, 50, 50)
    DARKER_GREY = (10, 25, 25)
    BLACK = (0, 0, 0)

    RED = (255, 60, 60)
    ORANGE = (255, 140, 60)
    YELLOW = (255, 255, 0)
    GREEN = (100, 255, 100)
    AQUA = (100, 255, 255)
    BLUE = (70, 150, 255)
    MAGENTA = (200, 0, 200)
    PINK = (255, 100, 255)


class SMValues:
    SM_1_POS = pg.Vector2(10, 100)
    SM_2_POS = pg.Vector2(10, 230)
    SM_3_POS = pg.Vector2(10, 360)
    SM_4_POS = pg.Vector2(10, 490)

    SM_COL_1 = Colours.RED
    SM_COL_2 = Colours.ORANGE
    SM_COL_3 = Colours.YELLOW
    SM_COL_4 = Colours.GREEN
    SM_COL_5 = Colours.AQUA
    SM_COL_6 = Colours.BLUE
    SM_COL_7 = Colours.MAGENTA
    SM_COL_8 = Colours.PINK
