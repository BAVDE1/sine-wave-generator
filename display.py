from constants import *


class SineDisplay:
    def __init__(self, game, pos: Vec2):
        self.game = game
        self.pos = pos
        self.size = Vec2(GameValues.DISPLAY_WIDTH, GameValues.DISPLAY_HEIGHT)
        self.rect = pg.Rect(Vec2(0, 0), self.size)
        self.screen = pg.Surface(self.size)
        self.sm_screens = {
            i: dict(last_pos=Vec2(0, 0), screen=self.get_default_screen()) for i in range(1, 1 + (GameValues.PAGE_NUMBERS * 4))
        }

        self.granularity = 0
        self.point_size = 2
        self.line_thickness = 2
        self.pixels_per_frame = 1

    def get_default_screen(self):
        return pg.Surface(self.size, pg.SRCALPHA)

    def clear_screen(self, num):
        self.sm_screens[num]['screen'] = self.get_default_screen()
        self.sm_screens[num]['last_pos'] = Vec2(0, 0)

    def render(self, screen: pg.Surface):
        self.screen.fill(Colours.BG_COL_LIGHT)

        # render lines
        pg.draw.line(self.screen, Colours.DARK_GREY, (0, self.rect.center[1]), (GameValues.DISPLAY_WIDTH, self.rect.center[1]), 3)
        pg.draw.line(self.screen, Colours.DARKER_GREY, (0, self.rect.center[1] * .5), (GameValues.DISPLAY_WIDTH, self.rect.center[1] * .5), 3)
        pg.draw.line(self.screen, Colours.DARKER_GREY, (0, self.rect.center[1] * 1.5), (GameValues.DISPLAY_WIDTH, self.rect.center[1] * 1.5), 3)
        pg.draw.line(self.screen, Colours.DARK_GREY, (GameValues.DISPLAY_WIDTH - self.pixels_per_frame, 0), (GameValues.DISPLAY_WIDTH - self.pixels_per_frame, GameValues.DISPLAY_HEIGHT), 2)
        pg.draw.line(self.screen, Colours.GREY, (GameValues.DISPLAY_WIDTH - self.granularity, 0), (GameValues.DISPLAY_WIDTH - self.granularity, GameValues.DISPLAY_HEIGHT), 3)

        # sines
        for num, modal in self.game.get_sine_modals().items():
            dic = self.sm_screens[num]
            lp = 'last_pos'
            sc = 'screen'

            # draw
            if self.granularity <= dic[lp].x:
                rect = pg.Rect(self.rect.midright[0] - self.point_size, self.rect.midright[1] + modal.get_sin(), self.point_size, self.point_size)
                pg.draw.rect(dic[sc], modal.colour, rect)  # point
                # line
                if dic[lp].y != 0:
                    ps = self.point_size / 2
                    pg.draw.line(dic[sc], modal.colour, (GameValues.DISPLAY_WIDTH - dic[lp].x - ps, dic[lp].y), rect.center, self.line_thickness)
                dic[lp] = Vec2(0, rect.center[1])

            # move
            moved_pos = Vec2(0 if modal.paused else -self.pixels_per_frame, 0)
            self.screen.blit(dic[sc], moved_pos)
            next_scrn = self.get_default_screen()
            next_scrn.blit(dic[sc], moved_pos)
            dic[sc] = next_scrn
            dic[lp].x -= moved_pos.x

        pg.draw.rect(self.screen, Colours.WHITE, self.rect, 3)
        screen.blit(self.screen, self.pos)
