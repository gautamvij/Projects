

import sys
import os
import math
import trap
from hero_exit import *

import pygame
from pygame import mixer
try:
    import _path
except:
    pass

import tiledtmxloader

#  -----------------------------------------------------------------------------

def main():
   
    demo_pygame('./maps/maze2.tmx',0)

#  -----------------------------------------------------------------------------

def demo_pygame(file_name,frm):
   
    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)
    # loading the sound files in different sound formats of mixer and main background sound in mixer stream 
    mixer.init()
    sound = mixer.Sound('./sounds/wind1.ogg')
    sound.play(-1)
	# setting up an environment for shifting the map while exiting from the map
    portal1 = pygame.Rect(30*12,0*16,5*12,9*12) 
    # init pygame and set up a screen
    pygame.init()
    pygame.display.set_caption("tiledtmxloader - " + file_name + \
                                                        " - keys: arrows, 0-9")
    screen_width = min(1024, world_map.pixel_width)
    screen_height = min(1024, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load the images using pygame
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    # prepare map rendering
    assert world_map.orientation == "orthogonal"

    # renderer
    renderer = tiledtmxloader.helperspygame.RendererPygame()

    # create hero sprite
    # use floats for hero position
    hero_pos_x = 4*16
    hero_pos_y = 16*61
    hero = create_hero(hero_pos_x, hero_pos_y)

    # dimensions of the hero for collision detection
    hero_width = hero.rect.width
    hero_height = hero.rect.width

    # cam_offset is for scrolling
    cam_world_pos_x = 512
    cam_world_pos_y = 512

    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height)

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    # filter layers
    sprite_layers = [layer for layer in sprite_layers if not layer.is_object_group]

    # add the hero the the right layer, it can be changed using 0-9 keys
    sprite_layers[2].add_sprite(hero)


    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    speed = 0.15
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # mainloop
    while running:
        dt = clock.tick(40)

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                print("fps: ", clock.get_fps())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # find directions
        direction_x = pygame.key.get_pressed()[pygame.K_RIGHT] - \
                                        pygame.key.get_pressed()[pygame.K_LEFT]
        direction_y = pygame.key.get_pressed()[pygame.K_DOWN] - \
                                        pygame.key.get_pressed()[pygame.K_UP]

        # make sure the hero moves with same speed in all directions (diagonal!)
        dir_len = math.hypot(direction_x, direction_y)
        dir_len = dir_len if dir_len else 1.0

        # update position
        step_x = speed * dt * direction_x / dir_len
        step_y = speed * dt * direction_y / dir_len
        step_x, step_y = check_collision(hero_pos_x, hero_pos_y, step_x, step_y, hero_width, hero_height, sprite_layers[3])
        hero_pos_x += step_x
        hero_pos_y += step_y
        hero.rect.center = (hero_pos_x, hero_pos_y)
		# checking for the hero position to change to next map
        if(portal1.collidepoint(hero.rect.left, hero.rect.centery)):
            sound.stop()
            portal=True
            portal_num=0
            nextlevel=next_map(file_name,0)
            running=False
 
		# adjusting the camera with respect to the hero position in vertical direction 
        cam_pos_x = 1024/2
        cam_pos_y = hero.rect.centery
        if hero.rect.centery >= 49*16:
            cam_pos_y = 49*16
        elif hero.rect.centery <=32*16:
            cam_pos_y = 32*16
        renderer.set_camera_position(cam_pos_x,cam_pos_y)
        #renderer.set_camera_position(hero.rect.centerx, hero.rect.centery)

        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0, 0, 0))

        # render the map
        for sprite_layer in sprite_layers:
            if sprite_layer.is_object_group:
                # we dont draw the object group layers
                # you should filter them out if not needed
                continue
            else:
                renderer.render_layer(screen, sprite_layer)

        pygame.display.flip()
    if (portal==True):
        
        trap.main()

#  -----------------------------------------------------------------------------

def create_hero(start_pos_x, start_pos_y):
    """
    Creates the hero sprite.
    """
    image = pygame.image.load('./images/head2.png')
    #image.fill((255, 0, 0, 200))
    rect = image.get_rect()
    rect.center = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)


#  -----------------------------------------------------------------------------

def check_collision(hero_pos_x, hero_pos_y, step_x, step_y, \
                                    hero_width, hero_height, coll_layer):
    """
    Checks collision of the hero against the world. Its not the best way to
    handle collision detection but for this demo it is good enough.

    :Returns: steps to add to heros current position.
    """
    # create hero rect
    hero_rect = pygame.Rect(0, 0, hero_width, hero_height)
    hero_rect.center = (hero_pos_x, hero_pos_y)

    # find the tile location of the hero
    tile_x = int((hero_pos_x) // coll_layer.tilewidth)
    tile_y = int((hero_pos_y) // coll_layer.tileheight)
    #print tile_x, tile_y

    # find the tiles around the hero and extract their rects for collision
    tile_rects = []
    for diry in (-1, 0 , 1):
        for dirx in (-1, 0, 1):
            if coll_layer.content2D[tile_y + diry][tile_x + dirx] is not None:
                tile_rects.append(coll_layer.content2D[tile_y + diry][tile_x + dirx].rect)

    # save the original steps and return them if not canceled
    res_step_x = step_x
    res_step_y = step_y
    #print step_x, step_y

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
   

    if value < 0:
        return math.floor(value)
    return math.ceil(value)

#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()


