from constants import *


class SineDisplay:
    def __init__(self, game, pos: pg.Vector2):
        self.game = game
        self.pos = pos
        self.size = pg.Vector2(GameValues.DISPLAY_WIDTH, GameValues.DISPLAY_HEIGHT)
        self.rect = pg.Rect(pg.Vector2(0, 0), self.size)
        self.screen = pg.Surface(self.size)
        self.moving_screen = pg.Surface(self.size)

        self.granularity = 20

    def render(self, screen: pg.Surface):
        self.screen.fill(Colours.BG_COL_LIGHT)

        # render
        pg.draw.line(self.screen, Colours.DARK_GREY, (0, self.rect.center[1]), (GameValues.DISPLAY_WIDTH, self.rect.center[1]), 3)
        pg.draw.line(self.screen, Colours.DARKER_GREY, (0, self.rect.center[1] * .5), (GameValues.DISPLAY_WIDTH, self.rect.center[1] * .5), 3)
        pg.draw.line(self.screen, Colours.DARKER_GREY, (0, self.rect.center[1] * 1.5), (GameValues.DISPLAY_WIDTH, self.rect.center[1] * 1.5), 3)
        pg.draw.line(self.screen, Colours.GREY, (GameValues.DISPLAY_WIDTH - self.granularity, 0), (GameValues.DISPLAY_WIDTH - self.granularity, GameValues.DISPLAY_HEIGHT), 3)
        pg.draw.rect(self.screen, Colours.WHITE, self.rect, 3)

        screen.blit(self.screen, self.pos)
