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
import enemy_attack
import sound
import shifty1
import cPickle as pk
import menu

try:
    import _path
except:
    pass



#  -----------------------------------------------------------------------------

def main():
    demo_pygame('./maps/tunnel3.tmx',0)

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
    tunnel3_sound = sound.create_music(file_name)
    sound.volume(tunnel3_sound,0.1)
    
    # create hero,enemy sprites
    hero_pos_x = 12*32
    hero_pos_y = 3*32
    hero = person.create_person(hero_pos_x, hero_pos_y,'./images/hero_u2.png')
    
    # create enemy,crabs and ring sprites
    enm1 = person.create_person(6*32, 22*32,'./images/slime_d1.png')
    enm2 = person.create_person(16*32, 22*32,'./images/slime_d1.png')
    crab = person.create_person(30*32, 38*32,'./images/crab.png')
    crab1 = person.create_person(49*32, 38*32,'./images/crab.png')
    ring = person.create_person(49*32, 33*32,'./images/ring.png')
    
    # cam_offset is for scrolling
    cam_world_pos_x = screen_width
    cam_world_pos_y = screen_height

    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height)

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    # filter layers
    sprite_layers = [layer for layer in sprite_layers if not layer.is_object_group]

    # add the hero and enemies to the right layer
    sprite_layers[1].add_sprite(hero)
    sprite_layers[1].add_sprite(enm1)
    sprite_layers[1].add_sprite(enm2)
    
    # variables for the main loop
    clock = pygame.time.Clock()
    running = True  # to run while loop
    speed = 7  # hero speed
    mr=ml=md=mu=0  # image variables(change images to show movements of hero)
    
    flag_crab = 0  # a variable to check when to add crab's sprite
    drctn='down' # direction where hero facing right now
    life = 1 # to keep track wheather hero is alive or not
    enm =[enm1,enm2] # list of enemy sprites
    dx_enm = [1,1] # list of direction in x of enemies
    dy_enm = [-1,-1] # list of direction in y of enemies
    left_enm = [1*32,9*32] # left collision coordinate for enemies(after which it will return back)
    right_enm = [12*32,21*32] # right collision coordinate for enemies(after which it will return back)
    weap_dir = [] # directions of weapons 
    weap_list = [] # contains a list of weapons (currently on screen) 
    arrow_list = [] # contains a list of arrows (currently on screen)
    arrow_dir = [] # directions of arrows
    # contains a list of enemy images
    enmimages = ['./images/slime_d1.png','./images/slime_d2.png','./images/slime_d3.png','./images/slime_u1.png','./images/slime_u2.png','./images/slime_u3.png']
    gold = [] # contains a list of gold (currently on screen)
    heart = [] # contains a list of heart (currently on screen)
    image_variable = [0,0]
    flag_ring = 0
    tic_flag = 0
    x = 0
    portal1 = pygame.Rect(58*32,28*32,2*32,8*32)
    portal=False

    point_weapon = 2.0 # decrease in health of hero when weapon of enemy collides with hero
    point_arrow = 15.0 # decrease in health of enemy when arrow of hero collides with enemy
    crab_attack = 10.0 # attack of crab
    point_heal = 20.0 # increase in health after healing
    HP_CRAB = 30.0 # health of crab
    gold_increase = 5 # increase in health of hero after getting gold
    heart_increase = 5.0 # increase in health of hero after getting heart
    speed_enm = 6 # speed of enemy
    HP_ENM = [100.0,100.0] # health of enemies
    hero_attack = 10 # hero attack
    defense_hero = 5 # hero defense

    #old variables to restore if hero dies in this map
    savegame=pk.load(open("./save.p","rb"))
    old_xp = savegame['xp']
    old_level = savegame['h_level']
    old_gold = savegame['gold']
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
    f_i=menu.create_f_i(renderer,sprite_layers,screen,c_pos) # arrow,armor,sword interface
    interf_fight=menu.create_interface_fight(renderer,sprite_layers,screen,c_pos)
    
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # mainloop
    while running:
        dt = clock.tick(50)
        savegame=pk.load(open("./save.p","rb"))
        
        #set coordinates on which turn based fighting appears
        if(hero_pos_x > 24*32 and flag_crab == 0 and len(enm)==0):    
            flag_crab = 1
        if(hero_pos_x > 43*32 and flag_crab == 2):
            flag_crab = 3
           
        # event handling
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and savegame['arrow_count'] > 0:
                    enemy_attack.create_arrow(arrow_list,arrow_dir,drctn,hero,sprite_layers) # create arrow on pressing 'w'
                    enemy_attack.remove_enm(HP_ENM,enm,dx_enm,right_enm,left_enm,dy_enm,sprite_layers,gold,heart) # remove enemy sprite if health bacomes zero
                    savegame['arrow_count'] -=1 # decrease the arrow count and update in the dictionary
                    pk.dump(savegame,open("./save.p","wb")) # save the changes of dictionary
                elif event.key == pygame.K_a:
                    # attack with sword on pressing 'a'
                    enemy_attack.attack(drctn,hero,enm,HP_ENM)
                    enemy_attack.remove_enm(HP_ENM,enm,dx_enm,right_enm,left_enm,dy_enm,sprite_layers,gold,heart) # remove enemy sprite if health bacomes zero

            # interface update
            menu.update_lg(l_g,c_pos)
            menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
            menu.update_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos,0)
            menu.update_f_i(f_i,c_pos)

        # if one enemy dies then other enemy's walking area increases(other enemy covers the region of previous enemy)            
        if len(enm)==1:
            right_enm[0] = 19*32
            left_enm[0] = 2*32
            
        # add crab sprite for turn based fighting
        if(flag_crab == 1):
            sprite_layers[1].add_sprite(crab)
            flag_crab = 2
            x = 35
            (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
        elif(flag_crab == 3):
            crab = crab1
            x = 54
            sprite_layers[1].add_sprite(crab)
            HP_CRAB = 30.0
            flag_crab = 4
            (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)

        # loop for turn based fighting until crab doesn't die
        while(HP_CRAB > 0 and (flag_crab==2 or flag_crab==4)):
            for event in pygame.event.get():
                # heal on pressing 'h'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h and tic_flag==0:
                    heal_sound = sound.create_soundfx('./sounds/heal.ogg')
                    sound.volume(heal_sound,0.4)
                    heal = person.create_person(hero.rect.centerx,hero.rect.top+11,'./images/heal_1.png') # create the heal sprite
                    sprite_layers[2].add_sprite(heal) # add the sprite to the right layer
                    savegame['hp'] += point_heal # increase the health and upadte in the dictionary
                    if savegame['hp'] > savegame['max_hp']:
                        savegame['hp'] = savegame['max_hp']
                    pk.dump(savegame,open("./save.p","wb")) # save the changes in dictionary
                    # interface update
                    menu.update_lg(l_g,c_pos)
                    menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
                    menu.update_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos,0)
                    # image update
                    while tic_flag<=13:
                        heal.image=pygame.image.load('./images/heal_1.png')
                        (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                        heal.image=pygame.image.load('./images/heal_2.png')
                        (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                        heal.image=pygame.image.load('./images/heal_3.png')
                        (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                        tic_flag += 1
                    tic_flag = 25
                    # remove the heal sprite
                    sprite_layers[2].remove_sprite(heal)
                    # rendering
                    (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_a and tic_flag==0:
                    # hero attacks on pressing 'a'
                    sword_sound = sound.create_soundfx('./sounds/sword.ogg')
                    sound.volume(sword_sound,0.4)
                    var_attack_hero = random.randint(hero_attack-2.0, hero_attack+2.0)
                    HP_CRAB -= var_attack_hero # crab's health decreases
                    enemy_attack.create_score(var_attack_hero)
                    # crab's image changes after hero attacks
                    crab.image=pygame.image.load('./images/crab_1.png')
                    (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                    crab.image=pygame.image.load('./images/crab_2.png')
                    (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                    crab.image=pygame.image.load('./images/crab_3.png')
                    (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                    crab.image=pygame.image.load('./images/crab_3.png')
                    # create the score sprite and add it
                    score = person.create_person(x*32,32*32,'./images/sample-out.png')
                    sprite_layers[1].add_sprite(score)
                    while(tic_flag<25):
                        score.rect.centery -= 2
                        tic_flag += 1
                        if(tic_flag == 25): sprite_layers[1].remove_sprite(score)
                        (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                    crab.image=pygame.image.load('./images/crab.png')
            if tic_flag == 25:
                pygame.time.delay(1000)
                # crab attacks
                var_attack_crab = random.randint(crab_attack-2.0,crab_attack+2.0)
                var_defense_hero = random.randint(defense_hero-3.0,defense_hero)
                sh = (var_attack_crab - var_defense_hero)
                if  sh<0 : sh = 0
                enemy_attack.create_score(sh)
                savegame['hp'] -= (sh)
                pk.dump(savegame,open("./save.p","wb"))
                # crab's image changes when it attacks
                shine = 0
                while shine < 10 :
                    crab.image=pygame.image.load('./images/crab(1).png')
                    (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                    crab.image=pygame.image.load('./images/crab.png')
                    (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                    shine += 1
                turnbase_sound = sound.create_soundfx('./sounds/turnbase_touch.ogg')
                sound.volume(turnbase_sound,0.4)
                # interface update
                menu.update_lg(l_g,c_pos)
                menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
                menu.update_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos,0)
                # create the score sprite and add it  
                score = person.create_person(hero_pos_x-32,hero_pos_y-32,'./images/sample-out.png')
                sprite_layers[1].add_sprite(score)
                while(tic_flag>0):
                    score.rect.centery += 2
                    tic_flag -= 1
                    if(tic_flag == 0): sprite_layers[1].remove_sprite(score)
                    (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                    
        # if crab's HP is zero then remove its sprite
        if(HP_CRAB <= 0) :
            sprite_layers[1].remove_sprite(crab)

        # add the ring sprite when second crab dies
        if(x==54):
            sprite_layers[1].add_sprite(ring)

        # increase the xp of player after killing the crab
        if(x==35 or x==54):
            savegame['xp'] +=15
            pk.dump(savegame,open("./save.p","wb"))
            x = 30

        # remove sprite when hero collides ring
        if pygame.sprite.collide_rect(hero,ring) and flag_ring!=1:
            ring_sound = sound.create_soundfx('./sounds/gold_heart.ogg')
            sound.volume(ring_sound,0.5)
            sprite_layers[1].remove_sprite(ring)
            flag_ring = 1
            ring_take=person.create_person(hero.rect.centerx,hero.rect.centery+200,'./images/ring_take.png')
            sprite_layers[2].add_sprite(ring_take)
            (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
            i=0
            while(i!=1): # Infinite loop until menu is to be removed
                for event in pygame.event.get():
                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                        i=1
                continue
            sprite_layers[2].remove_sprite(ring_take)

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

        enemy_attack.create_weapons(weap_list,sprite_layers,enm,weap_dir,dy_enm,0) # create the weapons
        enemy_attack.move_enemy(enm,right_enm,left_enm,dx_enm,speed_enm)  # random movement of enemy
        enemy_attack.dir_update(enm,hero,dy_enm) # direction update of enemy
        enemy_attack.image_update(enm,image_variable,dy_enm,enmimages) # image update of enemy

        enemy_attack.remove_arrow(arrow_list,enm,HP_ENM,arrow_dir,sprite_layers,point_arrow) # remove arrow if it goes out of the screen
        enemy_attack.remove_enm(HP_ENM,enm,dx_enm,right_enm,left_enm,dy_enm,sprite_layers,gold,heart) # remove enemy if health of enemy becomes zero
        enemy_attack.remove_weapon(hero,enm,weap_list,weap_dir,point_weapon,sprite_layers) # remove weapon

        # interface update
        menu.update_f_i(f_i,c_pos)

        i = 0
        l = len(gold)
        # if hero collides with gold sprite then increase the gold count and remove the sprite
        while(i>=0 and i<l):
            if pygame.sprite.collide_rect(hero,gold[i]):
                savegame=pk.load(open("./save.p","rb"))
                savegame['gold'] += gold_increase
                pk.dump(savegame,open("./save.p","wb"))
                gold_sound = sound.create_soundfx('./sounds/gold_heart.ogg')
                sound.volume(gold_sound,0.3)
                sprite_layers[1].remove_sprite(gold[i])
                gold.pop(i)
            else: i+= 1
            l = len(gold)

        # if hero collides with heart sprite then increase the hp and remove the sprite
        i = 0
        l = len(heart)
        while(i>=0 and i<l):
            if pygame.sprite.collide_rect(hero,heart[i]):
                savegame=pk.load(open("./save.p","rb"))
                savegame['hp'] += heart_increase
                if savegame['hp'] > savegame['max_hp']:
                    savegame['hp'] = savegame['max_hp']
                pk.dump(savegame,open("./save.p","wb"))
                heart_sound = sound.create_soundfx('./sounds/gold_heart.ogg')
                sound.volume(heart_sound,0.3)
                sprite_layers[1].remove_sprite(heart[i])
                heart.pop(i)
            else: i+= 1
            l = len(heart)

        # game starts again if player dies
        if savegame['hp'] <= 0:
            sound.stop_soundfx(tunnel3_sound)
            savegame['xp'] = old_xp
            savegame['h_level'] = old_level
            savegame['gold'] = old_gold
            savegame['sheild_hp'] = old_armor
            savegame['arrow_count'] = old_arrow
            savegame['hp'] = savegame['max_hp']
            pk.dump(savegame,open("./save.p","wb"))
            menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
            life = 0
            running = False

        # another map starts 
        if (flag_ring==1 and pygame.Rect.colliderect(hero.rect,portal1)):
            portal=True
            sound.stop_soundfx(tunnel3_sound)
            running=False

            
        # adjust camera according to the hero's position, follow him
        cam_pos_x = hero.rect.centerx
        cam_pos_y = hero.rect.centery
        if hero.rect.centerx <= 524 :
            cam_pos_x = 524
        elif hero.rect.centerx >=1459:
            cam_pos_x = 1459
        if hero.rect.centery <=406:
            cam_pos_y = 406
        renderer.set_camera_position(cam_pos_x,cam_pos_y)

        # interface update
        c_pos=(cam_pos_x,cam_pos_y)
        interface.rect.topleft=(c_pos[0]-512,c_pos[1]-384)
        hp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-382)
        xp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-345)
        l_g.rect.topleft=(c_pos[0]-508,c_pos[1]-381)
        f_i.rect.bottomright=(c_pos[0]+500,c_pos[1]+350)
        interf_fight.rect.bottomright=(c_pos[0]+512,c_pos[1]+384)

        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0, 0, 0))
        (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
    if life == 0:
        demo_pygame('./maps/tunnel3.tmx',0)

    elif portal==True:
        shifty1.demo_pygame('./maps/ship.tmx',0)
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
    
if __name__ == '__main__':
    main()


