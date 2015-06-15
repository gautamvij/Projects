import sys
import os
import math
import random
import time
import movements1
import person
import pygame
import tiledtmxloader
import enemy_attack
import sound
from PIL import Image, ImageDraw, ImageFont
import shifty1
import menu
import cPickle as pk

try:
    import _path
except:
    pass



#  -----------------------------------------------------------------------------

def main(frm):
    demo_pygame('./maps/tunnel2_4.tmx',frm)

#  -----------------------------------------------------------------------------

def demo_pygame(file_name,frm):

    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    # init pygame and set up a screen
    pygame.display.set_caption("tiledtmxloader - " + file_name + \
                                                        " - keys: arrows, 0-9")
    screen_width = min(1024, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load the images using pygame
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    # prepare map rendering
    assert world_map.orientation == "orthogonal"

    # renderer
    renderer = tiledtmxloader.helperspygame.RendererPygame()

    #background music
    tunnel2_4_sound = sound.create_music(file_name)
    sound.volume(tunnel2_4_sound,0.2)
    
    # create hero sprite
    if frm==0:
        hero_pos_x = 5*32
        hero_pos_y = 95*32
    else:
        hero_pos_x = 81*32
        hero_pos_y = 62*32
    hero = person.create_person(hero_pos_x, hero_pos_y ,'./images/hero_u2.png')

    # create monster sprites
    mon = []
    mon_dir = []
    mon_image = []
    mon.append(person.create_person(16*32, 82*32,'./images/slime14.png'))
    mon.append(person.create_person(39*32, 82*32,'./images/slime14.png'))
    mon.append(person.create_person(50*32, 82*32,'./images/slime14.png'))
    mon.append(person.create_person(60*32, 82*32,'./images/slime14.png'))
    mon.append(person.create_person(67*32, 82*32,'./images/slime14.png'))
    mon.append(person.create_person(5*32, 74*32,'./images/slime14.png'))
    mon.append(person.create_person(5*32, 47*32,'./images/slime14.png'))
    mon.append(person.create_person(14*32, 47*32,'./images/slime14.png'))
    mon.append(person.create_person(23*32, 33*32,'./images/slime14.png'))
    mon.append(person.create_person(23*32, 20*32,'./images/slime14.png'))
    mon.append(person.create_person(20*32, 8*32,'./images/slime14.png'))
    mon.append(person.create_person(43*32, 8*32,'./images/slime14.png'))
    mon.append(person.create_person(43*32, 24*32,'./images/slime14.png'))
    mon.append(person.create_person(43*32, 41*32,'./images/slime14.png'))
    mon.append(person.create_person(49*32, 47*32,'./images/slime14.png'))
    mon.append(person.create_person(66*32, 47*32,'./images/slime14.png'))
    mon.append(person.create_person(72*32, 32*32,'./images/slime14.png'))
    mon.append(person.create_person(72*32, 23*32,'./images/slime14.png'))
    mon.append(person.create_person(72*32, 8*32,'./images/slime14.png'))
    mon.append(person.create_person(81*32, 8*32,'./images/slime14.png'))
    mon.append(person.create_person(81*32, 19*32,'./images/slime14.png')) 
    mon.append(person.create_person(81*32, 36*32,'./images/slime14.png'))
    mon.append(person.create_person(81*32, 49*32,'./images/slime14.png'))
    mon.append(person.create_person(67*32, 64*32,'./images/slime14.png'))
    mon.append(person.create_person(82*32, 64*32,'./images/slime14.png'))

    #list to save the direcion constraints for enemy's movements
    mon_dir = [-1,0,-1,0,1,0,1,0,1,0,0,-1,1,0,-1,0,0,-1,0,1,1,0,-1,0,0,1,0,-1,1,0,-1,0,0,-1,0,1,1,0,-1,0,0,1,0,-1,0,1,1,0,-1,0]
    
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

    # add the hero and monsters to the the right layer
    sprite_layers[1].add_sprite(hero)
    i = 0
    for i in range(len(mon)):
        mon_image.append(1)
        sprite_layers[1].add_sprite(mon[i])

    # portal for entry and exit of hero
    portal1=pygame.Rect(4*32,96*32,3*32,2*32)
    portal2=pygame.Rect(85*32,61*32,1*32,3*32)
        
        
    # variables for the main loop
    clock = pygame.time.Clock()
    running = True # to run while loop
    speed = 10 # hero speed
    mr=ml=md=mu=0 # image variables(change images to show movements of hero)
    h_drctn = 'up'  # direction where hero facing right now
    life = 1 # to keep track wheather hero is alive or not
    arrow_list = [] # contains a list of arrows (currently on screen)
    arrow_dir = [] # directions of arrows

    HP_MON = [10.0]*(len(mon)) # health of monster
    point_arrow = 10.0 # decrease in health of enemy when arrow of hero collides with enemy
    point_enm = 1.0 # decrease in health of hero after collision with enemy
    enm_speed = 8.0 # speed of enemy

    savegame=pk.load(open("./save.p","rb"))
    old_xp = savegame['xp']
    old_level = savegame['h_level']
    old_armor = savegame['sheild_hp']
    old_arrow = savegame['arrow_count']

     # interface code
    c_pos=[cam_world_pos_x, cam_world_pos_y]
    interface=menu.create_interface(renderer,sprite_layers,screen,c_pos) 
    hp_sprite=person.create_person(c_pos[0],c_pos[1],'./images/hp_bar.png') # hp bar interface
    l_g=menu.create_l_g(renderer,sprite_layers,screen,c_pos) # level and gold interface
    [hp_sprite,hp]=menu.create_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos) 
    xp_sprite=person.create_person(c_pos[0],c_pos[1],'./images/exp_bar.png') # x interface
    xp_sprite=menu.create_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos)
    f_i=menu.create_f_i(renderer,sprite_layers,screen,c_pos) # arrow,armor,sword interface
    interf_fight=menu.create_interface_fight(renderer,sprite_layers,screen,c_pos)

    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # mainloop
    while running:
        dt = clock.tick(50)
        savegame=pk.load(open("./save.p","rb"))

        # event handling
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and savegame['arrow_count'] > 0:
                    enemy_attack.create_arrow(arrow_list,arrow_dir,h_drctn,hero,sprite_layers) # create arrow on pressing 'w'
                    remove_mon(HP_MON,mon,mon_dir,mon_image,sprite_layers) # remove monster sprite if health bacomes zero
                    savegame['arrow_count'] -= 1 # decrease the arrow count and update in the dictionary
                    pk.dump(savegame,open("./save.p","wb")) # save the changes of dictionary
                elif event.key == pygame.K_a:
                     # attack with sword on pressing 'a'
                    enemy_attack.attack(h_drctn,hero,mon,HP_MON)
                    remove_mon(HP_MON,mon,mon_dir,mon_image,sprite_layers)

            # interface update
            menu.update_lg(l_g,c_pos)
            menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
            menu.update_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos,0)
            menu.update_f_i(f_i,c_pos)

        # calling hero_move() function for hero's movements
        mov = movements1.hero_move(mr,ml,md,mu,hero_pos_x,hero_pos_y,hero,speed,sprite_layers[3])
        mr = mov[0]
        ml = mov[1]
        md = mov[2]
        mu = mov[3]
        hero_pos_x = mov[4]
        hero_pos_y = mov[5]

        # to detect the direction of hero
        if(mu>1):
            h_drctn='up'
        elif(mr>1):
            h_drctn='right'
        elif(md>1):
            h_drctn='down'
        elif(ml>1):
            h_drctn='left'

        # decresing the HP of player if collides any of the monsters
        # if HP becomes zero then start the game again
        for i in range(len(mon)):
            if pygame.sprite.collide_rect(hero,mon[i]):
                ouch_sound = sound.create_soundfx('./sounds/weapon_touch.ogg')
                sound.volume(ouch_sound,0.4)
                if savegame['sheild_hp']>0:
                    savegame['sheild_hp'] -= (point_enm/2)
                    savegame['hp'] -= (point_enm/2)
                    if savegame['sheild_hp']<0:
                        savegame['sheild_hp'] = 0
                else :
                    savegame['hp'] -= point_enm 
                    if savegame['hp'] <= 0:
                        sound.stop_soundfx(tunnel2_4_sound)
                        savegame['xp'] = old_xp
                        savegame['h_level'] = old_level
                        savegame['sheild_hp'] = old_armor
                        savegame['arrow_count'] = old_arrow
                        savegame['hp'] = savegame['max_hp']
                        pk.dump(savegame,open("./save.p","wb"))
                        menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
                        life = 0
                        running = False
                pk.dump(savegame,open("./save.p","wb"))

        (mon_dir,mon,mon_image) = move_mon(mon_dir,mon,mon_image,sprite_layers,enm_speed) # monsters's movement
        enemy_attack.remove_arrow(arrow_list,mon,HP_MON,arrow_dir,sprite_layers,point_arrow) # remove arrow if it goes out of the screen
        remove_mon(HP_MON,mon,mon_dir,mon_image,sprite_layers) # remove monsters
        menu.update_lg(l_g,c_pos) #interface update
        
        # adjust camera according to the hero's position, follow him
        # (don't make the hero follow the cam, maybe later you want different
        #  objects to be followed by the cam)
        cam_pos_x = hero.rect.centerx
        cam_pos_y = hero.rect.centery
        if hero.rect.centerx <= 520 :
            cam_pos_x = 520
        elif hero.rect.centerx >=2336:
            cam_pos_x = 2336
        if hero.rect.centery >= 2875:
            cam_pos_y = 2875
        elif hero.rect.centery <=408:
            cam_pos_y = 408
        renderer.set_camera_position(cam_pos_x,cam_pos_y)

        # interface update
        c_pos=(cam_pos_x,cam_pos_y)
        interface.rect.topleft=(c_pos[0]-512,c_pos[1]-384)
        hp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-382)
        xp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-345)
        l_g.rect.topleft=(c_pos[0]-508,c_pos[1]-381)
        f_i.rect.bottomright=(c_pos[0]+500,c_pos[1]+350)
        interf_fight.rect.bottomright=(c_pos[0]+512,c_pos[1]+384)

        # next map
        if pygame.Rect.colliderect(hero.rect,portal1) or pygame.Rect.colliderect(hero.rect,portal2) :
            portal=True
            sound.stop_soundfx(tunnel2_4_sound)
            running=False

        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0, 0, 0))
        (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)

    # Game restarts              
    if life == 0:
        demo_pygame('./maps/tunnel2_4.tmx',0)

    elif portal==True:
        shifty1.demo_pygame('./maps/village1.tmx',1)


#  -----------------------------------------------------------------------------

# render the map
def render_update(renderer,sprite_layers,screen):
    #sprite_layers[1].remove_sprite(score)
    # render the map
    for sprite_layer in sprite_layers:
        if sprite_layer.is_object_group:
            # we dont draw the object group layers
            # you should filter them out if not needed
            continue
        else:
            renderer.render_layer(screen,sprite_layer)
    pygame.display.flip()
    return (renderer,sprite_layers,screen)

#image update for monster's movement
def imageupdate(mon_dir,mon,mon_image,i):
    if 0<= mon_image[i] <=6: mon_image[i] += 1
    elif mon_image[i]==7: mon_image[i] = 0
    if mon_image[i] == 0:
        if (mon_dir[2*i]==-1):  mon[i].image = pygame.image.load('./images/slime04.png')
        elif (mon_dir[2*i]==1 ): mon[i].image = pygame.image.load('./images/slime24.png')
        elif (mon_dir[(2*i)+1]==1): mon[i].image = pygame.image.load('./images/slime14.png')
        else: mon[i].image = pygame.image.load('./images/slime34.png')
    elif mon_image[i] == 3:
        if (mon_dir[2*i]==-1):  mon[i].image = pygame.image.load('./images/slime05.png')
        elif (mon_dir[2*i]==1 ): mon[i].image = pygame.image.load('./images/slime25.png')
        elif (mon_dir[(2*i)+1]==1): mon[i].image = pygame.image.load('./images/slime15.png')
        else: mon[i].image = pygame.image.load('./images/slime35.png')
    return (mon,mon_image)

# monster movement
def move_mon(mon_dir,mon,mon_image,sprite_layers,speed1):
    i = 0
    for i in range(len(mon)):
        next_dir = random.randint(0,1000)
        # if it collides to the collision layer then change the direction
        step_x, step_y = movements1.check_collision(mon[i].rect.centerx, mon[i].rect.centery, speed1*mon_dir[2*i],speed1*mon_dir[(2*i)+1],\
                                                    mon[i].rect.width, 5, sprite_layers[3])
        dx = step_x*100
        dy = step_y*100
        # randomly change the direction of monster depending of next_dir
        if (((-2<dx<2) & (-2<dy<2)) | (next_dir%25 == 0)):
            mon_dir[2*i] = (-1)*mon_dir[2*i]
            mon_dir[(2*i)+1] = (-1)*mon_dir[(2*i)+1]
        (mon,mon_image) = imageupdate(mon_dir,mon,mon_image,i)
        mon[i].rect.centerx += speed1*mon_dir[2*i]
        mon[i].rect.centery += speed1*mon_dir[(2*i)+1]
    return (mon_dir,mon,mon_image)

# remove monsters after their health becomes zero
def remove_mon(HP_MON,mon,mon_dir,mon_image,sprite_layers):
    savegame=pk.load(open("./save.p","rb"))
    i = 0
    l = len(mon)
    while(i<l and i>=0):
        if HP_MON[i] <= 0:
            sprite_layers[1].remove_sprite(mon[i])
            savegame['xp'] += 2
            mon.pop(i)
            mon_dir.pop(i*2)
            mon_dir.pop(i*2)
            mon_image.pop(i)
            HP_MON.pop(i)
        else:
            i +=1
        l = len(mon)
    pk.dump(savegame,open("./save.p","wb"))

if __name__ == '__main__':
    main(0)

