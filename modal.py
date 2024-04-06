import math
import time

from constants import *
from interactable import Button, ButtonToggle, BTNOperation, Input, InputRange, InputRangeH, InputOperation


def v(v=0):
    pass


class SineModal:
    def __init__(self, pos: pg.Vector2, num, colour=Colours.YELLOW):
        self.num = num
        self.pos = pos
        self.size = pg.Vector2(220, 120)
        self.colour = colour
        self.screen = pg.Surface(self.size)
        self.paused = False

        common_kw = {'colour': colour, 'mouse_offset': pos, 'text_size': 15}
        self.name_inpt = Input('', pg.Vector2(6, -15), InputOperation(v),
                               default_val=Texts.GENERATOR + str(num), bg_col=Colours.BG_COL, max_value_chars=15, **common_kw)
        self.amp_inpt = InputRangeH(Texts.AMP, pg.Vector2(10, 30), InputOperation(v),
                                    min_val=GameValues.MIN_AMP, max_val=GameValues.MAX_AMP, line_length=97, thumb_radius=5, **common_kw)
        self.freq_inpt = InputRangeH(Texts.FREQ, pg.Vector2(10, 60), InputOperation(v),
                                     min_val=GameValues.MIN_FREQ, max_val=GameValues.MAX_FREQ, line_length=99, thumb_radius=5, **common_kw)
        self.phase_inpt = InputRangeH(Texts.PHASE, pg.Vector2(10, 90), InputOperation(v),
                                      default_val=GameValues.MIN_PHASE, min_val=GameValues.MIN_PHASE, max_val=GameValues.MAX_PHASE, line_length=75, thumb_radius=5, **common_kw)
        self.all_inpts = [self.name_inpt, self.amp_inpt, self.freq_inpt, self.phase_inpt]

        self.pause_btn = ButtonToggle(Texts.ON, pg.Vector2(185, 85), BTNOperation(self.toggle_pause),
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

    def get_sin(self):
        a = int(self.amp_inpt.value)
        f = int(self.freq_inpt.value)
        p = int(self.phase_inpt.value)
        t = time.time()
        return a * math.sin((f * t) + p)

    def update(self):
        """ Every frame """
        self.amp_inpt.update()
        self.freq_inpt.update()
        self.phase_inpt.update()

    def render(self, screen: pg.Surface):
        self.screen.fill(Colours.BG_COL)

        # render
        pg.draw.rect(self.screen, self.colour, self.get_rect(), 2)
        for inpt in self.all_inpts:
            inpt.render(self.screen)
        self.pause_btn.render(self.screen)
        self.del_btn.render(self.screen)

        screen.blit(self.screen, self.pos)
