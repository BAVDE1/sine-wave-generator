import math
import time

from constants import *
from interactable import Button, ButtonToggle, BTNOperation, Input, InputRange, InputRangeH, InputOperation


def v(v=0):
    pass


class SineModal:
    def __init__(self, game, pos: pg.Vector2, num, colour=Colours.YELLOW):
        self.game = game
        self.num = num
        self.pos = pos
        self.size = pg.Vector2(GameValues.MODAL_WIDTH, GameValues.MODAL_HEIGHT)
        self.colour = colour
        self.screen = pg.Surface(self.size)
        self.paused = False
        self.paused_time = 0
        self.old_freq = GameValues.MIN_FREQ

        margin = 10
        self.sine_circle = SineCircle(self, pg.Vector2(pos.x + self.size.x + margin, pos.y))

        common_kw = {'colour': colour, 'mouse_offset': pos, 'text_size': 15}
        self.name_inpt = Input('', pg.Vector2(6, -15), InputOperation(v),
                               default_val=Texts.GENERATOR + str(num), bg_col=Colours.BG_COL, max_value_chars=15, **common_kw)
        self.amp_inpt = InputRangeH(Texts.AMP, pg.Vector2(10, 30), InputOperation(v),
                                    default_val=GameValues.MAX_AMP / 2, min_val=GameValues.MIN_AMP, max_val=GameValues.MAX_AMP, line_length=97, thumb_radius=5, **common_kw)
        self.freq_inpt = InputRangeH(Texts.FREQ, pg.Vector2(10, 60), InputOperation(v),
                                     default_val=1, min_val=self.old_freq, max_val=GameValues.MAX_FREQ, line_length=99, thumb_radius=5, **common_kw)
        self.phase_inpt = InputRangeH(Texts.PHASE, pg.Vector2(10, 90), InputOperation(v),
                                      default_val=GameValues.MIN_PHASE, min_val=GameValues.MIN_PHASE, max_val=GameValues.MAX_PHASE, line_length=87, thumb_radius=5, **common_kw)
        self.all_inpts = [self.name_inpt, self.amp_inpt, self.freq_inpt, self.phase_inpt]

        self.pause_btn = ButtonToggle(Texts.ON, pg.Vector2(188, 85), BTNOperation(self.toggle_pause),
                                      colour=Colours.GREEN, toggled_col=Colours.LIGHT_GREY, toggle_col=Colours.LIGHT_GREY, text_size=15, toggled_text=Texts.OFF, outline=2, mouse_offset=pos)
        self.del_btn = Button(Texts.CLOSE, pg.Vector2(192, 0), BTNOperation(self.del_modal),
                              text_size=11, outline=2, colour=Colours.RED, override_size=pg.Vector2(18, 16), mouse_offset=pos)

    def del_modal(self):
        event = pg.event.Event(CustomEvents.DEL_MODAL, num=self.num)
        pg.event.post(event)

    def get_rect(self):
        return pg.Rect(0, 0, self.size.x, self.size.y)

    def key_input(self, key):
        for inpt in self.all_inpts:
            inpt.key_input(key)

    def mouse_up(self):
        self.amp_inpt.mouse_up()
        self.freq_inpt.mouse_up()
        self.phase_inpt.mouse_up()

    def mouse_down(self):
        for inpt in self.all_inpts:
            inpt.mouse_down()
        self.pause_btn.perform_operation()
        self.del_btn.perform_operation()

    def toggle_pause(self):
        p = self.paused
        self.paused = not p
        self.amp_inpt.set_active(p)
        self.freq_inpt.set_active(p)
        self.phase_inpt.set_active(p)

    def get_amp(self):
        return int(self.amp_inpt.get_value())

    def get_freq(self):
        return int(self.freq_inpt.get_value())

    def get_sin(self, amp=None, cos=False):
        a = self.get_amp() if amp is None else amp
        f = self.get_freq()
        p = int(self.phase_inpt.get_value())
        t = time.time() - self.paused_time
        return a * math.sin((f * t) + p) if not cos else a * math.cos((f * t) + p)

    def update(self):
        """ Every frame """
        self.amp_inpt.update()
        self.freq_inpt.update()
        self.phase_inpt.update()

        if self.paused:
            self.paused_time += self.game.delta_time

    def render(self, screen: pg.Surface):
        self.screen.fill(Colours.BG_COL)

        # render
        pg.draw.rect(self.screen, self.colour, self.get_rect(), 2)
        for inpt in self.all_inpts:
            inpt.render(self.screen)
        self.pause_btn.render(self.screen)
        self.del_btn.render(self.screen)

        self.sine_circle.render(screen)

        screen.blit(self.screen, self.pos)


class SineCircle:
    def __init__(self, modal: SineModal, pos: pg.Vector2):
        self.modal = modal
        self.pos = pos
        self.size = pg.Vector2(GameValues.MODAL_WIDTH_SMALL, GameValues.MODAL_HEIGHT)
        self.rect = pg.Rect(self.pos, self.size)
        self.circle_centre = pg.Vector2(self.rect.center[0] - (GameValues.MODAL_WIDTH_SMALL - GameValues.MODAL_HEIGHT) / 2, self.rect.center[1])
        self.font = pg.font.SysFont(GameValues.FONT, 13)

    def get_radius(self):
        perc = (self.modal.get_amp() - GameValues.MIN_AMP) / (GameValues.MAX_AMP - GameValues.MIN_AMP)
        amp = GameValues.MIN_RADIUS + (perc * (GameValues.MAX_RADIUS - GameValues.MIN_RADIUS))
        return amp

    def get_sin(self, rad):
        return self.modal.get_sin(rad - 1)

    def get_cos(self, rad):
        return self.modal.get_sin(amp=rad - 1, cos=True)

    def render(self, screen: pg.Surface):
        poi = 3
        cent = self.circle_centre
        poi_pos = pg.Vector2(cent.x - math.floor(poi / 2), cent.y - math.floor(poi / 2))
        pg.draw.rect(screen, self.modal.colour, self.rect, 2)

        rad = self.get_radius()
        sin = self.get_sin(rad)
        cos = self.get_cos(rad)
        sin_pos = pg.Vector2((cent.x, cent.y + sin))
        cos_pos = pg.Vector2((cent.x + cos, cent.y))
        hyp_pos = pg.Vector2(cent.x + cos, cent.y + sin)

        # guidelines
        pg.draw.circle(screen, Colours.DARKER_GREY, cent, rad)  # inner rad bg
        pg.draw.line(screen, Colours.DARK_GREY, (cent.x + GameValues.MAX_RADIUS, cent.y), (cent.x - GameValues.MAX_RADIUS, cent.y))
        pg.draw.line(screen, Colours.DARK_GREY, (cent.x, cent.y + GameValues.MAX_RADIUS), (cent.x, cent.y - GameValues.MAX_RADIUS))
        pg.draw.circle(screen, Colours.DARK_GREY, cent, GameValues.MIN_RADIUS, 1)
        pg.draw.circle(screen, Colours.DARK_GREY, cent, GameValues.MAX_RADIUS, 1)

        # hyp lines
        pg.draw.line(screen, Colours.LIGHT_GREY, hyp_pos, sin_pos)
        pg.draw.line(screen, Colours.LIGHT_GREY, hyp_pos, cos_pos)
        # sin
        pg.draw.line(screen, Colours.GREEN, cent, sin_pos)
        # cos
        pg.draw.line(screen, Colours.AQUA, cent, cos_pos)
        # hyp
        pg.draw.line(screen, Colours.WHITE, cent, hyp_pos)
        # amp
        pg.draw.circle(screen, Colours.WHITE, cent, rad, 1)
        # centre dot
        pg.draw.rect(screen, Colours.WHITE, pg.Rect(poi_pos, (poi, poi)))

        # text
        x = self.pos.x + 122
        screen.blit(self.font.render(str('{:.1f}'.format(sin)), True, Colours.GREEN), pg.Vector2(x, self.pos.y + 10))
        screen.blit(self.font.render(str('{:.1f}'.format(cos)), True, Colours.AQUA), pg.Vector2(x, self.pos.y + 45))
        theta = math.atan(sin_pos.magnitude() / cos_pos.magnitude())
        screen.blit(self.font.render(str('{:.3f}'.format(theta)), True, Colours.WHITE), pg.Vector2(x, self.pos.y + 80))
        screen.blit(self.font.render(str('{:.1f}'.format(math.degrees(theta))), True, Colours.WHITE), pg.Vector2(x, self.pos.y + 95))
