import math
import time

from constants import *
from interactable import Button, ButtonToggle, BTNOperation, Input, InputRange, InputRangeH, InputOperation


def v(v=0):
    pass


class ModalPage:
    def __init__(self, game, page_num):
        self.game = game
        self.pos = Vec2()
        self.page_num = page_num
        self.col = getattr(SMValues, f'SM_COL_{self.page_num}')

        self.sm_buttons = []
        self.sine_modals = {}

        # generate n (1 to 4) properties: sm_n, col_n & btn
        self.begin_n = 1 + ((page_num - 1) * 4)
        for i, modal_n in enumerate(range(self.begin_n, self.begin_n + 4), 1):
            sm_attr, col_attr = f'sm_{i}', f'col_{i}'
            div = 1 - (.15 * (i - 1))
            setattr(self, col_attr, (self.col[0] * div, self.col[1] * div, self.col[2] * div))
            setattr(self, sm_attr, None)
            self.sm_buttons.append(Button(Texts.NEW_SINE, getattr(SMValues, f'SM_{i}_POS'), BTNOperation(self.add_sine, None, modal_n), colour=getattr(self, col_attr), text_size=20, outline=2, margin=15))

    def get_sm_dic(self):
        return {
            self.begin_n: [self.sm_1.__str__(), SMValues.SM_1_POS, self.col_1],
            self.begin_n + 1: [self.sm_2.__str__(), SMValues.SM_2_POS, self.col_2],
            self.begin_n + 2: [self.sm_3.__str__(), SMValues.SM_3_POS, self.col_3],
            self.begin_n + 3: [self.sm_4.__str__(), SMValues.SM_4_POS, self.col_4]
        }

    def key_input(self, key):
        for sm in self.sine_modals.values():
            sm.key_input(key)

    def mouse_down(self):
        for btn in self.sm_buttons:
            btn.perform_operation()
        for sm in self.sine_modals.values():
            sm.mouse_down()

    def mouse_up(self):
        for sm in self.sine_modals.values():
            sm.mouse_up()

    def add_sine(self, sine_num):
        sm, pos, col = self.get_sm_dic()[sine_num]
        setattr(self, sm, SineModal(self.game, pos, sine_num, col, self.col))
        self.sine_modals[sine_num] = getattr(self, sm)
        self.sm_buttons[sine_num - self.begin_n].set_hidden(True)

    def del_sine(self, sine_num):
        sm, pos, col = self.get_sm_dic()[sine_num]
        setattr(self, sm, None)
        self.sine_modals[sine_num].clear_sine()
        self.sine_modals.pop(sine_num)
        self.sm_buttons[sine_num - self.begin_n].set_hidden(False)

    def update(self):
        for sm in self.sine_modals.values():
            sm.update()

    def render(self, screen: pg.Surface):
        for btn in self.sm_buttons:
            btn.render(screen)
        for sm in self.sine_modals.values():
            sm.render(screen)


class SineModal:
    def __init__(self, game, pos: Vec2, value, colour=Colours.YELLOW, input_colour=None, circle=True):
        self.game = game
        self.value = value
        self.pos = pos
        self.size = Vec2(GameValues.MODAL_WIDTH, GameValues.MODAL_HEIGHT)
        self.colour = colour
        self.input_colour = colour if input_colour is None else input_colour
        self.screen = pg.Surface(self.size)
        self.paused = False
        self.paused_time = 0

        self.amp = 0
        self.freq = 0
        self.phase = 0

        if circle:
            margin = 10
            self.sine_circle = SineCircle(self, Vec2(pos.x + self.size.x + margin, pos.y))

        common_kw = {'colour': self.input_colour, 'mouse_offset': pos, 'text_size': 15}
        self.name_inpt = Input('', Vec2(6, -15), InputOperation(v),
                               default_val=Texts.GENERATOR + str(value), bg_col=Colours.BG_COL, max_value_chars=15, **common_kw)
        self.amp_inpt = InputRangeH(Texts.AMP, Vec2(10, 30), InputOperation(self.set_amp),
                                    default_val=GameValues.MAX_AMP / 2, min_val=GameValues.MIN_AMP, max_val=GameValues.MAX_AMP, line_length=97, thumb_radius=5, update_live=True, **common_kw)
        self.freq_inpt = InputRangeH(Texts.FREQ, Vec2(10, 60), InputOperation(self.set_freq),
                                     default_val=1, min_val=GameValues.MIN_FREQ, max_val=GameValues.MAX_FREQ, line_length=99, thumb_radius=5, update_live=True, **common_kw)
        self.phase_inpt = InputRangeH(Texts.PHASE, Vec2(10, 90), InputOperation(self.set_phase),
                                      default_val=GameValues.MIN_PHASE, min_val=GameValues.MIN_PHASE, max_val=GameValues.MAX_PHASE, line_length=87, thumb_radius=5, update_live=True, **common_kw)
        self.all_inpts = [self.name_inpt, self.amp_inpt, self.freq_inpt, self.phase_inpt]

        self.clear_btn = Button(Texts.CLEAR, Vec2(188, 55), BTNOperation(self.clear_sine), colour=Colours.LIGHT_GREY, text_size=15, outline=2, mouse_offset=pos, override_size=Vec2(21, 21))
        self.pause_btn = ButtonToggle(Texts.ON, Vec2(188, 85), BTNOperation(self.toggle_pause), colour=Colours.GREEN, toggled_col=Colours.LIGHT_GREY, toggle_col=Colours.LIGHT_GREY, text_size=15, toggled_text=Texts.OFF, outline=2, mouse_offset=pos)
        self.del_btn = Button(Texts.CLOSE, Vec2(192, 0), BTNOperation(self.del_modal), text_size=11, outline=2, colour=Colours.RED, override_size=Vec2(18, 16), mouse_offset=pos)
        self.all_btns = [self.clear_btn, self.pause_btn, self.del_btn]

    def del_modal(self):
        event = pg.event.Event(CustomEvents.DEL_MODAL, num=self.value)
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
        for btn in self.all_btns:
            btn.perform_operation()

    def toggle_pause(self, value=None):
        p = self.paused if value is None else not bool(value)
        self.paused = not p
        self.amp_inpt.set_active(p)
        self.freq_inpt.set_active(p)
        self.phase_inpt.set_active(p)
        self.pause_btn.toggled = self.paused

    def clear_sine(self):
        event = pg.event.Event(CustomEvents.CLEAR_MODAL, num=self.value)
        pg.event.post(event)

    def set_amp(self, val):
        self.amp = int(val)

    def set_freq(self, val):
        self.freq = int(val)

    def set_phase(self, val):
        self.phase = int(val)

    def get_phase(self):
        return self.phase / self.game.phase_div

    def get_sin(self, amp=None, cos=False):
        a = self.amp if amp is None else amp
        f = self.freq
        p = self.get_phase()
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
        for btn in self.all_btns:
            btn.render(self.screen)

        if getattr(self, 'sine_circle', None):
            self.sine_circle.render(screen)

        screen.blit(self.screen, self.pos)


class SineCircle:
    def __init__(self, modal: SineModal, pos: Vec2):
        self.modal = modal
        self.pos = pos
        self.size = Vec2(GameValues.MODAL_WIDTH_SMALL, GameValues.MODAL_HEIGHT)
        self.rect = pg.Rect(self.pos, self.size)
        self.circle_centre = Vec2(self.rect.center[0] - (GameValues.MODAL_WIDTH_SMALL - GameValues.MODAL_HEIGHT) / 2, self.rect.center[1])
        self.font = pg.font.SysFont(GameValues.FONT, 13)

    def get_radius(self):
        perc = (self.modal.amp - GameValues.MIN_AMP) / (GameValues.MAX_AMP - GameValues.MIN_AMP)
        amp = GameValues.MIN_RADIUS + (perc * (GameValues.MAX_RADIUS - GameValues.MIN_RADIUS))
        return amp

    def get_sin(self, rad):
        return self.modal.get_sin(rad - 1)

    def get_cos(self, rad):
        return self.modal.get_sin(amp=rad - 1, cos=True)

    def render(self, screen: pg.Surface):
        poi = 3
        cent = self.circle_centre
        poi_pos = Vec2(cent.x - math.floor(poi / 2), cent.y - math.floor(poi / 2))
        pg.draw.rect(screen, self.modal.colour, self.rect, 2)

        rad = self.get_radius()
        sin = self.get_sin(rad)
        cos = self.get_cos(rad)
        sin_pos = Vec2((cent.x, cent.y + sin))
        cos_pos = Vec2((cent.x + cos, cent.y))
        hyp_pos = Vec2(cent.x + cos, cent.y + sin)

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
        screen.blit(self.font.render(str('{:.1f}'.format(sin)), True, Colours.GREEN), Vec2(x, self.pos.y + 10))
        screen.blit(self.font.render(str('{:.1f}'.format(cos)), True, Colours.AQUA), Vec2(x, self.pos.y + 45))
        theta = math.atan(sin_pos.magnitude() / cos_pos.magnitude())
        screen.blit(self.font.render(str('{:.3f}'.format(theta)), True, Colours.WHITE), Vec2(x, self.pos.y + 80))
        screen.blit(self.font.render(str('{:.1f}'.format(math.degrees(theta))), True, Colours.WHITE), Vec2(x, self.pos.y + 95))
