import sys
import os
import math
import random
import cPickle as pk
import pygame
from pygame import mixer
import tiledtmxloader

#import required modules
import menu
import mountain_top
import person ,climb

try:
    import _path
except:
    pass

def main():
    #pass the mapname 
    demo_pygame('./maps/mountainclimbing.tmx',0)

def demo_pygame(file_name,frm):
    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    #for background music and special sound effects
    mixer.init()
    sound1 = mixer.Sound('./sounds/ouch.ogg')
    sound2=mixer.Sound('./sounds/stone.ogg')

    file = './sounds/Rock_Slide.ogg'
    m = mixer.music.load(file)
    #(-1) argument plays it infinitely unless stopped explicitly
    mixer.music.play(-1);
    
    #set up a screen
    screen_width = min(704, world_map.pixel_width)
    screen_height = min(800, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load the images using pygame
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    # prepare map rendering
    assert world_map.orientation == "orthogonal"

    # renderer
    renderer = tiledtmxloader.helperspygame.RendererPygame()

    # create hero sprite
    hero_pos_x = screen_width/2
    hero_pos_y = 6300
    #create hero on specified co-ordinates and with specified image
    hero = person.create_person(hero_pos_x, hero_pos_y ,'./images/up.png')

    #portal to detect change of map
    portal2 = pygame.Rect(0,1*32,21*32,60)
    
    # create stones sprite
    stone_width =3
    stone1_height=3
    stone2_height=4
    stone3_height=5
    stone1=[]
    stone2=[]
    stone3=[]
    
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

    # add the hero to the the right layer
    sprite_layers[1].add_sprite(hero)
    
    # add stone positions
    stone1_pos_x=[]
    stone1_pos_y=[]
    stone2_pos_x=[]
    stone2_pos_y=[]
    stone3_pos_x=[]
    stone3_pos_y=[]
    
    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    speed_x = 4
    speed_y= 6
    last=0
    #load the saved game variables based on game progress
    sv=pk.load(open("./save.p","rb"))
    health=sv['hp']
    hp=sv['hp']
    hp_max=sv['max_hp']
    c_pos=[cam_world_pos_x, cam_world_pos_y]    
    interf_toggle=0
    interface=menu.create_interface(renderer,sprite_layers,screen,c_pos) 
    hp_sprite=person.create_person(c_pos[0],c_pos[1],'./images/hp_bar.png')
    l_g=menu.create_l_g(renderer,sprite_layers,screen,c_pos)
    [hp_sprite,hp]=menu.create_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos)
    xp_sprite=person.create_person(c_pos[0],c_pos[1],'./images/exp_bar.png')
    xp_sprite=menu.create_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos)

    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT,1000)
    cl = 0
    # mainloop
    while running:
        dt = clock.tick(40)
        sv=pk.load(open("./save.p","rb"))
                    
        # event handling
        for event in pygame.event.get():
            #update the health,experience and armour
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
            

        #based on collision with environment decide number of steps allowed
        mov = climb.hero_climb(cl,hero_pos_x,hero_pos_y,hero,speed_x,speed_y,sprite_layers[3])
        cl = mov[0]
        hero_pos_x = mov[1]
        hero_pos_y = mov[2]
        
        #check collision with portal to change map
        if(pygame.Rect.colliderect(portal2,hero.rect)):
            portal=True
            #stop the background music for this map
            mixer.music.stop()
            running =False

            

        # adjust camera according to the hero's position, follow him
        if ( hero.rect.centery >=6000):
            renderer.set_camera_position(350, 6000)
            c_pos=(350,6000)
        elif (hero.rect.centery <=400):
            renderer.set_camera_position(350, 400)
            c_pos=(350,400)
        else:
            renderer.set_camera_position(350,hero.rect.centery )
            c_pos=(350,hero.rect.centery)

        #position health bar, experience bar and armour
        interface.rect.topleft=(c_pos[0]-352,c_pos[1]-384)
        hp_sprite.rect.topleft=(c_pos[0]-240,c_pos[1]-382)
        xp_sprite.rect.topleft=(c_pos[0]-240,c_pos[1]-345)
        l_g.rect.topleft=(c_pos[0]-348,c_pos[1]-381)

        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0, 0, 0))

        # render the map
        for sprite_layer in sprite_layers:
            if sprite_layer.is_object_group:
                continue
            else:
                renderer.render_layer(screen, sprite_layer)

        time=(pygame.time.get_ticks() / 500)
        #to decide interval when to drop stones
        if time > last and len(stone1)+len(stone2)+len(stone3) <30:
            last=time
            hero_temp_x = hero.rect.centerx
            #decide x co-ordinate of stone randomly
            r=random.randint(0,100)
            if( r < 25):
                left_limit=hero_temp_x - 10
                right_limit = hero_temp_x +10
            elif ( r < 90) :
                left_limit = hero_temp_x - 200
                right_limit = hero_temp_x +200 
                if(left_limit<40): 
                    left_limit = 40
                    right_limit = 400
            
                if(right_limit >640):
                    left_limit = 300
                    right_limit = 660
            else :
                left_limit=10
                right_limit=690

            #to decide randomly the type of stone
            t=random.randint(0,math.floor(hero_pos_y))
            if t < 2000:
                t=3
            elif t < 4000:
                t=2
            else :
                t=1
            permission = random.randint(left_limit,right_limit);
            if(permission<50):
                permission = 55
            elif (permission > 650):
                permission = 645

            #append initial stone locations  and create stone sprites   
            if( t==1):             
                stone1_pos_x.append(permission)
                stone1_pos_y.append(max(hero_pos_y -800,50))
                stone1.append(create_stone(stone1_pos_x[len(stone1)],stone1_pos_y[len(stone1)],1))
                sprite_layers[1].add_sprite(stone1[len(stone1)-1])
            elif t==2 :
                stone2_pos_x.append(permission)
                stone2_pos_y.append(max(hero_pos_y -800,50))
                stone2.append(create_stone(stone2_pos_x[len(stone2)],stone2_pos_y[len(stone2)],2))
                sprite_layers[1].add_sprite(stone2[len(stone2)-1])
            else :
                stone3_pos_x.append(permission)
                stone3_pos_y.append(max(hero_pos_y -800,50))
                stone3.append(create_stone(stone3_pos_x[len(stone3)],stone3_pos_y[len(stone3)],3))
                sprite_layers[1].add_sprite(stone3[len(stone3)-1])
                
        n=0
        while n < len(stone1):
            #moving the stones of type1
            step_x, step_y = climb.check_collision(stone1_pos_x[n], stone1_pos_y[n], 0,8 *(6400-hero_pos_y) //6400 +10, stone_width, stone1_height, sprite_layers[3])
            stone1_pos_y[n] += step_y
            stone1[n].rect.midbottom = (stone1_pos_x[n], stone1_pos_y[n])
            #if stone is out of visible region remove stone sprite
            if (stone1_pos_y[n] >=hero_pos_y +400 or stone1_pos_y[n]>= 6300) :
                sprite_layers[1].remove_sprite(stone1[n])
                stone1.pop(n)
                stone1_pos_y.pop(n)
                stone1_pos_x.pop(n)
                #stop background music and play sound of stone reaching bottom of sea
                mixer.music.stop()
                sound2.play(0)
                #play background music again
                mixer.music.play(-1);
                continue
            else:
                n=n+1
        #to check players' collision with stone type1
        n=hero.rect.collidelist(stone1)
        if  n!= -1:
            #remove stone sprite
            sprite_layers[1].remove_sprite(stone1[n])
            stone1.pop(n)
            stone1_pos_y.pop(n)
            stone1_pos_x.pop(n)
            #decrease the health
            health=health-3
            sv['hp']=health
            pk.dump(sv,open("./save.p","wb"))
            mixer.music.stop()
            #play the hurt sound
            sound1.play(0)
            mixer.music.play(-1)

        if health <=0:
            #go back to initial position
            hero_pos_x=screen_width/2
            hero_pos_y=6300
            sv['hp']=sv['max_hp']
            health=sv['hp']
            
        n=0
        #similarly for stones of type2
        while n < len(stone2):
            step_x, step_y = climb.check_collision(stone2_pos_x[n], stone2_pos_y[n], 0,8 *(6400-hero_pos_y) //6400 + 10, stone_width, stone2_height, sprite_layers[3])
            stone2_pos_y[n] += step_y
            stone2[n].rect.midbottom = (stone2_pos_x[n], stone2_pos_y[n])
            if (stone2_pos_y[n] >=hero_pos_y +400 or stone2_pos_y[n]>= 6300):
                sprite_layers[1].remove_sprite(stone2[n])
                stone2.pop(n)
                stone2_pos_y.pop(n)
                stone2_pos_x.pop(n)
                mixer.music.stop()
                sound2.play(0)
                mixer.music.play(-1);
                continue
            else:
                n=n+1
        n=hero.rect.collidelist(stone2)
        if  n!= -1:
            sprite_layers[1].remove_sprite(stone2[n])
            stone2.pop(n)
            stone2_pos_y.pop(n)
            stone2_pos_x.pop(n)
            health=health-6
            sv['hp']=health
            pk.dump(sv,open("./save.p","wb"))
            mixer.music.stop()
            sound1.play(0)
            mixer.music.play(-1);
        if health <=0 : # changes to switch screen to game over
            hero_pos_x=screen_width/2
            hero_pos_y=6300
            sv['hp']=sv['max_hp']
            health=sv['hp']
            
            
        n=0
        #similarly for stone of type3
        while n < len(stone3):
            step_x, step_y = climb.check_collision(stone3_pos_x[n], stone3_pos_y[n], 0,8 *(6400-hero_pos_y) //6400  +10, stone_width, stone3_height, sprite_layers[3])
            stone3_pos_y[n] += step_y
            stone3[n].rect.midbottom = (stone3_pos_x[n], stone3_pos_y[n])
            if (stone3_pos_y[n] >=hero_pos_y +400  or stone3_pos_y[n]>= 6300):
                sprite_layers[1].remove_sprite(stone3[n])
                stone3.pop(n)
                stone3_pos_y.pop(n)
                stone3_pos_x.pop(n)
                mixer.music.stop()
                sound2.play(0)
                mixer.music.play(-1);
                continue
            else:
                n=n+1
        n=hero.rect.collidelist(stone3)
        if  n!= -1:
            sprite_layers[1].remove_sprite(stone3[n])
            stone3.pop(n)
            stone3_pos_y.pop(n)
            stone3_pos_x.pop(n)
            health=health-10
            sv['hp']=health
            pk.dump(sv,open("./save.p","wb"))
            mixer.music.stop()
            sound1.play(0)
            mixer.music.play(-1);
        if health <=0 : 
            hero_pos_x=screen_width/2
            hero_pos_y=6300# changes to switch screen to game over
            sv['hp']=sv['max_hp']
            health=sv['hp']
            
        pygame.display.flip()

    if portal==True:
        #chnage the map
        mountain_top.main()

#  -----------------------------------------------------------------------------

def create_stone(start_pos_x, start_pos_y,y):
    """
    Creates the stone sprite based on the random stone type decide
    """
    if y==3:
        image=pygame.image.load('./images/stone3.png')
    elif y==2:
        image=pygame.image.load('./images/stone2.png')
    else :
        image=pygame.image.load('./images/stone1.png')
    rect = image.get_rect()
    rect.midbottom = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)


#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()


