import time

from interactable import BTNOperation, Button, ButtonToggle, Input, InputRange, InputOperation, Collection
from constants import *
from modal import SineModal, ModalPage
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
        self.modal_pages = {i: ModalPage(self, i) for i in range(1, GameValues.PAGE_NUMBERS + 1)}
        self.phase_div = 1
        self.on_page = 1
        self.all_btns = []
        self.pg_btns = []

        # add page buttons
        pg_btn_y, override_siz, text_siz = 620, pg.Vector2(21, 22), 16
        for i in range(1, GameValues.PAGE_NUMBERS + 1):
            btn = ButtonToggle(f' {i} ', pg.Vector2(25 * i, 620), BTNOperation(self.change_page, num=i),
                               text_size=text_siz, colour=Colours.GREY, outline=2, toggle_col=Colours.WHITE,
                               toggled_col=Colours.WHITE, override_size=override_siz)
            btn.set_toggle(i == 1)
            self.all_btns.append(btn)
            self.pg_btns.append(btn)
        render_page_btn = ButtonToggle(' Render: page ', pg.Vector2(225, pg_btn_y), BTNOperation(self.toggle_render_type),
                                       text_size=text_siz, colour=Colours.LIGHT_GREY, outline=2, toggle_col=Colours.LIGHT_GREY, toggled_text=' Render: all ')
        self.all_btns.append(render_page_btn)
        self.render_all = False

        kwargs = {'update_live': True, 'text_size': 18}
        self.gran_inpt = InputRange(Texts.GRANULARITY, pg.Vector2(1100, 15), InputOperation(self.set_granularity), default_val=GameValues.MIN_GRAN, min_val=GameValues.MIN_GRAN, max_val=GameValues.MAX_GRAN, **kwargs)
        self.point_inpt = InputRange(Texts.POINT_SIZE, pg.Vector2(950, 15), InputOperation(self.set_point_size), default_val=2, min_val=GameValues.MIN_POINT_SIZ, max_val=GameValues.MAX_POINT_SIZ, **kwargs)
        self.line_inpt = InputRange(Texts.LINE_SIZE, pg.Vector2(800, 15), InputOperation(self.set_line_size), default_val=3, min_val=GameValues.MIN_LINE_SIZ, max_val=GameValues.MAX_LINE_SIZ, **kwargs)
        self.ppf_inpt = InputRange(Texts.PPF, pg.Vector2(650, 15), InputOperation(self.set_ppf), default_val=1, min_val=GameValues.MIN_PPF, max_val=GameValues.MAX_PPF, **kwargs)
        self.phase_div_inpt = InputRange(Texts.PHASE_DIV, pg.Vector2(100, 15), InputOperation(self.set_phase_div), default_val=GameValues.MIN_PHASE_DIV, min_val=GameValues.MIN_PHASE_DIV, max_val=GameValues.MAX_PHASE_DIV, **kwargs)
        self.inputs = [self.gran_inpt, self.point_inpt, self.line_inpt, self.ppf_inpt, self.phase_div_inpt]

    def events(self):
        for event in pg.event.get():
            # custom
            if event.type == CustomEvents.DEL_MODAL:
                self.get_active_page().del_sine(event.num)
            if event.type == CustomEvents.CLEAR_MODAL:
                self.sine_display.clear_screen(event.num)

            # key input
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                for inpt in self.inputs:
                    inpt.key_input(event.key)
                self.get_active_page().key_input(event.key)

            if event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

            # close game
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.running = False

            # mouse
            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                for inpt in self.inputs:
                    inpt.mouse_down()
                for btn in self.all_btns:
                    btn.perform_operation()
                self.get_active_page().mouse_down()

            if event.type == pg.MOUSEBUTTONUP and not pg.mouse.get_pressed()[0]:
                for inpt in self.inputs:
                    inpt.mouse_up()
                self.get_active_page().mouse_up()

    def change_page(self, num):
        self.on_page = num
        for i, btn in enumerate(self.pg_btns):
            btn.set_toggle(i + 1 == num)

    def toggle_render_type(self):
        self.render_all = not self.render_all
        print(self.render_all)

    def get_active_page(self):
        return self.modal_pages[self.on_page]

    def get_active_pages(self):
        pgs = []
        if not self.render_all:  # one page
            pgs.append(self.get_active_page())
        else:  # all pages
            for mp in self.modal_pages.values():
                pgs.append(mp)
        return pgs

    def get_active_sine_modals(self):
        return {
            i: sm for mp in self.get_active_pages() for i, sm in mp.sine_modals.items()
        }

    def update(self):
        for inpt in self.inputs:
            inpt.update()
        for mp in self.modal_pages.values():
            mp.update()

    def set_phase_div(self, val):
        self.phase_div = val

    def set_granularity(self, val):
        self.sine_display.granularity = val

    def set_point_size(self, val):
        self.sine_display.point_size = val

    def set_line_size(self, val):
        self.sine_display.line_thickness = val

    def set_ppf(self, val):
        self.sine_display.pixels_per_frame = val

    def render(self):
        self.final_screen.fill(Colours.BG_COL)
        self.canvas_screen.fill(Colours.BG_COL)

        # render here
        for inpt in self.inputs:
            inpt.render(self.canvas_screen)
        for btn in self.all_btns:
            btn.render(self.canvas_screen)
        self.get_active_page().render(self.canvas_screen)
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
