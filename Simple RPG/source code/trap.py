import time
from pygame import mixer
import sys
import os
import math
import random
import cPickle as pk
import pygame

import person, movements1
import shifty1

try:
    import _path
except:
    pass
import tiledtmxloader

#  -----------------------------------------------------------------------------

def main():
   
    demo_pygame('./maps/safe1.tmx',0)

#  -----------------------------------------------------------------------------

def demo_pygame(file_name,frm):

    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    pygame.display.set_caption("tiledtmxloader - " + file_name + \
                                                        " - keys: arrows, 0-9")
    screen_width = min(1024, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))
	# loading the sound files in different sound formats of mixer and main background sound in mixer stream 
    mixer.init()
    sound_guard_watch = mixer.Sound('./sounds/pain.ogg')
    sound_hole_fall = mixer.Sound('./sounds/scream2.ogg')
    file = './sounds/zrap_back.ogg'
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
    hero_pos_x = 3 * 32
    hero_pos_y = 21 * 32
    hero = person.create_person(hero_pos_x, hero_pos_y,'./images/hero_u2.png')
    hero_width = hero.rect.width
    hero_height = 5
    # laoding the scroll 
    map_trap = person.create_person(8*32+16,3*32 +30,'./images/map_trap.png')
	#creating the 3 guards 
    guard = []
    guard_pos_x = random.randint(10*32, 18*32)
    guard_pos_y = 18*32
    guard.append(create_guard(guard_pos_x,guard_pos_y))
    guard.append(create_guard(random.randint(22*32,31*32),15*32))
    guard.append(create_guard(random.randint(22*32,31*32),6*32))
	# field of view of different guards 
	# collision with this tile is death for hero
    danger = []
	# kill flag for last trap tile of pins from ground
    showkillbill=0
	# creating the pintrap but not adding to the sprite 
    killbill = create_kill(18*32, 8*32 + 48)
    hole = create_hole(18*32, 2*32)
    danger_count =140 + 1 # for kill tile
	# intersect tiles for nullyfying guard filed of view near stones 
    intersect1 = []
    for i in range(5):
        for j in range(5):
            intersect1.append(create_dang(13 *32 + j*16 + 16, (21 * 32 -16) + i*16 ))
    intersect2 = []
    for i in range(5):
        for j in range(5):
            intersect2.append(create_dang(13 *32 + j*16 + 48, (21 * 32 -16) + i*16 ))
   
    for i in range(danger_count-1):
        danger.append(create_dang(100,100))
    

    # dimensions of the hero for collision detection

    # cam_offset is for scrolling
    cam_world_pos_x = 512
    cam_world_pos_y = 768 / 2 

    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height)

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    # filter layers
    sprite_layers = [layer for layer in sprite_layers if not layer.is_object_group]

    # adding the hero and the danger and the traps to the the right layer
    
    sprite_layers[4].add_sprite(hero)
    sprite_layers[4].add_sprite(guard[0])
    sprite_layers[4].add_sprite(guard[1])
    sprite_layers[4].add_sprite(guard[2])
    sprite_layers[2].add_sprite(map_trap)
    for i in range(56,len(danger)):
        sprite_layers[1].add_sprite(danger[i])
    sprite_layers[3].add_sprite(hole)
	# set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # variables for the main loop
    cross_guards =0
    clock = pygame.time.Clock()
    running = True
    speed = 3.6505
    flag1 = random.randint(1,2)
    flag2 = random.randint(1,2)
    flag3 = random.randint(1,2)
    count = -1
    mr=ml=md=mu=0
    kill_active =0
    portal1 = pygame.Rect(7*32,2*32,96,64)
    
    # mainloop
    while running:
        """
		for 3 guards flag1 flag2 flag3 for their directions in horizontal direction 
	"""
        dt = clock.tick(35)
        # for guard1 movement here
        if(flag1 == 1):
            if(guard[0].rect.centerx < 10 * 32 ): flag1 = 2
            else : guard[0].rect.centerx-= 2
        elif (flag1 == 2):
            if(guard[0].rect.centerx > 18 * 32 ): flag1 = 1
            else : guard[0].rect.centerx+=2
        index=0 
		#updating the danger tiles for the first guard 
        if(flag1==1):
            for i in range(10,0,-1):
                for j in range(i):
                    danger[index].rect.center = ((guard[0].rect.centerx - j * 16),(guard[0].rect.centery + (10-i) * 16) )
                    index+= 1
        elif(flag1==2):
            for i in range(10,0,-1):
                for j in range(i):
                    danger[index].rect.center = ((guard[0].rect.centerx + j * 16),(guard[0].rect.centery + (10-i) * 16) )
                    index+=  1
					
        # for guard 2  movement here
        if(flag2 == 1):
            if(guard[1].rect.centerx < 22 * 32 ): flag2 = 2
            else : guard[1].rect.centerx-= 2
        elif (flag2 == 2):
            if(guard[1].rect.centerx > 31 * 32 ): flag2 = 1
            else : guard[1].rect.centerx+=2

        #updating the danger tiles for the first guard 
        if(flag2==1):
            for i in range(7,0,-1):
                for j in range(i):
                  danger[index].rect.center = ((guard[1].rect.centerx - j *16 ), (guard[1].rect.centery + (7 - i) * 16))
                  #danger[index].rect.center = ((guard[1].rect.centerx - j *16 ), (guard[1].rect.centery - (i * 16)))
                  index+=1
            for i in range(0,7):
                for j in range(i):
                  #danger[index].rect.center = ((guard[1].rect.centerx - j *16 ), (guard[1].rect.centery + (7 - i) * 16))
                  danger[index].rect.center = ((guard[1].rect.centerx - j *16 ), (guard[1].rect.centery - (7-i)  * 16))
                  index+=1
                  
        if(flag2==2):
            for i in range(7,0,-1):
                for j in range(i):
                  danger[index].rect.center = ((guard[1].rect.centerx + j *16 ), (guard[1].rect.centery + (7 - i) * 16))
                  index+=1
            for i in range(0,7):
                for j in range(i):
                  danger[index].rect.center = ((guard[1].rect.centerx + j *16 ), (guard[1].rect.centery - (7-i)  * 16))
                  index+=1          
       
        # for guard 3 movement here
        if(flag3 == 1):
            if(guard[2].rect.centerx < 22 * 32 ): flag3 = 2
            else : guard[2].rect.centerx-= 2
        elif (flag3 == 2):
            if(guard[2].rect.centerx > 31 * 32 ): flag3 = 1
            else : guard[2].rect.centerx+=2
        
        #updating the danger tiles for the first guard 
        if(flag3==1):
            for i in range(6,0,-1):
                for j in range(i):
                    danger[index].rect.center = ((guard[2].rect.centerx - j *16 ), (guard[2].rect.centery + (6 - i) * 16))
                    index+=1
            for i in range(0,6):
                for j in range(i):
                    danger[index].rect.center = ((guard[2].rect.centerx - j *16 ), (guard[2].rect.centery - (6-i)  * 16))
                    index+=1
                  
        if(flag3==2):
            for i in range(6,0,-1):
                for j in range(i):
                    danger[index].rect.center = ((guard[2].rect.centerx + j *16 ), (guard[2].rect.centery + (6 - i) * 16))
                    index+=1
            for i in range(0,6):
                for j in range(i):
                    danger[index].rect.center = ((guard[2].rect.centerx + j *16 ), (guard[2].rect.centery - (6-i)  * 16))
                    index+=1

        #taking map and map change condition here with the scroll 
        if(portal1.collidepoint(hero.rect.midtop) and pygame.key.get_pressed()[pygame.K_SPACE]==1):
            sprite_layers[2].remove_sprite(map_trap)
            mixer.music.stop()
            sv=pk.load(open("./save.p","rb"))
            #saving the data in the file 
            sv['pirate_map']=1
            sv['pirate_vil']=1
            sv['talk_vil']['./maps/ship.tmx'][0]=1
            pk.dump(sv,open("./save.p","wb"))
            portal=True
			# now change map after end of the loop at the end of the loop 
            running=False
			
        # checking collision in red zone

        for i in range(len(danger)):          
            if(pygame.sprite.collide_rect(hero,danger[i])):
                """ 
				to palce the hero to starting position if it the redzone is not in intersect field 
				if false is 0 then the hero is moved to the initial position 
				the intersect case is only for the first guard 
                """
                false =0
                if (flag1==1):
                    for j in range(len(intersect1)):
                        if(pygame.sprite.collide_rect(danger[i],intersect1[j])):
                            false =1
                    if(false == 0):
                        #print hero.rect.center
                        hero_pos_x = 3*32
                        hero_pos_y = 21*32
                        mixer.music.stop()
                        sound_guard_watch.play()
                        time.sleep(1)
                        mixer.music.play()
                        #print hero.rect.center
                        break
                elif (flag1==2):
                    
                    for j in range(len(intersect2)):
                        if(pygame.sprite.collide_rect(danger[i],intersect2[j])):
                            false =1
                    if(false == 0):
                        #print hero.rect.center
                        hero_pos_x = 3*32
                        hero_pos_y = 21*32
                        mixer.music.stop()
                        sound_guard_watch.play()
                        time.sleep(1)
                        mixer.music.play()
                        #print hero.rect.center
                        break

        # after crossing
		#stroing the hole image size for changing it later when hero crossing 
        r1 = hole.rect
        im = hole.image
        r2= im.get_rect()
        w = r2.width
        """
		cross_guards storing the checkpoint of the hero 
		1 after crossing all the guards 
		2 after crossing the hole 
        """
        if(count > 0):
            count+= 1
        if (hero_pos_y < 3*32 ):
            cross_guards = 1;
        
            #print cross_guards
        if(cross_guards ==1 and hero_pos_x < 20 * 32 and hero_pos_y < 3*32):
            r1 = hole.rect
            im = hole.image
            r2= im.get_rect()
            w = r2.width
			# if hole is large to limit hero falls and sent to starting position 
            if(w<60):
                im = pygame.transform.scale(im,(w+2,w+2))
                r = im.get_rect()
                r.center = r1.center
                hole.image = im
                hole.rect = r
            else:
                cross_guards = 0;
                hero_pos_x = 3*32
                hero_pos_y = 21*32
                mixer.music.stop()
                sound_hole_fall.play()
                time.sleep(1)
                im = pygame.transform.scale(im,(12,12))
                r = im.get_rect()
                r.center = r1.center
                hole.image = im
                hole.rect = r
                mixer.music.play()
        # condition that hero has crossed the hole trap count for pin from ground is started 
		#showkillbill is bool value for activating the pin ground trap 
        elif(cross_guards == 1 and hero_pos_x < 19 *32 and hero_pos_y > 3*32):
            cross_guards =2
            count = 1
         
        elif(cross_guards == 2 and not showkillbill == 1):
            showkillbill = 1             
            
        elif (cross_guards == 2 and  hero_pos_y > 16 *32):
            cross_guards = 0
            im = pygame.transform.scale(im,(12,12))
            r = im.get_rect()
            r.center = r1.center
            hole.image = im
            hole.rect = r
		# sendin the hero back to start from position if collsion of midbottom with pin trap 
        if(kill_active==1):
            if(killbill.rect.collidepoint(hero.rect.midbottom)):
                cross_guards = 0;
                hero_pos_x = 3*32
                hero_pos_y = 21*32
                mixer.music.stop()
                sound_guard_watch.play()
                time.sleep(1)
                im = pygame.transform.scale(im,(12,12))
                r = im.get_rect()
                r.center = r1.center
                hole.image = im
                hole.rect = r
                mixer.music.play()
        # timed fluctuation of the pin trap 
        if(showkillbill == 1 and count > 56):
            count = 1
            if(sprite_layers[3].contains_sprite(killbill)):
                sprite_layers[3].remove_sprite(killbill)
                kill_active=0
            else:
                sprite_layers[3].add_sprite(killbill)
                kill_active=1
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                print("fps: ", clock.get_fps())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
         
        # calling the hero_move fucntion from movements1 file for changing the position of the hero 
        mov = movements1.hero_move(mr,ml,md,mu,hero_pos_x,hero_pos_y,hero,speed,sprite_layers[5])
        mr = mov[0]
        ml = mov[1]
        md = mov[2]
        mu = mov[3]
        hero_pos_x = mov[4]
        hero_pos_y = mov[5]
        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0, 0, 0))

        # render the map
        for sprite_layer in sprite_layers:
            if sprite_layer.is_object_group:
                continue
            else:
                renderer.render_layer(screen, sprite_layer)

        pygame.display.flip()


    if portal==True:
        shifty1.demo_pygame('./maps/ship.tmx',1)

#  -----------------------------------------------------------------------------
#creating pingrpund trap 
def create_kill(midbottomx, midbottomy):
    #image = Image.open('kill.png')
    image = pygame.image.load('./images/kill.png')
  
    rect  = image.get_rect()
    
    rect.midbottom = (midbottomx, midbottomy)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)
    
# creating hole trap here 
def create_hole(midbottomx, midbottomy):
    #image = Image.open('kill.png')
    image = pygame.image.load('./images/holl.jpg')
	# small size of hole in the beginning 
    image = pygame.transform.scale(image,(12,12))
    rect  = image.get_rect()
    rect.center = (midbottomx, midbottomy)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)
    
def create_hero(start_pos_x, start_pos_y):
    
    image = pygame.image.load('./images/hero.png')
    #image.fill((255, 0, 0, 200))    
    rect = image.get_rect()
    rect.center = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)


def create_dang(start_pos_x, start_pos_y):
    image = pygame.image.load('./images/danger.png')
    
    #image.fill((255, 0, 0, 200))
    rect = image.get_rect()
    rect.center = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)


def create_guard(start_pos_x, start_pos_y):
    image = pygame.image.load('./images/guard.png')
    #image.fill((255, 0, 0, 200))
    rect = image.get_rect()
    rect.center = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)
#  -----------------------------------------------------------------------------

def check_collision(hero_pos_x, hero_pos_y, step_x, step_y, \
                                    hero_width, hero_height, coll_layer):
    """
    Checks collision of the hero against the world. Its not the best way to
    handle collision detection but for this demo it is good enough.

    :Returns: steps to add to heros current position.
    """
    # create hero rect
    hero_rect = pygame.Rect(0, 0, hero_width, hero_height)
    hero_rect.center = (hero_pos_x, hero_pos_y)

    # find the tile location of the hero
    tile_x = int((hero_pos_x) // coll_layer.tilewidth)
    tile_y = int((hero_pos_y) // coll_layer.tileheight)

    # find the tiles around the hero and extract their rects for collision
    tile_rects = []
    for diry in (-1, 0 , 1):
        for dirx in (-1, 0, 1):
            if coll_layer.content2D[tile_y + diry][tile_x + dirx] is not None:
                tile_rects.append(coll_layer.content2D[tile_y + diry][tile_x + dirx].rect)

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

    # return the step the hero should do
    return res_step_x, res_step_y

#  -----------------------------------------------------------------------------

def special_round(value):
    """
    For negative numbers it returns the value floored,
    for positive numbers it returns the value ceiled.
    """
    # same as:  math.copysign(math.ceil(abs(x)), x)
    # OR:
    # ## versus this, which could save many function calls
    # import math
    # ceil_or_floor = { True : math.ceil, False : math.floor, }
    # # usage
    # x = floor_or_ceil[val<0.0](val)

    if value < 0:
        return math.floor(value)
    return math.ceil(value)

#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()


