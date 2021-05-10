import pygame
import random
import json

from classes.classes import *

COLORS = ((252, 163, 17), (20, 33, 61), (229, 229, 229))
RES = (700, 600)
PASS_HEIGHT = 180
WALL_SPEED = 5
WALL_WIDTH = 60
WALL_HEIGHT = 60
FPS = 60


# non-main functions --- #
def generate_new_blocks(color:list, x_offset: int = 0, block_count: int=3) -> list:
    blocks = []
    total_height = 0
    gap = random.randint(-WALL_HEIGHT, PASS_HEIGHT)

    for _ in range(block_count):
        rect = pygame.Rect(RES[0]+x_offset, gap + total_height, WALL_WIDTH, WALL_HEIGHT)
        total_height += gap + WALL_HEIGHT
        gap = random.randint(PASS_HEIGHT-50, PASS_HEIGHT+50)

        blocks.append(Wall(rect, color))

    return blocks


# objects & vars --- #
pygame.init()
display = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
pygame.display.set_caption("Triplebox!")
icon = pygame.image.load('imgs/icon.png').convert_alpha()
pygame.display.set_icon(icon)
del icon

with open('data/data.json', 'r') as f:
    data = json.load(f)

color_abs_id = 0
main_run = True
game_over = False

walls = []
walls.extend(
    generate_new_blocks(COLORS[(color_abs_id+1) % 3]) 
    + generate_new_blocks(COLORS[(color_abs_id+1) % 3], 
    (RES[0] + WALL_WIDTH)//2)
)

score = 0
text_fade_in_factor = 150
score_txt = Text('fonts/Signika.ttf', 400, [0, 0], str(score), [x-15 for x in COLORS[(color_abs_id+2) % 3]], True)
score_txt.set_pos_to_center(RES, [0, -10])

hiscore_txt = Text('fonts/Signika.ttf', 48, [0, 0], "Highscore: "+str(data['hiscore']), [x-15 for x in COLORS[(color_abs_id+2) % 3]], True)
hiscore_txt.set_pos_to_center(RES, [0, 160])

player = Player(
    pygame.Rect(-50, RES[1]//2-25, 50, 50), 
    [pygame.image.load(f'imgs/player_{x}.png').convert_alpha() for x in range(3)],
    color_abs_id % 3
)



# main functions --- #
def events():
    global main_run
    """ All pygame.event stuff here. """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.jump()


def update():
    global walls, game_over, player, color_abs_id, score, score_txt, text_fade_in_factor, hiscore_txt
    """ All updating related stuff here. """
    if game_over:
        player.rect.width *= 1.04
        player.rect.height *= 1.04
        player.rect.x -= 0.02*player.rect.width
        player.rect.y -= 0.02*player.rect.height
        player.sprites[player.sprite_id] = pygame.transform.scale(
            player.sprites[player.sprite_id], 
            player.rect[2:4]
        )

        if player.rect.width > 2.5*RES[0] and player.rect.height > 2.5*RES[1]:
            game_over = False
            color_abs_id += 1
            player = Player(
                pygame.Rect(-50, RES[1]//2-25, 50, 50), 
                [pygame.image.load(f'imgs/player_{x}.png').convert_alpha() for x in range(3)],
                color_abs_id % 3
            )
            walls = []
            walls.extend(
                generate_new_blocks(COLORS[(color_abs_id+1) % 3]) 
                + generate_new_blocks(COLORS[(color_abs_id+1) % 3], 
                (RES[0] + WALL_WIDTH)//2)
            )
            score = 0
            text_fade_in_factor = 150
            score_txt.set_value(str(score), update=False)
            score_txt.set_color(COLORS[(color_abs_id+2) % 3])
            score_txt.set_pos_to_center(RES, [0, -10])
            hiscore_txt.set_color(COLORS[(color_abs_id+2) % 3])
            hiscore_txt.set_pos_to_center(RES, [0, 160])
            with open('data/data.json', 'w') as f:
                json.dump(data, f)
        return

    player.rect.x += player.x_anim_entry
    player.x_anim_entry *= 0.96
    player.apply_gravity()
    if abs(player.gravity) < 70:
        player.update_gravity()

    for i, w in enumerate(walls):
        w.rect.x -= WALL_SPEED
        if player.rect.colliderect(w.rect) or player.rect.y < 0 or player.rect.y + player.rect.height > RES[1]:
            game_over = True
            break
        if w.rect.x < -WALL_WIDTH:
            walls = walls[3:]
            break

    if len(walls) < 6:
        walls.extend(generate_new_blocks(COLORS[(color_abs_id+1) % 3]))
        score += 1
        score_txt.set_value(str(score))
        score_txt.set_pos_to_center(RES, [0, -10])
        if score > data['hiscore']:
            data['hiscore'] = score
            hiscore_txt.set_value("Highscore: "+str(data['hiscore']))
            hiscore_txt.set_pos_to_center(RES, [0, 160])


    if text_fade_in_factor != 1:
        c = [round(x-15+(text_fade_in_factor/10)) for x in COLORS[(color_abs_id+2) % 3]]
        score_txt.set_color(c)
        hiscore_txt.set_color(c)
        text_fade_in_factor -= 1

def render(display: object):
    """ All rendering related stuff here. """
    ticks = pygame.time.get_ticks()
    display.fill(COLORS[(color_abs_id+2) % 3])

    score_txt.render(display)
    hiscore_txt.render(display)
    for w in walls:
        w.render(display)
    player.render(display)

    pygame.display.update()


# mainloop --- #
while main_run:
    clock.tick(FPS)

    events()
    update()
    render(display)

pygame.quit()
