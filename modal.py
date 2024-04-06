import math
import time

import pygame as pg
from constants import *
from interactable import Button, ButtonToggle, BTNOperation, Input, InputRange, InputRangeH, InputOperation


def v(v=0):
    print(v)


class SineModal:
    def __init__(self, pos: pg.Vector2, num, colour=Colours.YELLOW):
        self.pos = pos
        self.size = pg.Vector2(220, 120)
        self.colour = colour

        txt_size = 15
        self.name_inpt = Input('', pg.Vector2(pos.x + 6, pos.y - txt_size), InputOperation(v),
                               default_val='generator ' + str(num), bg_col=Colours.BG_COL, text_size=txt_size, max_value_chars=15)
        self.amp_inpt = InputRangeH('amp', pg.Vector2(pos.x + 10, pos.y + 30), InputOperation(v),
                                    text_size=txt_size, min_val=1, max_val=50, line_length=80, thumb_radius=5)
        self.freq_inpt = InputRangeH('freq', pg.Vector2(pos.x + 10, pos.y + 60), InputOperation(v),
                                     text_size=txt_size, min_val=1, max_val=10, line_length=80, thumb_radius=5)
        self.phase_inpt = InputRangeH('phase', pg.Vector2(pos.x + 10, pos.y + 90), InputOperation(v),
                                      text_size=txt_size, default_val=0, min_val=0, max_val=100, line_length=80, thumb_radius=5)
        self.all_inpts = [self.name_inpt, self.amp_inpt, self.freq_inpt, self.phase_inpt]

        self.pause_btn = ButtonToggle(' O ', pg.Vector2(pos.x + 185, pos.y + 85), BTNOperation(v),
                                      colour=Colours.GREEN, toggled_col=Colours.LIGHT_GREY, toggle_col=Colours.LIGHT_GREY, text_size=txt_size, toggled_text='  |  ', outline=2)
        self.del_btn = Button(' X ', pg.Vector2(pos.x + 192, pos.y), BTNOperation(v),
                              text_size=11, outline=2, colour=Colours.RED, override_size=pg.Vector2(18, 16))

    def get_rect(self):
        return pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

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
        # print(self.get_sin())

    def render(self, screen: pg.Surface):
        pg.draw.rect(screen, self.colour, self.get_rect(), 2)
        for inpt in self.all_inpts:
            inpt.render(screen)
        self.pause_btn.render(screen)
        self.del_btn.render(screen)
