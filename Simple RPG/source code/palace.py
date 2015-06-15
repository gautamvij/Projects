#!/usr/bin/python
import sys
import os
import math
import random
import time
import movements1
import person
import pygame
import tiledtmxloader
import person
import sound
import enemy_attack
import cPickle as pk
import menu

try:
    import _path
except:
    pass



#  -----------------------------------------------------------------------------

def main():
    demo_pygame('./maps/palace_final.tmx',0)

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
    battlefield_sound = sound.create_music(file_name)
    
    # create hero
    hero_pos_x = 10*32
    hero_pos_y = 41*32
    hero = person.create_person(hero_pos_x, hero_pos_y,'./images/hero_u2.png')
    
    # create enemy sprites
    enm = []
    enm.append(person.create_person(10*32, 3*32,'./images/haabu_d1.png'))
    enm.append(person.create_person(14*32, 3*32,'./images/haabu_d1.png'))
    enm.append(person.create_person(10*32, 7*32,'./images/haabu_d1.png'))
    enm.append(person.create_person(14*32, 7*32,'./images/haabu_d1.png'))

    # create dragon sprite
    dragon = person.create_person(10*32, 27*32,'./images/dragon_d1.png')
    
    # cam_offset is for scrolling
    cam_world_pos_x = 520
    cam_world_pos_y = 1050

    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height)

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    # filter layers
    sprite_layers = [layer for layer in sprite_layers if not layer.is_object_group]

    # add the hero and enemies the the right layer
    sprite_layers[1].add_sprite(hero)
    sprite_layers[1].add_sprite(dragon)
    i = 0
    for i in range(len(enm)):
        sprite_layers[1].add_sprite(enm[i])
    
    # variables for the main loop
    clock = pygame.time.Clock()
    running = True # to run while loop
    speed = 7  # hero speed 
    mr=ml=md=mu=0  # image variables(change images to show movements of hero)
    
    tic_flag = 0
    drctn='down' # direction where hero facing right now
    life = 1 # to keep track wheather hero is alive or not
    arrow_list = [] # contains a list of arrows (currently on screen)
    arrow_dir = [] # directions of arrows
    enm_dir = [0,0,0,0]
    drag = [dragon]
    dx_dragon = [0]
    image_variable = [0]
    weap_dir = [] # directions of weapons 
    weap_list = [] # contains a list of weapons (currently on screen)
    color_change = 0 # a color variable for dragon
    dy_dragon = [1] # dragon direction
    specialarrow_list = [] # contains a list of specialarrows (currently on screen)
    specialarrow_dir = [] # directions of specialarrows
    dragonimages = ['./images/dragon_d1.png','./images/dragon_d2.png','./images/dragon_d3.png','./images/dragon_u1.png','./images/dragon_u2.png','./images/dragon_u3.png']
    enemyimages = ['./images/haabu_d1.png','./images/haabu_d2.png','./images/haabu_d3.png','./images/haabu_u1.png','./images/haabu_u2.png','./images/haabu_u3.png']
    chk = 0

    HP_ENM = [100.0,100.0,100.0,100.0] # health of enemies
    HP_DRAGON = [100.0] # health of dragon
    SPECIALARROW = 5    
    point_weapon = 1.0   # decrease in health of hero when weapon OR haabu collides with hero  ## HAABU MEANS ENEMY (in HINDI)
    point_arrow = 20.0    # arrow enemy collision
    point_dragon = 5.0    # hero dragon collision
    point_specialarrow = 10.0  # specialarrow hero collision
    haabu_speed = 6
    dragon_speed = 8

    #old variables to restore if hero dies in this map
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
    xp_sprite=person.create_person(c_pos[0],c_pos[1],'./images/exp_bar.png') # xp interface
    xp_sprite=menu.create_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos)
    s_a=menu.create_s_a(renderer,sprite_layers,screen,c_pos)
    f_i=menu.create_f_i(renderer,sprite_layers,screen,c_pos) # arrow,armor,sword interface
    interf_fight=menu.create_interface_fight(renderer,sprite_layers,screen,c_pos)
    spec_interf=menu.create_interface_spec_arrow(renderer,sprite_layers,screen,c_pos)

    d_hp=menu.create_interface_dragon(renderer,sprite_layers,screen,c_pos)
    dhp_sprite=person.create_person(c_pos[0]-400,c_pos[1],'./images/dragon_health.png') #dragon health interface
    dhp_sprite=menu.create_dragon_hp(renderer,sprite_layers,screen,dhp_sprite,c_pos,HP_DRAGON)
    
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # mainloop
    while running:
        dt = clock.tick(70)
        savegame=pk.load(open("./save.p","rb"))

        # keep adding a group of four enemies after dying previous group
        if len(enm)==0: 
            color_change += 1
            enm.append(person.create_person(10*32, 3*32,'./images/haabu_d1.png'))
            enm.append(person.create_person(14*32, 3*32,'./images/haabu_d1.png'))
            enm.append(person.create_person(10*32, 7*32,'./images/haabu_d1.png'))
            enm.append(person.create_person(14*32, 7*32,'./images/haabu_d1.png'))
            HP_ENM = [100.0,100.0,100.0,100.0]
            enm_dir = [0,0,0,0]
            i = 0
            for i in range(len(enm)):
                sprite_layers[1].add_sprite(enm[i])

        # dragon can be killed only if it is of orange color and only by specialarrows
        # five specialarrows are provided when dragon becomes orange
        if color_change%2==0:
            SPECIALARROW = 0
            chk = 0
            dragonimages = ['./images/dragon_d1.png','./images/dragon_d2.png','./images/dragon_d3.png','./images/dragon_u1.png','./images/dragon_u2.png','./images/dragon_u3.png']
        else:
            if chk == 0: 
                SPECIALARROW = 5
            chk = 1
            dragonimages = ['./images/orange_d1.png','./images/orange_d2.png','./images/orange_d3.png','./images/orange_u1.png','./images/orange_u2.png','./images/orange_u3.png']
            #spec_arrow_interf
            menu.update_s_a(s_a,c_pos,SPECIALARROW)
        # event handling
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and savegame['arrow_count'] > 0:
                    enemy_attack.create_arrow(arrow_list,arrow_dir,drctn,hero,sprite_layers) # create arrow on pressing 'w'
                    haabu_remove(enm,HP_ENM,sprite_layers,enm_dir)  # remove enemy sprite if health bacomes zero
                    savegame['arrow_count'] -=1 # decrease the arrow count and update in the dictionary
                    pk.dump(savegame,open("./save.p","wb")) # save the changes of dictionary
                elif event.key == pygame.K_a:
                    # attack with sword on pressing 'a'
                    enemy_attack.attack(drctn,hero,enm,HP_ENM)
                    haabu_remove(enm,HP_ENM,sprite_layers,enm_dir)
                elif event.key == pygame.K_s and color_change%2!=0 and SPECIALARROW > 0:
                    # attack with specialarrow on pressing 's'
                    enemy_attack.create_specialarrow(specialarrow_list,specialarrow_dir,drctn,hero,sprite_layers)
                    SPECIALARROW -= 1
                    
                # interface update
                menu.update_lg(l_g,c_pos)
                menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
                menu.update_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos,0)
                menu.update_f_i(f_i,c_pos)
                menu.update_dhp_bar(renderer,sprite_layers,screen,dhp_sprite,c_pos,HP_DRAGON)
                
                if(color_change%2==1):
                    menu.update_s_a(s_a,c_pos,SPECIALARROW)

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
            drctn='up'
        elif(mr>1):
            drctn='right'
        elif(md>1):
            drctn='down'
        elif(ml>1):
            drctn='left'

        haabu_move(hero,enm,enm_dir,enemyimages,haabu_speed) # random movement of enemy
        haabu_remove(enm,HP_ENM,sprite_layers,enm_dir)# remove enemy if health of enemy becomes zero
        
        if(color_change%2==0):enemy_attack.create_weapons(weap_list,sprite_layers,drag,weap_dir,dy_dragon,1) # create the weapons only if it is not of orange color
        enemy_attack.remove_weapon(hero,enm,weap_list,weap_dir,point_weapon,sprite_layers)

        # interface update
        menu.update_lg(l_g,c_pos)
        menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
        menu.update_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos,0)
        menu.update_f_i(f_i,c_pos)
        menu.update_dhp_bar(renderer,sprite_layers,screen,dhp_sprite,c_pos,HP_DRAGON)
        
        enemy_attack.move_enemy(drag,[19*32],[1*32],dx_dragon,dragon_speed)# random movement of dragon
        enemy_attack.dir_update(drag,hero,dy_dragon) # direction update of enemy
        enemy_attack.image_update(drag,image_variable,dy_dragon,dragonimages) # image update of enemy

        enemy_attack.remove_arrow(arrow_list,enm,HP_ENM,arrow_dir,sprite_layers,point_arrow) # removes arrow from the screen
        enemy_attack.remove_arrow(specialarrow_list,drag,HP_DRAGON,specialarrow_dir,sprite_layers,point_specialarrow) # removes specialarrow from the screen

        # decrease health of hero if it colldes with dragon
        if pygame.sprite.collide_rect(hero,drag[0]):
            weap_sound = sound.create_soundfx('./sounds/weapon_touch.ogg')
            sound.volume(weap_sound,0.4)
            savegame=pk.load(open("./save.p","rb"))
            savegame['hp'] -= point_dragon
            pk.dump(savegame,open("./save.p","wb"))
            
        # game starts again if player dies
        if savegame['hp'] <= 0:
            sound.stop_soundfx(battlefield_sound)
            savegame['xp'] = old_xp
            savegame['h_level'] = old_level
            savegame['sheild_hp'] = old_armor
            savegame['arrow_count'] = old_arrow
            savegame['hp'] = savegame['max_hp']
            pk.dump(savegame,open("./save.p","wb"))
            menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
            life = 0
            running = False

        # Game ends!
        # clean the screen!
        if HP_DRAGON[0] <= 0:
            i = 0
            l = len(enm)
            while(i>=0 and i<l):
                sprite_layers[1].remove_sprite(enm[i])
                enm.pop(i)
                l = len(enm)
            i = 0
            l = len(weap_list)
            while(i>=0 and i<l):
                sprite_layers[2].remove_sprite(weap_list[i])
                weap_list.pop(i)
                l = len(weap_list)
            i = 0
            l = len(arrow_list)
            while(i>=0 and i<l):
                sprite_layers[1].remove_sprite(arrow_list[i])
                arrow_list.pop(i)
                l = len(arrow_list)
            i = 0
            l = len(specialarrow_list)
            while(i>=0 and i<l):
                sprite_layers[1].remove_sprite(specialarrow_list[i])
                specialarrow_list.pop(i)
                l = len(specialarrow_list)
            sprite_layers[1].remove_sprite(drag[0])
            render_update(renderer,sprite_layers,screen)
            sound.stop_soundfx(battlefield_sound)
            running = False
            life = 2
            
        # adjust camera according to the hero's position, follow him
        cam_pos_x = hero.rect.centerx
        cam_pos_y = hero.rect.centery
        if hero.rect.centerx <= 520 :
            cam_pos_x = 520
        if hero.rect.centery >=1050:
            cam_pos_y = 1050
        elif hero.rect.centery <=407:
            cam_pos_y = 407
        renderer.set_camera_position(cam_pos_x, cam_pos_y)

        # interface update
        c_pos=(cam_pos_x,cam_pos_y)
        interface.rect.topleft=(c_pos[0]-512,c_pos[1]-384)
        hp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-382)
        xp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-345)
        l_g.rect.topleft=(c_pos[0]-508,c_pos[1]-381)
        f_i.rect.bottomright=(c_pos[0]+500,c_pos[1]+350)
        interf_fight.rect.bottomright=(c_pos[0]+512,c_pos[1]+384)
        dhp_sprite.rect.midbottom=(c_pos[0],c_pos[1]+350)
        d_hp.rect.midbottom=(c_pos[0],c_pos[1]+350)
        spec_interf.rect.topleft=(c_pos[0]-512,c_pos[1]-240)
        s_a.rect.topleft=(c_pos[0]-540,c_pos[1]-280)

        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0, 0, 0))
        (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
        
    if life == 0:
        demo_pygame('./maps/palace_final.tmx',0)
    elif life ==2:
        # Game ends!
        # Quit the window after pressing 'Esc'
        running = True
        ending_sound = sound.create_soundfx('./sounds/ending.ogg')
        sound.volume(ending_sound,1)
        while running :
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE ):
                    sound.stop_soundfx(ending_sound)
                    running = False
        pygame.quit()

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

# remove enemies
# increase hp of hero after killing enemies
def haabu_remove(enm,HP_ENM,sprite_layers,enm_dir):
    i = 0
    l = len(enm)
    while(i>=0 and i<l):
        if HP_ENM[i]<=0:
            savegame=pk.load(open("./save.p","rb"))
            savegame['xp']+=10
            pk.dump(savegame,open("./save.p","wb"))
            sprite_layers[1].remove_sprite(enm[i])
            enm.pop(i)
            enm_dir.pop(i)
            HP_ENM.pop(i)
        else:
            i += 1
        l = len(enm)

# movement of enemies according to position of hero      
def haabu_move(hero,enm,enm_dir,enemyimages,speed):
    i = 0
    dy_enm = []
    for i in range(len(enm)):
        if(hero.rect.centerx > enm[i].rect.centerx):
            dx = 1
        else:
            dx = -1
        if(hero.rect.centery > enm[i].rect.centery+32):
            dy = 1
            dy_enm.append(dy)
        else:
            dy = -1
            dy_enm.append(dy)
        enm[i].rect.centerx += speed*dx
        enm[i].rect.centery += speed*dy
        j = 0
        for j in range(i+1,len(enm)):
            if pygame.sprite.collide_rect(enm[i],enm[j]):
                enm[i].rect.centerx -= speed*dx
                enm[i].rect.centery -= speed*dy
    enemy_attack.image_update(enm,enm_dir,dy_enm,enemyimages)
    del dy_enm

if __name__ == '__main__':
    main()


