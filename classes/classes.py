import pygame
import math


class Player:
    def __init__(self, rect: object, sprites:list, sprite_id:int, jump_force: int=12, gravity_force: float=0.6):
        self.rect = rect
        self.sprites = [pygame.transform.smoothscale(x, rect[2:4]) for x in sprites]
        self.sprite_id = sprite_id
        self.jump_force = jump_force
        self.gravity_force = gravity_force
        self.gravity = -10
        self.x_anim_entry = 10

    def jump(self):
        self.gravity = -self.jump_force

    def update_gravity(self):
        self.gravity += self.gravity_force

    def apply_gravity(self):
        self.rect.y += self.gravity

    def render(self, display: object):
        rotated_img = pygame.transform.rotate(
            self.sprites[self.sprite_id], 
            -45*math.sin(self.gravity/45)
        )
        display.blit(rotated_img, self.rect[0:2])


class Wall:
    def __init__(self, rect: object, color: list=[20, 33, 61]):
        self.rect = rect
        self.color = color

    def render(self, display: object):
        pygame.draw.rect(display, self.color, self.rect)


class Text:
    def __init__(self, font_path: str, font_size: int, pos: list, init_value: str, color: list=(0, 0, 0), antialias: bool=False):
        self.size = font_size
        self.value = init_value
        self.antia = antialias
        self.color = color
        self.pos = pos
        self.font = pygame.font.Font(font_path, font_size)
        self.text = self.font.render(init_value, antialias, color)

    def render(self, display: object):
        display.blit(self.text, self.pos)

    def update_text(self):
        self.text = self.font.render(self.value, self.antia, self.color)

    def set_pos_to_center(self, rel_dimensions: list, offset: list=[0, 0]):
        self.pos = [
            (rel_dimensions[0] - self.text.get_width())/2 + offset[0], 
            (rel_dimensions[1] - self.text.get_height())/2 + offset[1]
        ]

    def set_value(self, new_value: str, update: bool=True):
        self.value = new_value
        if update:
            self.update_text()

    def set_color(self, new_color: list, update: bool=True):
        self.color = new_color
        if update:
            self.update_text()

    def set_pos(self, new_pos: list):
        self.pos = new_pos

class Button:
    def __init__(self, rect: object, text: object, bg_color: list, bg_color_pressed: list):
        self.rect = rect
        self.text = text
        self.bg_color = bg_color
        self.bg_color_pressed = bg_color_pressed
        self.original_text_color = text.color
        self.pressed = False
        self.text_shade = 0
        self.text.pos = [
            (self.rect[2] - text.text.get_width())/2 + self.rect[0],
            (self.rect[3] - text.text.get_height())/2 + self.rect[1]
        ]

    def render(self, display: object):
        bg_clr = self.bg_color
        if self.pressed:
            bg_clr = self.bg_color_pressed
        pygame.draw.rect(display, bg_clr, self.rect)
        self.text.render(display)

    def modify_text_shade(self, add_value: int):
        self.text_shade += add_value
        self.text.set_color([abs(x+self.text_shade) for x in self.original_text_color])

    def is_over(self, point: list):
        return self.rect.collidepoint(point)

    def set_colors(self, normal_color: list=None, pressed_color: list=None, text_color: list=None):
        self.bg_color = normal_color if not None else self.bg_color
        self.bg_color_pressed = pressed_color if not None else self.bg_color_pressed
        if text_color:
            self.text.set_color(text_color)
            self.original_text_color = text_color
