import sys
import os
import math

import pygame

try:
    import _path
except:
    pass

import tiledtmxloader

# 'frm' denotes the portals in a map
# this function returns the coordinates of hero after entering the portal
def entry(map_name,frm):
    if(map_name=='./maps/village1.tmx' and frm==0):     
        return [2*32,70*32+16]
    elif(map_name=='./maps/village1.tmx' and frm==1):
        return [82*32,10*32+16]
    elif(map_name=='./maps/village1.tmx' and frm==2):
        return [31*32+20,60*32]
    elif(map_name=='./maps/village2_out1.tmx' and frm==0):
       return [3*32,26*32]
    elif(map_name=='./maps/village2_out1.tmx' and frm==1):
       return [42*32,5*32]
    elif(map_name=='./maps/village2_out1.tmx' and frm==2):
       return [23*32+20,21*32]
    elif(map_name=='./maps/village2_inside.tmx' and frm==0):
        return [22*32,51*32]
    elif(map_name=='./maps/village2_inside.tmx' and frm==1):
        return [20*32+20,23*32]
    elif(map_name=='./maps/village2_inside.tmx' and frm==2):
        return [4*32+20,20*32]
    elif(map_name=='./maps/tunnel3.tmx' and frm==0):
        return [21*32,72*32]
    elif(map_name=='./maps/ship.tmx' and frm==0):
        return [4*32,3*32]
    elif(map_name=='./maps/ship.tmx' and frm==1):
        return [53*32,2*32+16]

