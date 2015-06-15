import person , movements1

import sys
import os
import time
import math
import tiledtmxloader
from pygame import mixer
import pygame
try:
    import _path
except:
    pass
import palace

#  -----------------------------------------------------------------------------

def main():
    
        demo_pygame('./maps/palace.tmx')

#  -----------------------------------------------------------------------------

def demo_pygame(file_name):
    """
    Example showing how to use the paralax scrolling feature.
    """
    
    HERO_HEALTH = 100
    file = './sounds/lava_back.ogg'
    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)
    # loading the sound files in different sound formats of mixer and main background sound in mixer stream 
    mixer.init()
    sound_fall = mixer.Sound('./sounds/scream2.ogg')
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
    hero_pos_x = 32*32  #32*32
    hero_pos_y = 39*32 + 20  #19*32
    hero = person.create_person(hero_pos_x, hero_pos_y ,'./images/hero_u2.png')
    hero_width = hero.rect.width
    hero_height = 5
    # palcing chest sprite as the key
    chest = person.create_person(29*32+16,17*32,'./images/closed_chest.png')
    
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
    sprite_layers[2].add_sprite(chest)
   
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    speed = 2.75
    mr=ml=md=mu=0
    lava_list = []
    # setting up different direction to check for in 4 tile section of map 
    """
    In the 4 tiles to be walkable each tile among them is connected to 2 other 4 tile sections so if hero 
    is on that tile only them the other 2 4 tile section will be isible as lava or not lava(walkable or not walkable )
    stored in different dirx and diry for all 4 tiles in a 4 tile section
    """
    dirx = [[0 for x in range(2)] for x in range(4)]
    diry = [[0 for x in range(2)] for x in range(4)]
    dirx[0][0] = -1 
    dirx[0][1] =  0 
    dirx[1][0] = 0
    dirx[1][1] = 1
    dirx[2][0] = -1
    dirx[2][1] = 0
    dirx[3][0] = 1
    dirx[3][1] = 0
    diry[0][0] = 0
    diry[0][1] = -1
    diry[1][0] = -1
    diry[1][1] = 0
    diry[2][0] = 0
    diry[2][1] = 1
    diry[3][0] = 0
    diry[3][1] = 1
    # string the walable path in the matrix by loading the tile data from 2nd layer of map
    matrix = [[None for x in range(10)] for x in range(10)]
    
    for i in range(10 ):
        for j in range(10):
            if sprite_layers[1].content2D[(10+i)*2][(10+j)*2] is None:
                matrix[i][j] = create_lava(10+j,10+i)#opp in case of content2D
                #sprite_layers[2].add_sprite(matrix[i][j])
                lava_list.append(matrix[i][j].rect)
                #sys.stdout.write('1 ')
            #else: sys.stdout.write('0 ')
        #print " "
    # for storing the current visible lava and editing them dynamically along with the motion of the hero
    active_list = []
    # stores the last position of the hero 
    old = (-1,-1)
    flag =0
    # 3 portals for chest and 2 gates 
    portal1 = pygame.Rect(28*32,15*32,96,64)#key place
    portal2 = pygame.Rect(21*32,10*32,96,96)#left door
    portal3 = pygame.Rect(35*32,10*32,96,96)#right door
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
        #print pygame.key.get_pressed()[pygame.K_SPACE]       
        mov = movements1.hero_move(mr,ml,md,mu,hero_pos_x,hero_pos_y,hero,speed,sprite_layers[4])
        mr = mov[0]
        ml = mov[1]
        md = mov[2]
        mu = mov[3]
        hero_pos_x = mov[4]
        hero_pos_y = mov[5]
        if(hero_pos_y < 20 *32):
            mixer.music.stop()
            # stopping the fast music after crossing the path of lava
        if(flag == 0 and portal1.collidepoint(hero.rect.midtop)):
            #print "collision deteected"
            # for checkign with the key taken from the chest
            
            if(pygame.key.get_pressed()[pygame.K_SPACE]==1):
                flag = 1
                chest.image = pygame.image.load('./images/open_chest.png')
                key_riddle=person.create_person(hero.rect.centerx,hero.rect.centery+200,'./images/lava_riddle.png')
                sprite_layers[3].add_sprite(key_riddle)
                #ring_take.rect.topleft=(1,1)
                for sprite_layer in sprite_layers:
                    if sprite_layer.is_object_group:
                        # we dont draw the object group layers
                        # you should filter them out if not needed
                        continue
                    else:
                        renderer.render_layer(screen, sprite_layer)

                pygame.display.flip()
                i=0
                while(i!=1):        ##Infinite loop until menu is to be removed
                    for event in pygame.event.get():
                        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                            i=1
                    continue
                sprite_layers[3].remove_sprite(key_riddle)
                #print "detected key here"
                # code for taking key and riddle
        elif(flag == 1 and portal2.collidepoint(hero.rect.midtop)):
            # for the wronng decision start from the beginning
            if(pygame.key.get_pressed()[pygame.K_SPACE]==1):
                hero_pos_x = 32 * 32
                hero_pos_y = 40 * 32
                mixer.music.play()
        elif(flag == 1 and portal3.collidepoint(hero.rect.midtop)):
            #if right path chosesn changing to next map
            if(pygame.key.get_pressed()[pygame.K_SPACE]==1):
                #condition on successful transition
                #print "detected right path"
                #music.mixer.stop()
                portal=True
                running=False
        # checking the midbottom of hero(foot ) if found in any rectangle of the tiles in activelist then dead 
        for i in range(len(active_list)):
            if(active_list[i].rect.collidepoint(hero.rect.midbottom)):
                hero_pos_x = 32 * 32 
                hero_pos_y = 40 * 32
                mixer.music.stop()
                sound_fall.play()
                time.sleep(2)
                mixer.music.play()
        #updating the activelist with the position of the hero 
        x_tile = (int)(hero_pos_x // 32)
        y_tile = (int)(hero_pos_y // 32)
        new = (x_tile, y_tile)
        # storing the tile numeber of the hero 
        if(old != new):
        # if the hero has changed its tile only then this check will be called for fast processing 
            if(len(active_list)>0):
            # emptying out the last active list 
                while( len(active_list) > 0):
                    sprite_layers[2].remove_sprite(active_list[0])
                    active_list.pop(0)
                # getting tile number in 4 tile section to check for which direction to select from above defined direction dataset
            n = get_tile_no(x_tile, y_tile)
            
            for i in range(2):
                # to check for the new tilesection are they in matrix laoded above 
                x = ((x_tile + dirx[n][i])//2 - 10)
                y = ((y_tile + diry[n][i])//2 - 10)
                if( 0 <= x <10 and 0 <= y < 10 ):
                    if(matrix[y][x] is not None and not sprite_layers[2].contains_sprite(matrix[y][x])):
                        # appending the kill tiles in the active list 
                        sprite_layers[2].add_sprite(matrix[y][x])
                        active_list.append(matrix[y][x])

        
        #renderer.set_camera_position(hero.rect.centerx, hero.rect.centery)
        # moving the camera positon acc to the hero location in the map
        cam_pos_x = hero.rect.centerx
        cam_pos_y = hero.rect.centery
        if hero.rect.centerx <= 520 :
            cam_pos_x = 520
        elif hero.rect.centerx >=((42*32)-530):
            cam_pos_x = ((42*32)-530)
        if hero.rect.centery >= 44*32-400:
            cam_pos_y = 44*32-400
        elif hero.rect.centery <=408:
            cam_pos_y = 408
        renderer.set_camera_position(cam_pos_x,cam_pos_y)

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

    if portal==True:
        palace.main()

#  -----------------------------------------------------------------------------
def create_lava(tile_64_x, tile_64_y):
    # creating lava sprite at given tile position of size = to 4 tiles 
    image = pygame.image.load('./images/lava.png')
    rect = image.get_rect()
    rect.midbottom = ((tile_64_x * 64)+32, (tile_64_y * 64) +64)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)

def get_tile_no(x,y):
    # getting the tile number in 4 section tile set 
    if x%2==0 and y%2 ==0:
        return 0;
    elif x%2 == 1 and y%2 == 1 :
        return 3;
    elif x%2 == 0 and y%2 == 1:
        return 2;
    else:
        return 1;

#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()


