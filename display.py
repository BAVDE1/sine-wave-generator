from constants import *


class SineDisplay:
    def __init__(self, game, pos: pg.Vector2):
        self.game = game
        self.pos = pos
        self.size = pg.Vector2(GameValues.DISPLAY_WIDTH, GameValues.DISPLAY_HEIGHT)
        self.rect = pg.Rect(pg.Vector2(0, 0), self.size)
        self.screen = pg.Surface(self.size)
        self.sm_screens = {i: dict(paused=False, last_pos=0, screen_a=self.get_default_screen(), screen_b=None) for i in range(1, 5)}

        self.granularity = 0
        self.point_size = 2

        self.pixels_per_frame = 1

    def get_default_screen(self):
        return pg.Surface(self.size, pg.SRCALPHA)

    def get_screens(self, num):
        """ Returns on screen and empty screen keys """
        a, b = 'screen_a', 'screen_b'
        return [a, b] if self.sm_screens[num][a] is not None else [b, a]

    def toggle_pause(self, num, paused):
        self.sm_screens[num]['paused'] = paused

    def clear_screen(self, num):
        self.sm_screens[num][self.get_screens(num)[0]] = self.get_default_screen()

    def render(self, screen: pg.Surface):
        self.screen.fill(Colours.BG_COL_LIGHT)

        # render lines
        pg.draw.line(self.screen, Colours.DARK_GREY, (0, self.rect.center[1]), (GameValues.DISPLAY_WIDTH, self.rect.center[1]), 3)
        pg.draw.line(self.screen, Colours.DARKER_GREY, (0, self.rect.center[1] * .5), (GameValues.DISPLAY_WIDTH, self.rect.center[1] * .5), 3)
        pg.draw.line(self.screen, Colours.DARKER_GREY, (0, self.rect.center[1] * 1.5), (GameValues.DISPLAY_WIDTH, self.rect.center[1] * 1.5), 3)
        pg.draw.line(self.screen, Colours.GREY, (GameValues.DISPLAY_WIDTH - self.granularity, 0), (GameValues.DISPLAY_WIDTH - self.granularity, GameValues.DISPLAY_HEIGHT), 3)

        # sines
        for num, modal in self.game.sine_modals.items():
            dic = self.sm_screens[num]
            lp = 'last_pos'
            last_pos = dic[lp]
            screen_on, screen_empty = self.get_screens(num)

            # draw
            if self.granularity <= last_pos:
                rect = pg.Rect(self.rect.midright[0] - self.point_size, self.rect.midright[1] + modal.get_sin(), self.point_size, self.point_size)
                pg.draw.rect(dic[screen_on], modal.colour, rect)
                dic[lp] = 0

            # move
            moved_pos = pg.Vector2(0 if dic['paused'] else -self.pixels_per_frame, 0)
            self.screen.blit(dic[screen_on], moved_pos)
            dic[screen_empty] = self.get_default_screen()
            dic[screen_empty].blit(dic[screen_on], moved_pos)
            dic[screen_on] = None
            dic[lp] -= moved_pos.x

        pg.draw.rect(self.screen, Colours.WHITE, self.rect, 3)
        screen.blit(self.screen, self.pos)
