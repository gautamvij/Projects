


import sys
import os
import math
import pygame
from pygame import mixer
import cPickle as pk
try:
    import _path
except:
    pass
import random

import tiledtmxloader		# tiled map editor library
# files loading below
import person
import shifty1

#  -----------------------------------------------------------------------------

def main():
   
    demo_pygame('./maps/zish.tmx')   # main function for running the same code for test runs

#  -----------------------------------------------------------------------------
speed_x = 0.0
speed_y = 0.0 # Different speeds calibration in horizonatal and vertical direction 
def demo_pygame(file_name):
  
    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)
    pygame.display.set_caption("tiledtmxloader - " + file_name + \
                                                        " - keys: arrows, 0-9")
    screen_width = min(1024, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    mixer.init()
	# loading the sound files in different sound formats of mixer and main background sound in mixer stream 
    fish_catch = mixer.Sound('./sounds/zish_catch.ogg')
    file = './sounds/zish_back.ogg'
    mixer.music.load(file)
    mixer.music.play(-1)
    
    
    # load the images using pygame
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    # prepare map rendering
    assert world_map.orientation == "orthogonal"

    # renderer
    renderer = tiledtmxloader.helperspygame.RendererPygame()

    # create hero sprite
    # use floats for hero position
    hero_pos_x = 1048/2
    hero_pos_y = 768/2 + 6 *32
    hero = create_hero(hero_pos_x, hero_pos_y)
    hero_width = 31 
    hero_height = 5
    
    # creating random fish
    fishes = []
    fish_count =10
    fish_loc = []
    for i in range(fish_count):
        fishes.append(create_fish())
    #Storing the fishes in an array for further addition 
    for i in range(fish_count):
        fish_loc.append(fishes[i].rect)
    # for different directions different images to be set on the moving fish.
    im1 = pygame.image.load('./images/ztile1.png')
    im2 = pygame.image.load('./images/ztile2.png')
    
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

    # adding the hero  and the firshes to the the right layer
    sprite_layers[1].add_sprite(hero)
    flag = [0 for x in range(fish_count)]
	#small fishes added in bottom of screen showing the count of remaining fishes left to complete the game
    small_fish = []
    for i in range(fish_count):
        small_fish.append(person.create_person(64 +i*32,22*32,'./images/ztile_small.png'))
        
    for i in range(len(flag)):
        sprite_layers[1].add_sprite(fishes[i])
    for i in range(len(flag)):
        sprite_layers[1].add_sprite(small_fish[i])

    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    speed_x = 0.0
    speed_y = 0.0
    #initializing random values for the direction of 10 fishes 
    for i in range(len(flag)):
        flag[i]=random.randint(1,2)
    # mainloop
    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT, 10000)
    
    while running:
        dt = clock.tick(50) # value set to work same with different processors 

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
			# showing the fps
            elif event.type == pygame.USEREVENT:
                print("fps: ", clock.get_fps())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                    
        # deciding fish speed at each instant along with the need to change direction with another function
        for i in range(len(flag)):
            f_temp_x = fishes[i].rect.centerx
            f_temp_y = fishes[i].rect.centery
            if(flag[i]==0):
                flag[i] = random.randint(1,2)
            if(flag[i]==1):
                f_temp_x+= random.randint(6,11)
            else:
                f_temp_x-= random.randint(6,11)
            f_temp_x, f_temp_y, flag[i] = dist_bound_x(f_temp_x,f_temp_y,flag[i])  # returns new position with direction flag
            if(flag[i]==1):
                fishes[i].image = im2
            else:
                fishes[i].image = im1
			# assiging the new final positon of every fish in every tick
            fishes[i].rect.centerx = f_temp_x
            fishes[i].rect.centery = f_temp_y
            fish_loc[i] = fishes[i].rect
        
        # find directions
        direction_x = pygame.key.get_pressed()[pygame.K_RIGHT] - pygame.key.get_pressed()[pygame.K_LEFT]
        direction_y = pygame.key.get_pressed()[pygame.K_DOWN] -  pygame.key.get_pressed()[pygame.K_UP]
        

        # make sure the hero moves with same speed in all directions (diagonal!)
        speed_x+= direction_x*0.0056
        speed_y+= direction_y*0.0056
        dir_len = math.hypot(direction_x, direction_y)
        dir_len = dir_len if dir_len else 1.0
        if(math.fabs(speed_x)>0.74):
            if(speed_x>0):
                speed_x =  0.7
            else:
                speed_x = - 0.7
        # update position
        step_x = speed_x * 36  / dir_len
        step_y = speed_y * 36  / dir_len
        step_x, step_y = check_collision(hero_pos_x, hero_pos_y, step_x, step_y, hero_width, hero_height, sprite_layers[3]) # to check collision from boundary for the hook
        hero_pos_x += step_x
        hero_pos_y += step_y
        if(step_x == 0):
            speed_x =0.0
        if(step_y == 0):
            speed_y =0.0
        hero.rect.center = (hero_pos_x, hero_pos_y)
		# checking for the contact with the hook midtop for catching fish
        flag = fish_collision(fish_loc, hero.rect, flag)

        i=0
		# always check for any value in flag to be 0 if yes to remove that fish 
        while(i<len(flag)):
            #print i
            if(flag[i] == 0):
                fish_catch.play()
                sprite_layers[1].remove_sprite(fishes[i]) # removing big fish from big screen
                flag.pop(i)
                sprite_layers[1].remove_sprite(small_fish[len(flag)]) # removing small fish from big screen 
                fishes.pop(i)
                fish_loc.pop(i)
                continue
            i+=1
        #print("cleared here")
		# synchronizing fishes sound along with their catch.
        if(len(flag)==0):
            mixer.music.stop()
            sv=pk.load(open("./save.p","rb"))
            sv['f_vil']=1
            sv['talk_vil']['./maps/village2_out1.tmx'][0]=1
            pk.dump(sv,open("./save.p","wb")) # saving the results in the file to check for the next time in the story where to go or not to go
            running=False
        # adjust camera according to the hero's position, follow him
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

	# calling the other map after completion of catching all the fishes 
    shifty1.demo_pygame('./maps/village2_out1.tmx',2)

#  -----------------------------------------------------------------------------
def fish_collision(fishes_loc, hero,flag):
	
    for i in range(len(flag)):
        #return the true if there is a collision with any fish and sets that falg to 0
	if(fishes_loc[i].collidepoint(hero.midtop)==1):
            flag[i]=0
    return flag
    
def create_fish():
	# randomly deciding the fish location in a decided field
    fish_pos_x = random.randint(60,900)
    fish_pos_y = random.randint(60, 450)
    image = pygame.image.load("./images/ztile1.png")
    rect = image.get_rect()
    rect.center = (fish_pos_x, fish_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)

def create_hero(start_pos_x, start_pos_y):
    """
    Creates the hero sprite.
    """
    image = pygame.image.load("./images/zow1.png")
    rect = image.get_rect()
    rect.center = (start_pos_x, start_pos_y)
	# adding the two parts of tile image and its rect to the sprite
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect) 

#  -----------------------------------------------------------------------------

def check_collision(hero_pos_x, hero_pos_y, step_x, step_y, \
                                    hero_width, hero_height, coll_layer):
    # create hero rect
    hero_rect = pygame.Rect(0, 0, hero_width, hero_height)
    #print hero_rect.height
    #print hero_rect.width
    hero_rect.center = (hero_pos_x, hero_pos_y)

    # find the tile location of the hero
    tile_x = int((hero_pos_x) // coll_layer.tilewidth)
    tile_y = int((hero_pos_y) // coll_layer.tileheight)

    # find the tiles around the hero and extract their rects for collision
    tile_rects = []
    for diry in (-2, -1, 0 , 1, 2):
        for dirx in ( -2, -1, 0, 1, 2):
            if coll_layer.content2D[tile_y + diry][tile_x + dirx] is not None:
                tile_rects.append(coll_layer.content2D[tile_y + diry][tile_x + dirx].rect)
    #print hero_rect.center
    # save the original steps and return them if not canceled
    res_step_x = step_x
    res_step_y = step_y

    # x direction, floor or ceil depending on the sign of the step
    step_x = special_round(step_x)

    # detect a collision and dont move in x direction if colliding
    if hero_rect.move(step_x, 0).collidelist(tile_rects) > -1:
        res_step_x = 0

		# y direction, floor or ceil depending on the sign of the step
    step_y = special_round(step_y)

    # detect a collision and dont move in y direction if colliding
    if hero_rect.move(0, step_y).collidelist(tile_rects) > -1:
        res_step_y = 0
        
    #return the step the hero should do
    return res_step_x, res_step_y


def special_round(value):
    """
    For negative numbers it returns the value floored,
    for positive numbers it returns the value ceiled.
    """

    if value < 0:
        return math.floor(value)
    return math.ceil(value)

#  -----------------------------------------------------------------------------

def dist_bound_x(x, y, flag):
    
    if((1024 - x)<45 or x<45):
        x = random.randint(60,900)
        y = random.randint(60,450)
        flag = random.randint(1,2)
        return x,y, flag
    else: return x,y,flag

if __name__ == '__main__':
    main()


