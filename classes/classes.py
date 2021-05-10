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
    def __init__(self, font_path: str, size: int, pos: list, init_value: str, color: list=(0, 0, 0), antialias: bool=False):
        self.size = size
        self.value = init_value
        self.antia = antialias
        self.color = color
        self.pos = pos
        self.font = pygame.font.Font(font_path, size)
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
