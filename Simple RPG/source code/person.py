import sys
import os
import math
import random
import time
import pygame
import tiledtmxloader
from constants import *
from PIL import Image, ImageDraw, ImageFont
try:
    import _path
except:
    pass

#creating a general sprite with the given image and adding it to given position
def create_person(start_pos_x, start_pos_y,img):
    image = pygame.image.load(img)
    rect = image.get_rect()
    rect.midbottom = (start_pos_x, start_pos_y)
    new_sprite= tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)
    return new_sprite

#create the text image sprite and saving it
def create_text_img(tximg,menutext,dialog_show):
    imgtx = Image.open(tximg)
    draw = ImageDraw.Draw(imgtx)
    font = ImageFont.truetype("./PAPYRUS.ttf",30)
    draw.text((260,70),menutext[dialog_show],(0,0,0),font=font)
    name='./images/sample-out_talk.png'
    imgtx.save(name)
    return name
    
#create the text sprite -> different form create person as midtop required 
def create_menu_bg(start_pos_x, start_pos_y,img):
    image = pygame.image.load(img)
    rect = image.get_rect()
    rect.midtop = (start_pos_x, start_pos_y)
    menu = tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)
    return menu

#Creating the villager dictionary
def create_villager(map_name):
    #creating villagers according to maps
    if(map_name=='./maps/village1.tmx'):
        #giving co-ordinates
        vil1x=6*32
        vil1y=66*32
        #the starting image of the villager
        imge='./images/villager1_d2.png'
        #the dictionary of the villager
        #sprte-> holds the sprite of the villager
        #toplx, toply -> hold the top x and y co-ord of the imaginary movement rect
        #w,h -> holds the width and height of the rect
        vil1 = {'sprte':create_person(vil1x,vil1y,imge),'toplx':5*32,'toply':65*32,'w':2*32,'h':5*32}
        vil2x=27*32
        vil2y=59*32
        img='./images/villager2_d2.png'
        vil2={'sprte':create_person(vil2x,vil2y,img),'toplx':24*32,'toply':59*32,'w':7*32,'h':3*32}
        vil3x=19*32+8
        vil3y=20*32+8
        img='./images/villager3_d2.png'
        vil3={'sprte':create_person(vil3x,vil3y,img),'toplx':17*32,'toply':19*32,'w':4*32,'h':4*32}
        return [vil1,vil2,vil3]
    elif(map_name=='./maps/village2_out1.tmx'):
        vil1x=25*32+16
        vil1y=24*32+16
        imge='./images/fishing_guy.png'
        #rect variables = None -> stationary villager
        vil1 = {'sprte':create_person(vil1x,vil1y,imge),'toplx':None,'toply':None,'w':None,'h':None}
        return [vil1]
    elif(map_name=='./maps/spooky.tmx'):
        vil1x=23*20
        vil1y=23*20
        imge='./images/spook_d1.png'
        vil1 = {'sprte':create_person(vil1x,vil1y,imge),'toplx':None,'toply':None,'w':None,'h':None}
        return [vil1]
    elif(map_name=='./maps/village2_inside.tmx'):
        vil1x=20*32+16
        vil1y=32*32+16
        imge='./images/villager1_d2.png'
        vil1 = {'sprte':create_person(vil1x,vil1y,imge),'toplx':16*32,'toply':29*32,'w':8*32,'h':6*32}
        vil2x=36*32
        vil2y=47*32
        img='./images/villager4_d2.png'
        vil2={'sprte':create_person(vil2x,vil2y,img),'toplx':32*32,'toply':45*32,'w':7*32,'h':5*32}
        vil3x=2*32+20
        vil3y=18*32+8
        img='./images/spook_d1.png'
        vil3={'sprte':create_person(vil3x,vil3y,img),'toplx':2*32,'toply':18*32,'w':1,'h':1}
        vil4x=17*32
        vil4y=52*32
        img='./images/villager8_d3.png'
        vil4={'sprte':create_person(vil4x,vil4y,img),'toplx':16*32,'toply':51*32,'w':3*32,'h':3*32}
        vil5x=35*32
        vil5y=17*32
        img='./images/villager5_d2.png'
        vil5={'sprte':create_person(vil5x,vil5y,img),'toplx':35*32,'toply':17*32,'w':1,'h':1}
        vil6x=36*32
        vil6y=18*32
        img='./images/villager6_l2.png'
        vil6={'sprte':create_person(vil6x,vil6y,img),'toplx':36*32,'toply':18*32,'w':1,'h':1}
        vil7x=34*32
        vil7y=18*32
        img='./images/villager7_r2.png'
        vil7={'sprte':create_person(vil7x,vil7y,img),'toplx':34*32,'toply':18*32,'w':1,'h':1}

        #returning the list of dictionaries
        return [vil1,vil2,vil3,vil4,vil5,vil6,vil7]

    #if no vilaager return empty list
    else:
        return []

#creating the list of ->list of -> villager images
def create_v_pics(map_name):
    ##from "constants.py"
    if map_name=='./maps/village1.tmx':
        return [vil1_img, vil2_img, vil3_img] #meaning->constants.vil2_img etc

    elif map_name=='./maps/village2_inside.tmx':
        return [vil4_img,vil5_img,vil6_img,vil7_img,vil8_img,vil9_img,vil10_img]

    #return None if no villager
    else:
        return None

#creating collectables on the map
#creatung same as villagers
def create_misc(map_name):
    if map_name=='./maps/village1.tmx':
        misc1x=31*32+16
        misc1y=75*32
        imge='./images/boots.png'
        misc1 = {'sprte':create_person(misc1x,misc1y,imge),'name':'boots','value':30}
        misc2x=69*32
        misc2y=70*32+16
        imge='./images/locket.png'
        misc2 = {'sprte':create_person(misc2x,misc2y,imge),'name':'locket','value':60}
        misc3x=21*32
        misc3y=48*32+16
        imge='./images/fish_rod.png'
        misc3 = {'sprte':create_person(misc3x,misc3y,imge),'name':'fish_rod','value':20}
        return [misc1,misc2,misc3]
    elif map_name=='./maps/village2_out1.tmx':
        misc1x=16*32+16
        misc1y=9*32
        imge='./images/bush1.png'
        misc1 = {'sprte':create_person(misc1x,misc1y,imge),'name':'rose','value':10}
        return [misc1]
    elif map_name=='./maps/village2_inside.tmx':
        misc1x=6*32+16
        misc1y=17*32
        imge='./images/lamp.png'
        misc1 = {'sprte':create_person(misc1x,misc1y,imge),'name':'lamp','value':40}
        misc2x=41*32
        misc2y=18*32+16
        imge='./images/book.png'
        misc2 = {'sprte':create_person(misc2x,misc2y,imge),'name':'book','value':40}
        return [misc1,misc2]


#creating portals for changing maps
#portals are rectangles that return their index (in "hero_exit.py") if collision happens (-1 of no collision)
#and if the condition of the map are satisfied -> map changes
def create_portal(map_name):
    if map_name=='./maps/village1.tmx':
        portal1=pygame.Rect(69*32,4*32,4*32,3*32)
        portal2=pygame.Rect(76*32,4*32,4*32,3*32)
        portal3=pygame.Rect(83*32,4*32,4*32,3*32)
        portal4=pygame.Rect(90*32,4*32,4*32,3*32)

        return [portal1,portal2,portal3,portal4]

    elif map_name=='./maps/village2_out1.tmx':
        portal1=pygame.Rect(42*32,0*32,2*32,2*32)

        return [portal1]

    elif map_name=='./maps/tunnel3.tmx':
        portal1=pygame.Rect(58*32,28*32,2*32,8*32)

        return [portal1]

    elif map_name=='./maps/tunnel2_4.tmx':
        portal1=pygame.Rect(4*32,96*32,3*32,2*32)
        portal1=pygame.Rect(85*32,61*32,1*32,3*32)

        return [portal1,portal2]

    elif map_name=='./maps/village2_inside.tmx':
        portal1=pygame.Rect(23*32,55*32,3*32,1*32)

        portal2=pygame.Rect(22*32,1*32,2*32,1*32)
        portal3=pygame.Rect(25*32,1*32,2*32,1*32)
        portal4=pygame.Rect(20*32,20*32,50,50)
        portal5=pygame.Rect(3*32-10,18*32,20,32)

        return [portal1,portal2,portal3,portal4]

    elif map_name=='./maps/ship.tmx':
        portal1=pygame.Rect(57*32,2*32,1*32,2*32)

        return [portal1]

#creating a shop portal-> buying/selling menu comes up if colliding with this portal and pressing SPACE("shifty1.py")
def create_shop_portal(map_name):
    if map_name=='./maps/village2_inside.tmx':
        portal1=pygame.Rect(38*32,23*32,1*32,3*32)

        return portal1
    else:
        return None
