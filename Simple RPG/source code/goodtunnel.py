import sys
import os
import math
import random
import cPickle as pk
import pygame
import tiledtmxloader
from pygame import mixer

#import required modules
import person,movements1
import shifty1
import goodtunnel2
from hero_exit import *

try:
    import _path
except:
    pass


def main():
    #pass the mapname and index denoting the previous map
    demo_pygame('./maps/tunnel.tmx',0)

def demo_pygame(file_name,frm):
    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)
    
    mixer.init()
    #background music and special sound effects
    sound = mixer.Sound('./sounds/oh.ogg')
    file = './sounds/SunnyDay.ogg'
    m = mixer.music.load(file)
    mixer.music.play(-1);

    #set up a screen
    screen_width = min(1000, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load the images using pygame
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    # prepare map rendering
    assert world_map.orientation == "orthogonal"

    # renderer
    renderer = tiledtmxloader.helperspygame.RendererPygame()

    #decide hero location based on the previous map
    if frm==0:
        hero_pos_x = 200
        hero_pos_y = 1860
    else:
        hero_pos_x=200
        hero_pos_y=47*20
        
    # create hero sprite
    hero = person.create_person(hero_pos_x, hero_pos_y ,'./images/hero_u2.png')

    # create treasurechest sprite
    treasure_width =3
    treasure_height=3
    
    #create pot sprite
    pot_width=3
    pot_height=4

    #create pot2 sprite
    pot2_width=4
    pot2_height=4
    
    # dimensions of the hero for collision detection
    hero_width = hero.rect.width
    hero_height = 5

    # cam_offset is for scrolling
    cam_world_pos_x = hero.rect.centerx
    cam_world_pos_y = hero.rect.centery

    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height)

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    # filter layers
    sprite_layers = [layer for layer in sprite_layers if not layer.is_object_group]

    # add the hero the the right layer, it can be changed using 0-9 keys
    sprite_layers[3].add_sprite(hero)
    
    #load the saved game variables
    sv=pk.load(open("./save.p","rb"))
    ft=sv['flagtreasure']
    # add pots positions
    pots_pos_x=[240,760,600,960]
    pots_pos_y=[60,320,880,1800]
    #create gold pots based on whether the pots have already been opened or not
    pots=[]
    for i in range(4) :
        if ft[i]==0 :
            pots.append(create_pot(pots_pos_x[i], pots_pos_y[i]))
            sprite_layers[2].add_sprite(pots[len(pots)-1]);
    
    # add pots2 positions
    pots2_pos_x=[700,80]
    pots2_pos_y=[440,160]
    pots2=[]
    #create gold pots2 based on whether the pots have already been opened or not
    for i in range(2) :
        if ft[i+4]==0 :
            pots2.append(create_pot2(pots2_pos_x[i], pots2_pos_y[i]))
            sprite_layers[2].add_sprite(pots2[len(pots2)-1]);
    
    # add treasure positions
    treasure_pos_x=[960,820,320,780]
    treasure_pos_y=[180,840,1200,1440]
    treasure=[]
    #create treasure chest based on whether the pots have already been opened or not 
    for i in range(4) :
        if ft[i+6]==0 :
            treasure.append(create_treasure(treasure_pos_x[i], treasure_pos_y[i]))
            sprite_layers[2].add_sprite(treasure[len(treasure)-1]);
            
    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    speed=6
    health=100
    mr=ml=md=mu=0
    flag1=[0 for x in range(4)]
    flag2=[0 for x in range(4)]
    flag3=[0 for x in range(4)]
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT,1000)

    #create portals to detect collision with these to change maps
    portal1 = pygame.Rect(0,98*20,49*20,20)
    portal2 = pygame.Rect(0,0,49*20,20)
    portal=False
    # mainloop
    while running:
        dt = clock.tick(40)
        sv=pk.load(open("./save.p","rb"))
        ft=sv['flagtreasure']           
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
        mov = movements1.hero_move(mr,ml,md,mu,hero_pos_x,hero_pos_y,hero,speed,sprite_layers[4])
        mr = mov[0]
        ml = mov[1]
        md = mov[2]
        mu = mov[3]
        hero_pos_x = mov[4]
        hero_pos_y = mov[5]

        # adjust camera according to the hero's position, follow him
        if ( hero.rect.centery >=1600):
            renderer.set_camera_position(500, 1600)
        elif (hero.rect.centery <=385):
            renderer.set_camera_position(500, 385)
        else:
            renderer.set_camera_position(500,hero.rect.centery )

        #go to previous map or next map based on the portal it collides with
        if(pygame.Rect.colliderect(portal1,hero.rect)):
            portal=True
            portal_num=0
            nextlevel=next_map(file_name,0)
            running=False
            mixer.music.stop()
        elif(pygame.Rect.colliderect(portal2,hero.rect)):
            portal=True
            portal_num=1
            nextlevel=next_map(file_name,1)
            running=False
            mixer.music.stop()

        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0, 0, 0))

        #render the map
        for sprite_layer in sprite_layers:
            if sprite_layer.is_object_group:
                # we dont draw the object group layers
                # you should filter them out if not needed
                continue
            else:
                renderer.render_layer(screen, sprite_layer)
                
        #detects which treasure chest the hero collides with
        n=hero.rect.collidelist(treasure)
        if  n!= -1:
            r1=treasure[n].rect;
            #change the image to open treasure chest
            im=pygame.image.load('./images/treasure2.png');
            treasure[n].image=im
            treasure[n].rect=im.get_rect();
            treasure[n].rect.center=r1.center
            #if gold not already taken update hero's gold 
            if(flag1[n]==0):
                flag1[n]=1
                ft[n+6]=1
                sv['gold'] += 13
                mixer.music.stop()
                sound.play(0)
                mixer.music.play(-1);

        #detects which pot the hero collides with
        n=hero.rect.collidelist(pots)
        if  n!= -1:
            sprite_layers[2].remove_sprite(pots[n]);
            #if gold not already taken update hero's gold 
            if(flag2[n]==0):
                ft[n]=1
                flag2[n]=1
                sv['gold'] += 7
                mixer.music.stop()
                sound.play(0)
                mixer.music.play(-1);

        #detects which pot the hero collides with
        n=hero.rect.collidelist(pots2)
        if  n!= -1:
            sprite_layers[2].remove_sprite(pots2[n]);
            #if gold not already taken update hero's gold
            if(flag3[n]==0):
                ft[n+4]=1
                flag3[n]=1
                sv['gold'] += 7
                mixer.music.stop()
                sound.play(0)
                mixer.music.play(-1);
            
        sv['flagtreasure']=ft 
        pygame.display.flip()
        #save the new game variables back to dictionary
        pk.dump(sv,open("./save.p","wb"))

    if (portal==True and portal_num==0):
        
        mp=nextlevel[0]
        frm=nextlevel[1]
        #go to previous map
        shifty1.demo_pygame(mp,frm)

    elif (portal==True and portal_num==1):

        mp=nextlevel[0]
        frm=nextlevel[1]
        #go to next map
        goodtunnel2.demo_pygame(mp,frm)

#  -----------------------------------------------------------------------------

def create_treasure(start_pos_x, start_pos_y):
    image=pygame.image.load('./images/treasure1.png')
    rect = image.get_rect()
    rect.midbottom = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)

def create_pot(start_pos_x, start_pos_y):
    image=pygame.image.load('./images/pot.png')
    rect = image.get_rect()
    rect.midbottom = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)

def create_pot2(start_pos_x, start_pos_y):
    image=pygame.image.load('./images/egypt.png')
    rect = image.get_rect()
    rect.midbottom = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)

#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()


