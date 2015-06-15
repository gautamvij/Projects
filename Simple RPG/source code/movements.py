import sys
import os
import math
import random
import time
import pygame
import tiledtmxloader
import person
from collision import *
import sound

try:
    import _path
except:
    pass


#Main hero moving function
#mr,ml,md,mu ->variables for each direction whose value decide the images for animation
#hero_pos_(x/y) -> hero's current position
#speed ->hero's speed
#sprite_layers-> all the layers in map (for collision function)
#vil -> villager dictionary of the map
#misc-> misc collectable dictionary of the map
def hero_move(mr,ml,md,mu,hero_pos_x,hero_pos_y,hero,speed,sprite_layers,vil,misc):
        vcount=len(vil)
        #decideing the diretion dx=1->right, dy=-1->up and so on
        dx = pygame.key.get_pressed()[pygame.K_RIGHT] - pygame.key.get_pressed()[pygame.K_LEFT]
        dy = pygame.key.get_pressed()[pygame.K_DOWN] - pygame.key.get_pressed()[pygame.K_UP]
        #cancelling the diagonal movement
        #due to this snippet horizontal direction overides the viertical one
        if(dx==+1 or dx==-1):
                dy=0
        ##HERO RIGHT MOVEMENT
        if(dx==1):
            #all other animation variables made 1
            ml=md=mu=1
            #right animation var made +1
            mr +=1
            ##Code for changing the image according to the variable value
            if(mr==15):
                mr=1
            if mr in range(1,8):
                hero.image=pygame.image.load('./images/hero_r1.png')
            elif mr in range(8,15):
                hero.image=pygame.image.load('./images/hero_r3.png')
        #HERO LEFT MOVEMENT
        elif(dx==-1):
            #changed
            mr=md=mu=1
            ml += 1
            if(ml==15):
                ml=1
            if (ml in range(1,8)):
                hero.image=pygame.image.load('./images/hero_l1.png')
            elif ml in range(8,15):
                hero.image=pygame.image.load('./images/hero_l3.png')
        #HERO UP MOVEMENT
        elif(dy==-1):
            #changed
            ml=md=mr=1
            mu +=1
            if(mu==15):
                mu=1
            if mu in range(1,8):
                hero.image=pygame.image.load('./images/hero_d1.png')
            elif mu in range(8,15):
                hero.image=pygame.image.load('./images/hero_d3.png')
        #HERO DOWN MOVEMENT
        elif(dy==1):
            #changed
            ml=mr=mu=1
            md += 1
            if(md==15):
                md=1
            if (md in range(1,8)):
                hero.image=pygame.image.load('./images/hero_u1.png')
            elif md in range(8,15):
                hero.image=pygame.image.load('./images/hero_u3.png')

        #TAKING THE STEP
        #these values contain the next step of the hero
        step_x = speed  * dx 
        step_y = speed  * dy
        #checking if the next step collides with collision layer on the map
        #if does not collide -> keeps the changed step
        #if collides the original steps are returned
        ##31,5-> width and height of hero rect
        #height made less to give a better visual effect of hero overlapping some objects parialy
        step_x, step_y = collision_world(hero_pos_x, hero_pos_y, step_x, step_y, 31, 5, sprite_layers[3])
        #a hypothetical hero sprite
        hero_hypo=hero
        #hypothetcal sprite gets the same rectangle
        hero_hypo.rect.midbottom=hero.rect.midbottom
        #the hypothetical hero moves a bit farther than the main sprite
        new_pos_x=hero_pos_x + step_x*2
        new_pos_y=hero_pos_y + step_y*2
        hero_hypo.rect.midbottom=(new_pos_x, new_pos_y)

        #sound for movement
        if(step_x!=0 or step_y!=0):
            steps=sound.create_soundfx('./sounds/step.ogg')  
            steps.set_volume(0.1)

        #check if the hypothetical sprite is colliding with the vilagers
        #one step was not enough
        i = 0  
        for i in range(0,len(vil)):
            if checkCollision(hero_hypo, vil[i]['sprte']):
                break
        #if nothing in the way -> move the hero
        else:
            hero_pos_x += step_x
            hero_pos_y += step_y
            hero.rect.midbottom = (hero_pos_x, hero_pos_y)
        #return the required variables
        #mr,ml,md,mu returned tisave which image was being shown to keep the movement smoother
        return [mr, ml, md, mu, hero_pos_x, hero_pos_y, hero, hero_hypo]

#function to move the villagers
#drctn -> the old direction in which a villager was moving
#drctn -> list with length = no. of villagers
#vmu,vmr,vmd,vml -> variables for changing the images of villagers for animation
#an imaginary rectangle is made for every villager which bouds the movement of that villager
#vilager cannot move outside this rectangle -> made along with villager in "person.py"
def move_villager(drctn,speed,vil,hero_hypo,vmu,vmr,vmd,vml,map_name):
    #f no illager (then no direction)->give nothing
    if drctn==None:
        return None
    #get the images of villager movements
    #pic[x][y] -> x tells which villager, y tells which image
    pic=person.create_v_pics(map_name)
    #directions initialised--------> NOTE different from vmu,vmr,vmd,vml
    muv='up'
    mdv='down'
    mrv='right'
    mlv='left'
    no=''#no direction -> just standing
    #speed of the villager
    speedv=speed
    #initializing the old direction (any value will do)
    dir_old=muv
    #a random variable to change directions
    chng=random.randint(0,1000)
    i=0
    ##condition fro stationary villagers
    #villager dictionary explained in "person.py"
    for i in range(0,len(vil)):
        if(vil[i]['toplx']==None):
            return None

        #Create a hypothetical rectangles for villager and hero
        vil_hypo=pygame.Rect(vil[i]['sprte'].rect.left-100,vil[i]['sprte'].rect.top-100,vil[i]['sprte'].rect.width+100,vil[i]['sprte'].rect.height+100)
        her_hypo=pygame.Rect(hero_hypo.rect.left-10,hero_hypo.rect.top-10,hero_hypo.rect.width+10,hero_hypo.rect.height+10)
        
        #UP DIRECTION
        if drctn[i]==muv:
            #same logic as hero to change the images
            if pic!=None:
                vml=vmd=vmu=1
                vmu +=1
                if(vmu==15):
                    vmu=1
                #store the current direction in dir_old variable
                dir_old=drctn[i]
                if vmu in range(1,8):
                    vil[i]['sprte'].image=pygame.image.load(pic[i][0])
                elif vmu in range(8,15):
                    vil[i]['sprte'].image=pygame.image.load(pic[i][1])

            ##if the hypothetical rectangles collide -> stop the villager
            ##otherwise villager could move up on the hero and then hero -> unable to move :-O
            if collision_other(her_hypo, vil_hypo):
                speedv=0

            #moving the villager upwards
            #can move only upto a limit
            if(vil[i]['sprte'].rect.top>vil[i]['toply']+15):
                vil[i]['sprte'].rect.top-=speedv
                #changing directions in between
                if(chng==10):
                    drctn[i]=decidedirection()
                elif(chng%30<2):
                    drctn[i]=no
            #chabge direction if limit of up direction reached
            else:
                drctn[i]=decidedirection()

        #DOWN MOVEMENT
        elif drctn[i]==mdv:
            if pic!=None:
                vml=vmr=vmu=1
                vmd +=1
                if(vmd==15):
                    vmd=1
                dir_old=drctn[i]
                if vmd in range(1,8):
                    vil[i]['sprte'].image=pygame.image.load(pic[i][4])
                elif vmd in range(8,15):
                    vil[i]['sprte'].image=pygame.image.load(pic[i][5])

            dir_old=drctn[i]
            if collision_other(her_hypo, vil_hypo):
                speedv=0
            if(vil[i]['sprte'].rect.bottom<(vil[i]['toply']+vil[i]['h']-15)):
                vil[i]['sprte'].rect.bottom+=speedv
                if(chng==10):
                    drctn[i]=decidedirection()
                elif(chng%30<2):
                    drctn[i]=no
            else:
                drctn[i]=decidedirection()

        #LEFT MOVEMENT
        elif drctn[i]==mlv:
            if pic!=None:
                vmr=vmd=vmu=1
                vml +=1
                if(vml==15):
                    vml=1
                dir_old=drctn[i]
                if vml in range(1,8):
                    vil[i]['sprte'].image=pygame.image.load(pic[i][6])
                elif vml in range(8,15):
                    vil[i]['sprte'].image=pygame.image.load(pic[i][7])

            dir_old=drctn[i]
            if collision_other(her_hypo, vil_hypo):
                speedv=0
            if(vil[i]['sprte'].rect.left>vil[i]['toplx']+15):
                vil[i]['sprte'].rect.left-=speedv
                if(chng==10):
                    drctn[i]=decidedirection()
                elif(chng%30<2):
                    drctn[i]=no
            else:
                drctn[i]=decidedirection()

        #RIGHT MOVEMENT
        elif drctn[i]==mrv:
            if pic!=None:
                vml=vmd=vmu=1
                vmr +=1
                if(vmr==15):
                    vmr=1
                dir_old=drctn[i]
                if vmr in range(1,8):
                    
                    vil[i]['sprte'].image=pygame.image.load(pic[i][2])
                elif vmr in range(8,15):
                    vil[i]['sprte'].image=pygame.image.load(pic[i][3])

            dir_old=drctn[i]
            if collision_other(her_hypo, vil_hypo):
                speedv=0
            if(vil[i]['sprte'].rect.right<(vil[i]['toplx']+vil[i]['w']-15)):
                vil[i]['sprte'].rect.right+=speedv
                if(chng==10):
                    drctn[i]=decidedirection()
                elif(chng%30<2):
                    drctn[i]=no
            else:
                drctn[i]=decidedirection()

        #NO MOVEMENT
        elif drctn[i]==no:
            if collision_other(her_hypo, vil_hypo):
                speedv=0
            elif(chng%200==0):
                #after stooping keep moving in the old direction
                drctn[i]=dir_old
        
    #return the list containg the old direcions of the villagers
    return drctn

#function to decide random direction of the villager based on a random integer
def decidedirection():
    muv='up'
    mdv='down'
    mrv='right'
    mlv='left'
    d=muv  #settig an initial value - can be any direction
    a=random.randint(1,12)
    if a in range(1,3):
        d=muv
    elif a in range(4,6):
        d=mrv
    elif a in range(7,9):
        d=mdv
    elif a in range (10,12):
        d=mlv
    return d

def colliding_other_living(vil,hero_hypo):
    for i in range(0,len(vil)):
        vil_hypo=pygame.Rect(vil[i]['sprte'].rect.left-10,vil[i]['sprte'].rect.top-10,vil[i]['sprte'].rect.width+10,vil[i]['sprte'].rect.height+10)
        her_hypo=pygame.Rect(hero_hypo.rect.left-10,hero_hypo.rect.top-10,hero_hypo.rect.width+10,hero_hypo.rect.height+10)
        if collision_other(her_hypo, vil_hypo):
            return i