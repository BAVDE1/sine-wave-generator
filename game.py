import time

from interactable import BTNOperation, Button, ButtonToggle, Input, InputRange, InputOperation, Collection
from constants import *
from modal import SineModal
from display import SineDisplay


def test(val=0):
    print('test', val)


class Game:
    def __init__(self):
        self.running = True
        self.fps = 60
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()
        self.last_frame = time.time()
        self.delta_time = time.time()

        self.canvas_screen = pg.Surface(pg.Vector2(GameValues.SCREEN_WIDTH, GameValues.SCREEN_HEIGHT))
        self.final_screen = pg.display.get_surface()

        self.sine_display = SineDisplay(self, pg.Vector2(430, 100))

        self.sm_1: SineModal | None = None
        self.sm_2: SineModal | None = None
        self.sm_3: SineModal | None = None
        self.sm_4: SineModal | None = None
        self.sine_modals = {}

        kwargs = {'text_size': 20, 'outline': 2, 'margin': 15}
        self.sm_1_btn = Button(Texts.NEW_SINE, SMValues.SM_1_POS, BTNOperation(self.add_sine, None, 1), colour=SMValues.SM_1_COL, **kwargs)
        self.sm_2_btn = Button(Texts.NEW_SINE, SMValues.SM_2_POS, BTNOperation(self.add_sine, None, 2), colour=SMValues.SM_2_COL, **kwargs)
        self.sm_3_btn = Button(Texts.NEW_SINE, SMValues.SM_3_POS, BTNOperation(self.add_sine, None, 3), colour=SMValues.SM_3_COL, **kwargs)
        self.sm_4_btn = Button(Texts.NEW_SINE, SMValues.SM_4_POS, BTNOperation(self.add_sine, None, 4), colour=SMValues.SM_4_COL, **kwargs)
        self.sm_buttons = [self.sm_1_btn, self.sm_2_btn, self.sm_3_btn, self.sm_4_btn]

        self.gran_inpt = InputRange(Texts.GRANULARITY, pg.Vector2(1100, 15), InputOperation(self.set_granularity),
                                    default_val=5, min_val=GameValues.MIN_GRAN, max_val=GameValues.MAX_GRAN, update_live=True, text_size=18)
        self.inputs = [self.gran_inpt]

    def events(self):
        for event in pg.event.get():
            # custom
            if event.type == CustomEvents.DEL_MODAL:
                self.del_sine(event.num)

            if event.type == CustomEvents.PAUSE_SINE:
                self.sine_display.toggle_pause(event.num, event.paused)

            # key input
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                for inpt in self.inputs:
                    inpt.key_input(event.key)
                for sm in self.sine_modals.values():
                    sm.key_input(event.key)

            if event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

            # close game
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.running = False

            # mouse
            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                for inpt in self.inputs:
                    inpt.mouse_down()
                for btn in self.sm_buttons:
                    btn.perform_operation()
                for sm in self.sine_modals.values():
                    sm.mouse_down()

            if event.type == pg.MOUSEBUTTONUP and not pg.mouse.get_pressed()[0]:
                for inpt in self.inputs:
                    inpt.mouse_up()
                for sm in self.sine_modals.values():
                    sm.mouse_up()

    def get_sm_dic(self):
        return {
            1: [self.sm_1.__str__(), SMValues.SM_1_POS, SMValues.SM_1_COL],
            2: [self.sm_2.__str__(), SMValues.SM_2_POS, SMValues.SM_2_COL],
            3: [self.sm_3.__str__(), SMValues.SM_3_POS, SMValues.SM_3_COL],
            4: [self.sm_4.__str__(), SMValues.SM_4_POS, SMValues.SM_4_COL]
        }

    def add_sine(self, sine_num):
        sm, pos, col = self.get_sm_dic()[sine_num]
        setattr(self, sm, SineModal(self, pos, sine_num, col))
        self.sine_modals[sine_num] = getattr(self, sm)
        self.sm_buttons[sine_num - 1].set_hidden(True)

    def del_sine(self, sine_num):
        sm, pos, col = self.get_sm_dic()[sine_num]
        setattr(self, sm, None)
        self.sine_modals.pop(sine_num)
        self.sm_buttons[sine_num - 1].set_hidden(False)
        self.sine_display.clear_screen(sine_num)

    def update(self):
        for inpt in self.inputs:
            inpt.update()
        for sm in self.sine_modals.values():
            sm.update()

    def set_granularity(self, val):
        self.sine_display.granularity = val

    def render(self):
        self.final_screen.fill(Colours.BG_COL)
        self.canvas_screen.fill(Colours.BG_COL)

        # render here
        for inpt in self.inputs:
            inpt.render(self.canvas_screen)
        for btn in self.sm_buttons:
            btn.render(self.canvas_screen)
        for sm in self.sine_modals.values():
            sm.render(self.canvas_screen)
        self.sine_display.render(self.canvas_screen)

        # final
        scaled = pg.transform.scale(self.canvas_screen, pg.Vector2(GameValues.SCREEN_WIDTH * GameValues.RES_MUL, GameValues.SCREEN_HEIGHT * GameValues.RES_MUL))
        self.final_screen.blit(scaled, pg.Vector2(0, 0))

        pg.display.flip()

    def main_loop(self):
        while self.running:
            self.delta_time = time.time() - self.last_frame
            self.last_frame = time.time()
            self.events()
            self.update()
            self.render()

            self.clock.tick(self.fps)
            pg.display.set_caption("{} - fps: {:.2f}".format("sine gen", self.clock.get_fps()))
