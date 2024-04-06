

def get_middle(pos, width_1, width_2) -> int:
    return (pos + (width_1 / 2)) - (width_2 / 2)


class Texts:
    GENERATOR = 'generator '
    AMP = 'amp'
    FREQ = 'freq'
    PHASE = 'phase'
    ON = ' O '
    OFF = '  |  '
    CLOSE = ' X '


class GameValues:
    FONT = "Times New Roman"

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    RES_MUL = 1

    MIN_AMP = 1
    MIN_FREQ = 1
    MIN_PHASE = 0
    MAX_AMP = 50
    MAX_FREQ = 10
    MAX_PHASE = 100


class Colours:
    BG_COL = (0, 10, 10)
    WHITE = (255, 255, 255)
    GREEN = (100, 255, 100)
    RED = (255, 100, 100)
    LIGHT_GREY = (150, 150, 150)
    GREY = (100, 100, 100)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
