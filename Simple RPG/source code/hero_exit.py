import sys
import os
import math
import cPickle as pk
import pygame
import random
try:
    import _path
except:
    pass

import tiledtmxloader

# checks if hero collides to a portal
# if it does then returns the index of the portal
# otherwise returns -1
def exit_map(hero,portal):
    plen=len(portal)
    i=0
    for i in range(0,plen):
        if pygame.Rect.colliderect(hero.rect, portal[i]):
            return i
    return -1

# if hero collides to portal then it returns the next map corresponding to that portal
def next_map(map_name,portal_num):
    sv=pk.load(open("./save.p","rb"))
    if map_name=='./maps/village1.tmx':
        if portal_num==0:
            return ['./maps/tunnel.tmx',0]
        elif portal_num==1:
            return ['./maps/tunnel2_4.tmx',0]
        elif portal_num==2:
            return ['./maps/tunnel3.tmx',0]
        elif portal_num==3:
            return ['./maps/tunnel2_4.tmx',1]

    elif map_name=='./maps/tunnel2_4.tmx':
        if (portal_num==0 or portal_num==1):
            return ['./maps/village1.tmx',1]

    elif map_name=='./maps/tunnel3.tmx':
        if portal_num==0:
            return ['./maps/ship.tmx',0]

    elif map_name=='./maps/mountainclimbing.tmx':
        if portal_num==0:
            return['./maps/mountain_top.tmx',0]

    elif map_name=='./maps/village2_out1.tmx':
        if portal_num==0:
            return ['./maps/village2_inside.tmx',0]

    elif map_name=='./maps/village2_inside.tmx':
        if portal_num==0:
            return ['./maps/village2_out1.tmx',1]
        elif (portal_num==1 and sv['spook']==1):
            # sv['spook'] == 1 denotes that hero has talked to spooky guy
            # 'village2_inside' contains two paths to go out of this map
            # portal_num == 1 denotes the first path 
            return ['./maps/mountainclimbing.tmx',0]
        elif (portal_num==2 and sv['spook']==1):
            # portal_num == 1 denotes the first path 
            return ['./maps/mountainclimbing.tmx',0]
        elif portal_num==3:
            # portal_num == 3 denotes the hotel map
            return ['./maps/hotel.tmx',0]

    elif map_name=='./maps/tunnel.tmx':
        if portal_num==0:
            return ['./maps/village1.tmx',1]
        elif portal_num==1:
            return ['./maps/tunnel2.tmx',0]

    elif map_name=='./maps/ship.tmx':
        if (portal_num==0 and sv['pirate']==1):
            # sv['pirate'] == 1 denotes that hero has talked to pirate guy
            if(random.randint(1,2)==1):
                return['./maps/maze.tmx',0]
            else:
                return['./maps/maze2.tmx',0]

    elif map_name=='./maps/maze.tmx':
        if portal_num==0:
            return['./maps/safe1.tmx',0]
    elif map_name=='./maps/maze2.tmx':
        if portal_num==0:
            return['./maps/safe1.tmx',0]
