
import sys
import os
import math
import cPickle as pk
import pygame
try:
    import _path
except:
    pass
import tiledtmxloader
from pygame import mixer

import person , movements1
import shifty1
import menu

#  -----------------------------------------------------------------------------

def main():
	 # main function for running the same code for test runs
    demo_pygame('./maps/knifehouse.tmx')

#  -----------------------------------------------------------------------------

def demo_pygame(file_name):
 
    file = './sounds/Firestrm.ogg'
    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)
    mixer.init()
    # loading the sound files in different sound formats of mixer and main background sound in mixer stream 
    sound_ouch = mixer.Sound('./sounds/pain.ogg')
    mixer.music.load(file)
    mixer.music.play(-1);
	
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

    # create hero sprite
    # use floats for hero position
    hero_pos_x = 18*32+16
    hero_pos_y = 22*32
    hero = person.create_person(hero_pos_x, hero_pos_y ,'./images/hero_u2.png')
    # dimensions of the hero for collision detection
    
    hero_width = hero.rect.width
    hero_height = 5
	# create knife sprite
    knife_pos_x =  8 *32 
    knife_pos_y = 21 * 32 
    knife = create_knife(knife_pos_x, knife_pos_y)
	# create coin sprite
    coin_pos_x = 28*32 +16
    coin_pos_y = 16*32
    coin = create_coin(coin_pos_x, coin_pos_y)
 
    # cam_offset is for scrolling
    cam_world_pos_x = 1024/2
    cam_world_pos_y = 768/2
    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height)

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    # filter layers
    sprite_layers = [layer for layer in sprite_layers if not layer.is_object_group]

    # add the hero the the right layer, it can be changed using 0-9 keys
    sprite_layers[3].add_sprite(hero)
    sprite_layers[2].add_sprite(coin)
    sprite_layers[2].add_sprite(knife)

    # layer add/remove hero keys
    num_keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, \
                    pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]


    ###FOR INTERFACE on top-left corner loading the libraries from menu file and loading the local variables into the function 
    savegame=pk.load(open("./save.p","rb"))
    HERO_HEALTH = savegame['hp'] # loading the last hero health 
    hp=savegame['hp']
    hp_max=savegame['max_hp']   # keep updating the values in pk file 
    c_pos=[cam_world_pos_x, cam_world_pos_y]
    
	#c_pos=camra.camera(file_name,renderer,hero)       
    interf_toggle=0
    interface=menu.create_interface(renderer,sprite_layers,screen,c_pos) 
    hp_sprite=person.create_person(c_pos[0],c_pos[1],'./images/hp_bar.png')
    l_g=menu.create_l_g(renderer,sprite_layers,screen,c_pos)
    [hp_sprite,hp]=menu.create_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos)
	#for showing the xp in the interface
    xp_sprite=person.create_person(c_pos[0],c_pos[1],'./images/exp_bar.png')
    xp_sprite=menu.create_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos)

    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    speed = 4.75
	# setting up an environment for shifting the map while exiting from the map
    portal1 = pygame.Rect(17*32,22*32,96,32)
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    mr=ml=md=mu=0
    
    # mainloop
    while running:
        dt = clock.tick(50)  # value set to work same with different processors 
		## continously moving the interface and saving the health and other data in the files
        savegame=pk.load(open("./save.p","rb"))
        interface.rect.topleft=(c_pos[0]-512,c_pos[1]-384)
        hp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-382)
        xp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-345)
        l_g.rect.topleft=(c_pos[0]-508,c_pos[1]-381)

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                print("fps: ", clock.get_fps())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    mixer.music.stop()


            menu.update_lg(l_g,c_pos)
            menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
            menu.update_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos,0)

        # find directions
		# loading commom movement of hero stored in movements1 file and chaning its positions 
        mov = movements1.hero_move(mr,ml,md,mu,hero_pos_x,hero_pos_y,hero,speed,sprite_layers[4])
        mr = mov[0]
        ml = mov[1]
        md = mov[2]
        mu = mov[3]
        hero_pos_x = mov[4]
        hero_pos_y = mov[5]
        # fire collision health loss 
        if(fire_ouch(hero_pos_x,hero_pos_y,sprite_layers[1])):
            sound_ouch.play()
            dmg=0.85
			# updating the new health
            menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,dmg)
            savegame['hp'] -=dmg
            HERO_HEALTH -=dmg
            if(HERO_HEALTH < 0):
				# setting the hero kill position from fire
                savegame['hp']=savegame['max_hp']
                HERO_HEALTH = savegame['hp']
                hero_pos_x = 18*32+16
                hero_pos_y = 22*32
				# if knife and coin not taken adding them here 
                if( not sprite_layers[2].contains_sprite(knife)):
                 sprite_layers[2].add_sprite(knife)
                if( not sprite_layers[2].contains_sprite(coin)):
                 sprite_layers[2].add_sprite(coin)

            
        # getting coin here
        if(pygame.sprite.collide_rect(hero,coin)):
           sprite_layers[2].remove_sprite(coin)

        #getting knife here
        if(pygame.sprite.collide_rect(hero,knife)):
           sprite_layers[2].remove_sprite(knife)
		# collision with portal for changing map
        if(portal1.collidepoint(hero.rect.midbottom) and not sprite_layers[2].contains_sprite(coin) \
            and not sprite_layers[2].contains_sprite(knife)):
            mixer.music.stop()
            savegame['b_h_vil']=1
            savegame['talk_vil']['./maps/village1.tmx'][1]=1
            savegame['dagger']=1
            savegame['eqp_weapon']='dagger'
            pk.dump(savegame,open("./save.p","wb"))
            running=False
            #CODE FOR MAP CHANGING HERE.........
        # condition for shifting map
        
        # adjust camera according to the hero's position, follow him
        # (don't make the hero follow the cam, maybe later you want different
        #  objects to be followd by the cam)
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

        pk.dump(savegame,open("./save.p","wb"))
        pygame.display.flip()
	# calling the other map after completion of catching all the fishes
    shifty1.demo_pygame('./maps/village1.tmx',2) 

#  -----------------------------------------------------------------------------

# returning bool for collision with any fire 
def fire_ouch(hero_pos_x,hero_pos_y,fire_layer):
	# calculating the tile numbers
    tile_x = int((hero_pos_x) // fire_layer.tilewidth)
    tile_y = int((hero_pos_y) // fire_layer.tileheight)
    if fire_layer.content2D[tile_y][tile_x] is not None:
        return True
    else:
        return False
## making the coin and knife sprite here jsut like hero in person file without any movemennt 
def create_coin(start_pos_x, start_pos_y):
    image = pygame.image.load('./images/coin.png')
    image = pygame.transform.scale(image,(55,55))
    rect = image.get_rect()
    rect.midbottom = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)

def create_knife(start_pos_x, start_pos_y):
    image = pygame.image.load('./images/knife.png')
    rect = image.get_rect()
    rect.midbottom = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)


#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()


