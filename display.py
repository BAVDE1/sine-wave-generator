from constants import *


class SineDisplay:
    def __init__(self, game, pos: pg.Vector2):
        self.game = game
        self.pos = pos
        self.size = pg.Vector2(GameValues.DISPLAY_WIDTH, GameValues.DISPLAY_HEIGHT)
        self.rect = pg.Rect(pg.Vector2(0, 0), self.size)
        self.screen = pg.Surface(self.size)
        self.sm_screens = {i: dict(last_pos=0, screen_a=pg.Surface(self.size, pg.SRCALPHA), screen_b=None) for i in range(1, 5)}

        self.granularity = 20

        self.pixels_per_frame = 1

    def render(self, screen: pg.Surface):
        self.screen.fill(Colours.BG_COL_LIGHT)

        # render lines
        pg.draw.line(self.screen, Colours.DARK_GREY, (0, self.rect.center[1]), (GameValues.DISPLAY_WIDTH, self.rect.center[1]), 3)
        pg.draw.line(self.screen, Colours.DARKER_GREY, (0, self.rect.center[1] * .5), (GameValues.DISPLAY_WIDTH, self.rect.center[1] * .5), 3)
        pg.draw.line(self.screen, Colours.DARKER_GREY, (0, self.rect.center[1] * 1.5), (GameValues.DISPLAY_WIDTH, self.rect.center[1] * 1.5), 3)
        pg.draw.line(self.screen, Colours.GREY, (GameValues.DISPLAY_WIDTH - self.granularity, 0), (GameValues.DISPLAY_WIDTH - self.granularity, GameValues.DISPLAY_HEIGHT), 3)
        pg.draw.rect(self.screen, Colours.WHITE, self.rect, 3)

        # sines
        for num, modal in self.game.sine_modals.items():
            dic = self.sm_screens[num]
            a, b = 'screen_a', 'screen_b'
            screen_on, screen_empty = [a, b] if dic[a] is not None else [b, a]
            new_sc = pg.Surface(self.size, pg.SRCALPHA)

            # draw
            rect = pg.Rect(self.rect.midright[0] - 10, self.rect.midright[1] + modal.get_sin(), 2, 2)
            pg.draw.rect(dic[screen_on], modal.colour, rect)
            # pg.draw.rect(dic[screen_on], Colours.GREEN, pg.Rect(0, 0, self.size.x, self.size.y), 1)

            # move
            moved_pos = (0 - self.pixels_per_frame, 0)
            self.screen.blit(dic[screen_on], moved_pos)
            dic[screen_empty] = pg.Surface(self.size, pg.SRCALPHA)
            dic[screen_empty].blit(dic[screen_on], moved_pos)
            dic[screen_on] = None

        screen.blit(self.screen, self.pos)
