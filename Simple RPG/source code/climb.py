import sys
import os
import math
import random
import pygame

def hero_climb(cl,hero_pos_x,hero_pos_y,hero,speed_x,speed_y,sprite_layers_no):
        #to determine directions of movement
        dx = pygame.key.get_pressed()[pygame.K_RIGHT] - pygame.key.get_pressed()[pygame.K_LEFT]
        dy = pygame.key.get_pressed()[pygame.K_DOWN] - pygame.key.get_pressed()[pygame.K_UP]
        if(dx==1 or dx==-1):
                dy=0
        if 0<= cl <14: cl += 1
        elif cl==14: cl = 0
        #change image to show the arms and legs movement for player
        if cl == 0:
                hero.image = pygame.image.load('./images/up.png')
        elif cl == 7:
                hero.image = pygame.image.load('./images/down.png')

        # update position
        step_x = speed_x  * dx
        step_y = speed_y * dy
        step_x, step_y = check_collision(hero_pos_x, hero_pos_y, step_x, step_y, hero.rect.width, 5, sprite_layers_no)
        hero_pos_x += step_x
        hero_pos_y += step_y
        hero.rect.midbottom = (hero_pos_x, hero_pos_y)
        return [cl,hero_pos_x,hero_pos_y]

def check_collision(hero_pos_x, hero_pos_y, step_x, step_y, \
                                    hero_width, hero_height, coll_layer):
    """
    Checks collision of the hero against the world. 
    :Returns: steps to add to heros current position.
    """
    # create hero rect
    hero_rect = pygame.Rect(0, 0, hero_width, hero_height)
    hero_rect.midbottom = (hero_pos_x, hero_pos_y)

    # find the tile location of the hero
    tile_x = int((hero_pos_x) // coll_layer.tilewidth)
    tile_y = int((hero_pos_y) // coll_layer.tileheight)

    if (tile_y >= 1 and tile_y <199) :
        tile_rects = []
        for diry in (-1, 0 , 1):
            for dirx in (-1, 0, 1):
                if coll_layer.content2D[tile_y + diry][tile_x + dirx] is not None:
                    tile_rects.append(coll_layer.content2D[tile_y + diry][tile_x + dirx].rect)
    # find the tiles around the hero and extract their rects for collision
    else:
       return 0, 0 

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
