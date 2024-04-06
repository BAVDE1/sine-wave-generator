import pygame as pg


def get_middle(pos, width_1, width_2) -> int:
    return (pos + (width_1 / 2)) - (width_2 / 2)


class CustomEvents:
    DEL_MODAL = pg.event.custom_type()


class Texts:
    GENERATOR = 'generator '
    AMP = 'amp'
    FREQ = 'freq'
    PHASE = 'phase'
    ON = ' 1 '
    OFF = ' 0 '
    CLOSE = ' X '
    NEW_SINE = 'New Sine'


class GameValues:
    FONT = "Times New Roman"

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    RES_MUL = 1

    MODAL_WIDTH = 220
    MODAL_HEIGHT = 120

    MIN_RADIUS = 30
    MAX_RADIUS = 50

    MIN_AMP = 1
    MIN_FREQ = 1
    MIN_PHASE = 0
    MAX_AMP = 50
    MAX_FREQ = 10
    MAX_PHASE = 10


class Colours:
    BG_COL = (0, 10, 10)
    WHITE = (255, 255, 255)
    LIGHT_GREY = (150, 150, 150)
    GREY = (100, 100, 100)
    BLACK = (0, 0, 0)

    YELLOW = (255, 255, 0)
    GREEN = (100, 255, 100)
    RED = (255, 100, 100)
    PINK = (255, 100, 255)
    AQUA = (100, 255, 255)


class SMValues:
    SM_1_POS = pg.Vector2(20, 100)
    SM_2_POS = pg.Vector2(20, 230)
    SM_3_POS = pg.Vector2(20, 360)
    SM_4_POS = pg.Vector2(20, 490)

    SM_1_COL = Colours.GREEN
    SM_2_COL = Colours.PINK
    SM_3_COL = Colours.AQUA
    SM_4_COL = Colours.RED
