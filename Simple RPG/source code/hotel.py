import sys
import os
import math
import random
import tiledtmxloader
from pygame import mixer
import pygame
import cPickle as pk

import person,movements1
import shifty1
import menu

try:
    import _path
except:
    pass

def main():
    #pass the map name and index to detect the previous/next map
    demo_pygame('./maps/hotel.tmx',0)

def demo_pygame(file_name,frm):
    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    mixer.init()
    # background music 
    file = './sounds/hotel.ogg'
    m = mixer.music.load(file)
    mixer.music.play(-1);
    
    #set up a screen
    screen_width = min(900, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load the images using pygame
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    # prepare map rendering
    assert world_map.orientation == "orthogonal"

    # renderer
    renderer = tiledtmxloader.helperspygame.RendererPygame()

    # create hero sprite
    hero_pos_x = 200
    hero_pos_y = 1600
    hero = person.create_person(hero_pos_x, hero_pos_y ,'./images/hero_u2.png')
    
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
    sprite_layers[2].add_sprite(hero)
    
    # add pots positions
    ty=pk.load(open("./save.p","rb"))
    t=ty['hotel_treasure']
    pots_pos_x=[100,520,800,180]
    pots_pos_y=[960,960,820,120]
    pots=[]
    flag=[0,0,0,0,0]
    for i in range(4):
        if t[i]==0 :
            pots.append(create_pot(pots_pos_x[i], pots_pos_y[i]));
    
    c_pos=[cam_world_pos_x, cam_world_pos_y]
    ty=pk.load(open("./save.p","rb"))
    hp=ty['hp']
    hp_max=ty['max_hp']      
    interf_toggle=0
    interface=menu.create_interface(renderer,sprite_layers,screen,c_pos) 
    hp_sprite=person.create_person(c_pos[0],c_pos[1],'./images/hp_bar.png')
    l_g=menu.create_l_g(renderer,sprite_layers,screen,c_pos)
    [hp_sprite,hp]=menu.create_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos)
    xp_sprite=person.create_person(c_pos[0],c_pos[1],'./images/exp_bar.png')
    xp_sprite=menu.create_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos)

        
    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    speed=6
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT,1000)
    mr=ml=md=mu=0

    #create portals to detect when to change map
    portal1 = pygame.Rect(19*20,73*20,5*20,2*20)
    portal2 = pygame.Rect(2*20,81*20,40*20,40)

    # mainloop
    while running:
        dt = clock.tick(40)
        ty=pk.load(open("./save.p","rb"))
                    
        # event handling

        for event in pygame.event.get():
            menu.update_lg(l_g,c_pos)
            menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
            menu.update_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos,0)

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

        # adjust camera according to the hero's position, follow him
        if ( hero.rect.centery >=1280):
            renderer.set_camera_position(450, 1280)
            c_pos=(450+60,1360)
        elif (hero.rect.centery <=400):
            renderer.set_camera_position(450, 400)
            c_pos=(450+60,400)
        else:
            renderer.set_camera_position(450,hero.rect.centery )
            c_pos=(450+60,hero.rect.centery)


        #place health,experience and armours
        interface.rect.topleft=(c_pos[0]-512,c_pos[1]-384)
        hp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-382)
        xp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-345)
        l_g.rect.topleft=(c_pos[0]-508,c_pos[1]-381)

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
                
        ##If talk to receptionist
        #List Variable to check if the person has bought the room or not
        pos_hero=None
        if(flag[4] == 0 and pygame.Rect.colliderect(portal1,hero.rect) and pygame.key.get_pressed()[pygame.K_SPACE]==1):
            pos_hero=menu.warning_msg(file_name,renderer,sprite_layers,screen,c_pos,0)

        if pos_hero!=None:
            hero_pos_x=pos_hero[0]
            hero_pos_y= pos_hero[1]
            ty=pk.load(open("./save.p","rb"))

        if(portal2.collidepoint(hero.rect.midbottom)): 
            pk.dump(ty,open("./save.p","wb"))
            mixer.music.stop()
            running=False
        t=ty['hotel_treasure']
        n=hero.rect.collidelist(pots)
        if  n== 0 and flag[n]==0 and t[n]==0 :
            ty['hp']+=5
            flag[n]=1
            t[n]=1 
        elif n==1 and flag[n]==0 and t[n]==0 :
            ty['gold']+=5
            flag[n]=1
            t[n]=1 
        elif n==2 and flag[n]==0 and t[n]==0 :
            ty['gold']+=10
            flag[n]=1
            t[n]=1 
        elif n==3 and flag[n]==0 and t[n]==0 :
            ty['hp']+=10
            flag[n]=1
            t[n]=1 
                     
            
        ty['hotel_treasure']=t
        pk.dump(ty,open("./save.p","wb"))
        pygame.display.flip()

    shifty1.demo_pygame('./maps/village2_inside.tmx',1)



#  -----------------------------------------------------------------------------
def create_pot(start_pos_x, start_pos_y):
    image=pygame.image.load('./images/collision.png')
    rect = image.get_rect()
    rect.midbottom = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)

#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()


