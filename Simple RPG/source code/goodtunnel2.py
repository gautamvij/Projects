import sys
import os
import math
import random
import tiledtmxloader
import pygame
from pygame import mixer

#import required modules
import person,movements1
import goodtunnel
try:
    import _path
except:
    pass



def main():
    #pass the mapname and index to denote the previous map
    demo_pygame('./maps/tunnel2.tmx',0)

def demo_pygame(file_name,frm):
    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    mixer.init()
    # background music play infinitely unless stopped explicitly
    file = './sounds/Sunny2.ogg'
    m = mixer.music.load(file)
    mixer.music.play(-1);
    
    #set up a screen
    screen_width = min(930, world_map.pixel_width)
    screen_height = min(760, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load the images using pygame
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    # prepare map rendering
    assert world_map.orientation == "orthogonal"

    # renderer
    renderer = tiledtmxloader.helperspygame.RendererPygame()

    # create hero sprite
    hero_pos_x = 500
    hero_pos_y = 1450
    #create hero at specified location with specified image
    hero = person.create_person(hero_pos_x, hero_pos_y ,'./images/hero_u2.png')
    
    # dimensions of the hero for collision detection
    hero_width = hero.rect.width
    hero_height = 5

    # cam_offset is for scrolling
    cam_world_pos_x = screen_width/2
    cam_world_pos_y = screen_height/2

    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height)

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    # filter layers
    sprite_layers = [layer for layer in sprite_layers if not layer.is_object_group]

    # add the hero sprite
    sprite_layers[2].add_sprite(hero)
           
    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    speed=3
    portal=False
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT,1000)
    mr=ml=md=mu=0
    #create portal to detect collision with player and update map
    portal1 = pygame.Rect(1*20,74*20,49*20,20)
    # mainloop
    while running:
        dt = clock.tick(50)
                    
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
       
        mov = movements1.hero_move(mr,ml,md,mu,hero_pos_x,hero_pos_y,hero,speed,sprite_layers[3])
        mr = mov[0]
        ml = mov[1]
        md = mov[2]
        mu = mov[3]
        hero_pos_x = mov[4]
        hero_pos_y = mov[5]
        
        #update camera position according to hero's position
        if ( hero.rect.centery >=1150):
            renderer.set_camera_position(490, 1150)
        elif (hero.rect.centery <=380):
            renderer.set_camera_position(490, 380)
        else:
            renderer.set_camera_position(490,hero.rect.centery )

        #detect collision with portal
        if(portal1.collidepoint(hero.rect.midbottom)):
            portal=True
                    
        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0, 0, 0))

        #render the map
        for sprite_layer in sprite_layers:
            if sprite_layer.is_object_group:
                continue
            else:
                renderer.render_layer(screen, sprite_layer)
                            
        pygame.display.flip()
        if portal==True:
            #stop the background music and change the map
            mixer.music.stop()
            goodtunnel.demo_pygame('./maps/tunnel.tmx',1)

#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()


