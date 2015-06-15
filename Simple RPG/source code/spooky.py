import sys
import os
import math
import random
import cPickle as pk
import tiledtmxloader
import pygame
from pygame import mixer

#import required modules
import person,movements1
import talk
import menu
import sound
import shifty1


try:
    import _path
except:
    pass



def main():
    #pass mapname
    demo_pygame('./maps/spooky.tmx')

def demo_pygame(file_name):
    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    mixer.init()
    #background music
    sound = mixer.Sound('./sounds/bats.ogg')
    file = './sounds/spooky.ogg'
    m = mixer.music.load(file)
    mixer.music.play(-1);
    
    #set up a screen
    screen_width = min(950, world_map.pixel_width)
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
    hero_pos_x = 400
    hero_pos_y = 800
    hero = person.create_person(hero_pos_x, hero_pos_y ,'./images/hero_u2.png')
    
    # dimensions of the hero for collision detection
    hero_width = hero.rect.width
    hero_height = 3

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

    # add the hero the the right layer, it can be changed using 0-9 keys
    sprite_layers[2].add_sprite(hero)
           
    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    speed=5
    health=100
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT,1000)
    mr=ml=md=mu=0
    #create portal to change map
    portal1 = pygame.Rect(19*20,42*20,180,20)

    #create the spooky guy
    vil=person.create_villager(file_name)
    sprite_layers[1].add_sprite(vil[0]['sprte'])
    
    # mainloop
    while running:
        dt = clock.tick(40)
        #update camera position as per hero's position
        if ( hero.rect.centery >=570):
            renderer.set_camera_position(475, 570)
            c_pos=(475,570)
        elif (hero.rect.centery <=380):
            renderer.set_camera_position(475, 380)
            c_pos=(475,380)
        else:
            renderer.set_camera_position(475,hero.rect.centery )
            c_pos=(475,hero.rect.centery)


                    
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                print("fps: ", clock.get_fps())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                x=event.key
                if (vil!=None):
                    talk_result=talk.iftalk(0,x,vil,0,hero_pos_x,hero_pos_y,file_name)
                else:
                    talk_result=None


                if(talk_result[0]==1):
                    menutext=menu.create_menu_vil(0,file_name,talk_result[2])        
                    dialog_show=0                                                    
                    
                    txtim=person.create_text_img('./images/textbox.png',menutext,dialog_show)    
                    menu_ui=person.create_menu_bg(c_pos[0],c_pos[1]-768/2,txtim)    
                    

                    sprite_layers[2].add_sprite(menu_ui)
                    shifty1.render_update(renderer,sprite_layers,screen)

                    #the loop for showing text box (again and again) till dialogues not completed
                    while(dialog_show<len(menutext)):
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                x=event.key
                                if(x==pygame.K_SPACE):
                                    sprite_layers[2].remove_sprite(menu_ui)             
                                    dialog_show +=1                                     
                                    if dialog_show==len(menutext):                      
                                        break
                                    
                                    txtim=person.create_text_img('./images/textbox.png',menutext, \
                                                                 dialog_show)
                                    menu_ui=person.create_menu_bg(c_pos[0],c_pos[1]-768/2,\
                                                  txtim)                                
                                    
                                    sprite_layers[2].add_sprite(menu_ui)
                                    sv['spook']=1
                                    sv['talk_vil'][file_name][0]=1
                                    sv['talk_vil']['./maps/village2_inside.tmx'][2]=1
                                    pk.dump(sv,open("./save.p","wb"))

                        
                        shifty1.render_update(renderer,sprite_layers,screen)


                    menu.exit_menu(x)##an infite loop till 'x' is pressed
                    sprite_layers[2].remove_sprite(menu_ui)
                

        # find directions
       
        mov = movements1.hero_move(mr,ml,md,mu,hero_pos_x,hero_pos_y,hero,speed,sprite_layers[3])
        mr = mov[0]
        ml = mov[1]
        md = mov[2]
        mu = mov[3]
        hero_pos_x = mov[4]
        hero_pos_y = mov[5]

        sv=pk.load(open("./save.p","rb"))
        if(portal1.collidepoint(hero.rect.midbottom) and sv['talk_vil'][file_name][0]==1):
            portal=True
            running = False
            mixer.music.stop();
        
            
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
        t=random.randint(0,1000)
        #based on random numnber play bats sound
        if(t<5):
            mixer.music.stop()
            sound.play(0)
            mixer.music.play(-1);
                          
            
        # changes to switch screen to game over
        pygame.display.flip()

    if portal==True:
        #change the map
        shifty1.demo_pygame('./maps/village2_inside.tmx',2)

#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()


