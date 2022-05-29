import pygame as pg
import win32api
import time


def dot_in_rectangle(rect: pg.Rect, dot: tuple) -> bool:
    x_rect, y_rect, w, h = rect
    x_mouse, y_mouse = dot
    if x_rect < x_mouse < x_rect + w and y_rect < y_mouse < y_rect + h:
        return True
    return False


class Button:
    def __init__(self, position, text, action, color=(0, 0, 0), width=0, height=0, font_size=25, border=2, active=True, **kwargs):
        self.position = position
        self._border = border
        self.text = text
        self.color = color
        self._font_color = color
        self.font_size = font_size
        self._font = pg.font.Font(None, font_size)
        self._txt_surface = self._font.render(text, True, self._font_color)
        self.width = width
        self.height = height
        if width < self._txt_surface.get_width() + 10:
            self.width = self._txt_surface.get_width() + 10
        if height < self._txt_surface.get_height() + 10:
            self.height = self._txt_surface.get_height() + 10
        self.action = action
        self.kwargs = kwargs
        self.active = active

    def draw(self, surface: pg.surface):
        rect = pg.Rect(*self.position, self.width, self.height)
        x, y = pg.mouse.get_pos()
        if dot_in_rectangle(rect, (x, y)):
            self._font_color = (255, 255, 255)
            self._txt_surface = self._font.render(self.text, True, self._font_color)
            if self.active:
                pg.draw.rect(surface, rect=rect, color=self.color, width=0)
            else:
                pg.draw.rect(surface, rect=rect, color=(122, 122, 122), width=0)
            left = win32api.GetKeyState(0x001)
            if left in [-127, -128] and self.active:
                self.action(**self.kwargs)
                time.sleep(0.1)
        else:
            self._font_color = self.color
            if self.active:
                self._txt_surface = self._font.render(self.text, True, self._font_color)
                pg.draw.rect(surface, rect=rect, color=self.color, width=2)
            else:
                pg.draw.rect(surface, rect=rect, color=(122, 122, 122), width=2)
                self._txt_surface = self._font.render(self.text, True, (122, 122, 122))
        surface.blit(self._txt_surface, (rect.x + (self.width - self._txt_surface.get_width()) / 2,
                                         rect.y + (self.height - self._txt_surface.get_height()) / 2))
