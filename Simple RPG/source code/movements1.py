import sys
import os
import math
import random
import time
import pygame
import tiledtmxloader

try:
    import _path
except:
    pass

# find directions
# update hero image according to movement
def hero_move(mr,ml,md,mu,hero_pos_x,hero_pos_y,hero,speed,sprite_layers_no):
        dx = pygame.key.get_pressed()[pygame.K_RIGHT] - pygame.key.get_pressed()[pygame.K_LEFT]
        dy = pygame.key.get_pressed()[pygame.K_DOWN] - pygame.key.get_pressed()[pygame.K_UP]
        if(dx==1 or dx==-1):
            dy=0
        if(dx==1):
            ml = mu = md = 1
            mr +=1
            if(mr==15):
                mr=1
            if mr in range(1,8):
                hero.image=pygame.image.load('./images/hero_r1.png')
            elif mr in range(8,15):
                hero.image=pygame.image.load('./images/hero_r3.png')
        elif(dx==-1):
            mr = mu = md = 1
            ml += 1
            if(ml==15):
                ml=1
            if (ml in range(1,8)):
                hero.image=pygame.image.load('./images/hero_l1.png')
            elif ml in range(8,15):
                hero.image=pygame.image.load('./images/hero_l3.png')
        elif(dy==-1):
            ml = mr = md = 1
            mu +=1
            if(mu==15):
                mu=1
            if mu in range(1,8):
                hero.image=pygame.image.load('./images/hero_d1.png')
            elif mu in range(8,15):
                hero.image=pygame.image.load('./images/hero_d3.png')
        elif(dy==1):
            ml = mu = mr = 1
            md += 1
            if(md==15):
                md=1
            if (md in range(1,8)):
                hero.image=pygame.image.load('./images/hero_u1.png')
            elif md in range(8,15):
                hero.image=pygame.image.load('./images/hero_u3.png')

# update position
        step_x = speed  * dx
        step_y = speed  * dy
        step_x, step_y = check_collision(hero_pos_x, hero_pos_y, step_x, step_y, hero.rect.width, 5, sprite_layers_no)
        hero_pos_x += step_x
        hero_pos_y += step_y
        hero.rect.midbottom = (hero_pos_x, hero_pos_y)
        return [mr, ml, md, mu, hero_pos_x, hero_pos_y, hero]
        
#  -----------------------------------------------------------------------------

def check_collision(hero_pos_x, hero_pos_y, step_x, step_y, 
                                    hero_width, hero_height, coll_layer):
    """
    Checks collision of the hero against the world. Its not the best way to
    handle collision detection but for this demo it is good enough.

    :Returns: steps to add to heros current position.
    """
    # create hero rect
    hero_rect = pygame.Rect(0, 0, hero_width, hero_height)
    hero_rect.midbottom = (hero_pos_x, hero_pos_y)

    # find the tile location of the hero
    tile_x = int((hero_pos_x) // coll_layer.tilewidth)
    tile_y = int((hero_pos_y) // coll_layer.tileheight)

    # find the tiles around the hero and extract their rects for collision
    tile_rects = []
    for diry in (-1, 0 , 1):
        for dirx in (-1, 0, 1):
            if coll_layer.content2D[tile_y + diry][tile_x + dirx] is not None:
                tile_rects.append(coll_layer.content2D[tile_y + diry][tile_x + dirx].rect)

    # save the original steps and return them if not canceled
    res_step_x = step_x
    res_step_y = step_y

    # x direction, floor or ceil depending on the sign of the step
    step_x = special_round(step_x)

    # detect a collision and dont move in x direction if colliding
    if hero_rect.move(step_x, 0).collidelist(tile_rects) > -1:
        res_step_x = 0

    # y direction, floor or ceil depending on the sign of the step
    step_y = special_round(step_y)

    # detect a collision and dont move in y direction if colliding
    if hero_rect.move(0, step_y).collidelist(tile_rects) > -1:
        res_step_y = 0

    # return the step the hero should do
    return res_step_x, res_step_y

#  -----------------------------------------------------------------------------

def special_round(value):
    """
    For negative numbers it returns the value floored,
    for positive numbers it returns the value ceiled.
    """
    # same as:  math.copysign(math.ceil(abs(x)), x)
    # OR:
    # ## versus this, which could save many function calls
    # import math
    # ceil_or_floor = { True : math.ceil, False : math.floor, }
    # # usage
    # x = floor_or_ceil[val<0.0](val)

    if value < 0:
        return math.floor(value)
    return math.ceil(value)
