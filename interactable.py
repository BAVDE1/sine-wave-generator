import math

import pygame as pg
from constants import *


class BTNOperation:
    def __init__(self, function=None, collection=None, *args, **kwargs):
        if not function and not collection:
            raise ValueError("No function or collection given")
        if function and not callable(function):
            raise ValueError("The given function param is not callable.")
        if collection and not isinstance(collection, Collection):
            raise ValueError("The given collection is not of instance Collection")

        self.args = args
        self.kwargs = kwargs
        self.function = function
        self.collection = collection

    def perform_operation(self):
        if self.function:
            self.function(*self.args, **self.kwargs)
        if self.collection:
            self.collection.toggle()

    def __repr__(self):
        return f"BTNOperation({self.function.__name__ if self.function else self.collection}({self.args}, {self.kwargs}))"


class InputOperation:
    def __init__(self, function):
        if not callable(function):
            raise ValueError("The given function param is not callable.")
        self.function = function

    def perform_operation(self, value):
        self.function(value)

    def __repr__(self):
        return f"InputOperation({self.function.__name__})"


class Collection:
    """ A collection of buttons within a separate screen that can be toggled on and off """
    def __init__(self, pos: pg.Vector2, size: pg.Vector2, buttons=None, toggled=False):
        if buttons is None:
            buttons = []
        self.buttons = [btn for btn in buttons if isinstance(btn, Button)]

        self.pos = pos
        self.size = size
        self.coll_screen = pg.Surface(self.size)

        self.toggled = toggled

    def add_buttons(self, new_buttons: list):
        for new_btn in new_buttons:
            if isinstance(new_btn, Button):
                new_btn._hidden = not self.toggled
                new_btn.change_mouse_offset(self.pos)
                self.buttons.append(new_btn)

    def remove_button(self, index):
        """ -1 to remove all buttons """
        if index in self.buttons:
            self.buttons.pop(index)
        if index == -1:
            self.buttons.clear()

    def toggle(self):
        self.toggled = not self.toggled
        for btn in self.buttons:
            btn._hidden = not self.toggled

    def mouse_down(self):
        for btn in self.buttons:
            btn.perform_operation()

    def toggle_active(self, val):
        for btn in self.buttons:
            btn._active = val

    def render(self, screen: pg.Surface):
        self.coll_screen.fill(Colours.BG_COL)
        if self.toggled:
            pg.draw.rect(self.coll_screen, (255, 255, 255), pg.Rect(0, 0, self.size.x, self.size.y), 2)
            for btn in self.buttons:
                btn.render(self.coll_screen)
        screen.blit(self.coll_screen, self.pos)

    def __repr__(self):
        return f"Collection({self.pos}, {self.size}, {self.toggled}, {len(self.buttons)})"


class Button:
    def __init__(self, text, pos: pg.Vector2, operation: BTNOperation,
                 text_size=30, colour=(255, 255, 0), text_margin=5,
                 override_size: pg.Vector2 | None = None, outline=0,
                 hidden=False, active=True):
        self.font = pg.font.SysFont(GameValues.FONT, text_size)

        self.margin = text_margin
        self.operation = operation
        self._hidden = hidden
        self._active = active

        self.text = text
        self.colour: pg.Color = pg.Color(colour)
        self.outline = outline

        self.pos = pos
        self.override_size = None
        if override_size:
            self.override_size = pg.Vector2(override_size)
        self.mouse_offset = pg.Vector2(0, 0)

    def get_text_pos(self):
        return pg.Vector2(self.get_bounds().topleft) + pg.Vector2(self.margin * .5)

    def get_text(self):
        return self.text

    def get_size(self):
        if self.override_size:
            return self.override_size
        fnt = self.font.render(self.get_text(), True, self.colour)
        return pg.Vector2(fnt.get_width() + self.margin, fnt.get_height() + self.margin)

    def get_bounds(self):
        b = pg.Rect(self.pos.x + self.margin, self.pos.y + self.margin, self.get_size().x, self.get_size().y)
        if self.override_size:
            b.size = self.override_size
        return b

    def change_pos(self, new_pos: pg.Vector2):
        self.pos = new_pos

    def change_mouse_offset(self, new_off: pg.Vector2):
        self.mouse_offset = new_off

    def set_hidden(self, val: bool):
        self._hidden = val

    def set_active(self, val: bool):
        self._active = val

    def get_col(self, given_col=None):
        col = pg.Color(given_col if given_col else self.colour)
        if not self._active:
            m = 0.3
            col.update(math.ceil(col.r * m), math.ceil(col.g * m), math.ceil(col.b * m))
        return col

    def render(self, screen: pg.Surface):
        if not self._hidden:
            self.mouse_hover(screen)

            # outline
            if self.outline:
                pg.draw.rect(screen, self.get_col(), self.get_bounds(), self.outline)

            screen.blit(self.font.render(self.get_text(), True, self.get_col()), self.get_text_pos())

    def get_mouse_bounds(self):
        return pg.Rect(self.get_bounds().topleft + self.mouse_offset, self.get_bounds().size)

    def get_operation(self):
        if self.is_mouse_in_bounds():
            return self.operation

    def mouse_hover(self, screen: pg.Surface):
        if self.is_mouse_in_bounds():
            pg.draw.rect(screen, self.get_col((50, 50, 50)), self.get_bounds())

    def is_mouse_in_bounds(self):
        mp = pg.Vector2(pg.mouse.get_pos()) / GameValues.RES_MUL
        bounds = self.get_mouse_bounds()
        return (bounds.x < mp.x < bounds.x + bounds.width
                and bounds.y < mp.y < bounds.y + bounds.height)

    def should_perform_op(self):
        return self.is_mouse_in_bounds() and not self._hidden and self._active

    def perform_operation(self):
        if self.should_perform_op():
            self.operation.perform_operation()


class ButtonToggle(Button):
    def __init__(self, text, pos: pg.Vector2, operation: BTNOperation,
                 text_size=30, colour=(255, 255, 0), text_margin=5,
                 override_size: pg.Vector2 | None = None, outline=0,
                 hidden=False, active=True,
                 toggle_col=(255, 255, 255), toggled_text="", toggled_col=None):
        self.toggle_col = toggle_col
        self.toggled_col = toggled_col if toggled_col is not None else colour
        self.toggled = False
        self.toggled_text = toggled_text if toggled_text else text
        super().__init__(text, pos, operation, text_size, colour, text_margin, override_size, outline, hidden, active)

    def get_text(self):
        return self.toggled_text if self.toggled else self.text

    def perform_operation(self):
        super().perform_operation()
        if self.is_mouse_in_bounds() and not self._hidden and self._active:
            self.toggled = not self.toggled

    def get_col(self, given_col=None):
        class_col = self.toggled_col if self.toggled else self.colour
        col = pg.Color(given_col if given_col else class_col)
        if not self._active:
            m = 0.3
            col.update(math.ceil(col.r * m), math.ceil(col.g * m), math.ceil(col.b * m))
        return col

    def render(self, screen: pg.Surface):
        super().render(screen)
        if self.toggled:
            pg.draw.rect(screen, self.toggle_col, self.get_bounds(), 1)


class Input:
    def __init__(self, text, pos: pg.Vector2, operation: InputOperation,
                 text_size=20, text_col=(255, 255, 0), bg_col=(50, 50, 50), max_value_chars=3, int_only=False, margin=5,
                 default_val="", max_val=0, min_val=0, hidden=False, active=True, validator=str):
        self.font = pg.font.SysFont(GameValues.FONT, text_size)

        self.text = text
        self.colour: pg.Color = pg.Color(text_col)
        self.bg_col = bg_col
        self.margin = margin
        self.operation = operation
        self._hidden = hidden
        self._active = active
        self.int_only = int_only

        self.max = max_val
        self.min = min_val
        self.max_value_chars = max_value_chars

        self.selected = True
        self.value = default_val
        self.validator = validator

        self.box_bounds = pg.Rect(pos.x, text_size + pos.y + margin, (text_size * max_value_chars) * 0.8, text_size + margin)
        display_text = self.font.render(text, True, text_col)
        self.text_pos = pg.Vector2(get_middle(pos.x, self.box_bounds.width, display_text.get_width()), pos.y)

        self.de_select()  # load defaults

    def key_input(self, key):
        replace_chars = {'space': ' ', 'left shift': '', 'right shift': ''}
        if self.selected and not self._hidden and self._active:
            if key == pg.K_RETURN:
                self.de_select()
                return
            elif key == pg.K_BACKSPACE:
                self.value = self.value[:-1]
                return

            # add to value
            if len(self.value) < self.max_value_chars:
                char = pg.key.name(key)
                char = replace_chars[char] if char in replace_chars else char
                if self.int_only and not char.isdigit():
                    return
                self.value += char
                return
            self.de_select()

    def get_col(self, given_col=None):
        col = pg.Color(given_col if given_col else self.colour)
        if not self._active:
            m = 0.3
            col.update(math.ceil(col.r * m), math.ceil(col.g * m), math.ceil(col.b * m))
        return col

    def de_select(self):
        if self.selected:
            self.selected = False
            self.validate_input()
            self.operation.perform_operation(int(self.value) if self.int_only else self.value)

    def change_value(self, new_value):
        self.validate_input(new_value)

    def validate_input(self, new_val=None):
        new_val = new_val if new_val is not None else self.value
        if self.int_only:
            self.value = self.validator(min(self.max, max(self.min, int(new_val if new_val else 0))))  # new val if not None
            return int(self.value)
        return self.value

    def mouse_down(self):
        if self.is_mouse_in_input_bounds() and not self._hidden and self._active:
            self.selected = True
            return
        self.de_select()

    def set_hidden(self, val: bool):
        self._hidden = val

    def set_active(self, val: bool):
        self._active = val

    def render(self, screen: pg.Surface):
        if not self._hidden:
            pg.draw.rect(screen, self.get_col(self.bg_col), self.box_bounds)
            self.mouse_input_hover(screen)

            if self.selected:
                pg.draw.rect(screen, (255, 255, 255), self.box_bounds, 2)

            # text
            screen.blit(self.font.render(self.text, True, self.get_col()), self.text_pos)
            value_text = self.font.render(self.value, True, self.get_col())
            screen.blit(value_text, pg.Vector2(get_middle(self.box_bounds.x, self.box_bounds.width, value_text.get_width()), self.box_bounds.y))

    def mouse_input_hover(self, screen: pg.Surface):
        if self.is_mouse_in_input_bounds():
            pg.draw.rect(screen, self.get_col((100, 100, 100)), self.box_bounds)

    def is_mouse_in_input_bounds(self):
        mp = pg.Vector2(pg.mouse.get_pos()) / GameValues.RES_MUL
        return (self.box_bounds.x < mp.x < self.box_bounds.x + self.box_bounds.width
                and self.box_bounds.y < mp.y < self.box_bounds.y + self.box_bounds.height)


class InputRange(Input):
    def __init__(self, text, pos: pg.Vector2, operation: InputOperation, text_size=20, text_col=(255, 255, 0), bg_col=(50, 50, 50),
                 margin=5, default_val=5, max_val=10, min_val=0, hidden=False, active=True,
                 line_length=100, line_width=3, thumb_radius=6, line_margin=10, update_live=False):
        super().__init__(text, pos, operation, text_size, text_col, bg_col, len(str(max_val)), True, margin, default_val,
                         max_val, min_val, hidden, active)
        self.min = min(max_val - 1, min_val)
        self.line_length = line_length
        self.line_width = line_width
        self.line_margin = line_margin
        self.thumb_radius = thumb_radius

        self.range_selected = False
        self.update_live = update_live

    def change_range_value(self, new_val):
        old_val = int(self.value)
        new_val = self.validate_input(round(new_val))
        if self.update_live and old_val != new_val:
            self.operation.perform_operation(new_val)

    def de_select(self):
        if self.selected or self.range_selected:
            self.selected = False
            self.validate_input()
            self.operation.perform_operation(int(self.value))

    def mouse_down(self):
        super().mouse_down()
        if self.is_mouse_in_thumb_bounds(self.get_positions()[2]) and not self.range_selected:
            self.range_selected = True

    def mouse_up(self):
        if self.range_selected:
            self.de_select()
            self.range_selected = False

    def get_positions(self):
        """ Returns: line start, line end, thumb pos """
        mid = self.box_bounds.x + (self.box_bounds.width / 2)
        ll = self.line_length / 2
        y = self.box_bounds.y + self.box_bounds.height + self.line_margin + self.thumb_radius
        val = max(self.min, min(self.max, int(self.value if self.value else 0)))  # value if not None
        thumb_x = mid + (((val - ((self.max + self.min) / 2)) / (self.max - self.min)) * self.line_length)
        return pg.Vector2(mid - ll, y), pg.Vector2(mid + ll, y),  pg.Vector2(thumb_x, y)

    def render(self, screen: pg.Surface):
        super().render(screen)
        if not self._hidden:
            start, end, thumb_pos = self.get_positions()

            pg.draw.line(screen, self.colour, start, end, width=self.line_width)  # line
            pg.draw.circle(screen, self.colour, thumb_pos, radius=self.thumb_radius)  # thumb

            # update selected / hover
            if self.is_mouse_in_thumb_bounds(thumb_pos) or self.range_selected:
                width = self.thumb_radius if self.range_selected else math.ceil(self.thumb_radius / 4)
                pg.draw.circle(screen, Colours.BLACK, thumb_pos, width=width, radius=self.thumb_radius - 2)
    
    def update(self):
        """ Called every frame """
        if self.range_selected:
            mp_x = pg.mouse.get_pos()[0]
            start, end = self.get_positions()[:2]
            percent = ((mp_x - start.x) / (end.x - start.x))
            val = self.min + ((self.max - self.min) * percent)
            self.change_range_value(val)

    def is_mouse_in_thumb_bounds(self, thumb_pos):
        mp_x, mp_y = pg.mouse.get_pos()
        return (thumb_pos.x - self.thumb_radius < mp_x < thumb_pos.x + self.thumb_radius
                and thumb_pos.y - self.thumb_radius < mp_y < thumb_pos.y + self.thumb_radius)


class InputRangeH(InputRange):
    """ Horizontal alignment of InputRange """
    def __init__(self, text, pos: pg.Vector2, operation: InputOperation, text_size=20, text_col=(255, 255, 0), bg_col=(50, 50, 50),
                 margin=5, default_val=5, max_val=10, min_val=0, hidden=False, active=True,
                 line_length=100, line_width=3, thumb_radius=6, line_margin=10, update_live=False):
        super().__init__(text, pos, operation, text_size, text_col, bg_col, margin, default_val, max_val, min_val, hidden,
                         active, line_length, line_width, thumb_radius, line_margin, update_live)

        size = pg.Vector2((text_size * self.max_value_chars) * 0.8, text_size + margin)
        text_width = self.font.render(text, True, text_col).get_width()
        self.box_bounds = pg.Rect(text_width + pos.x + margin, pos.y, size.x, size.y)
        self.text_pos = pg.Vector2(pos.x, pos.y)

    def get_positions(self):
        """ Returns: line start, line end, thumb pos """
        ll = self.line_length / 2
        x = self.box_bounds.x + self.box_bounds.width + ll + self.margin + self.thumb_radius
        y = self.box_bounds.y + (self.box_bounds.height / 2)
        val = max(self.min, min(self.max, int(self.value if self.value else 0)))  # value if not None
        thumb_x = x + (((val - ((self.max + self.min) / 2)) / (self.max - self.min)) * self.line_length)
        return pg.Vector2(x - ll, y), pg.Vector2(x + ll, y),  pg.Vector2(thumb_x, y)
