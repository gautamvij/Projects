

import sys
import os
import math
import random
import time
from hero_entry import *
from hero_exit import *
import movements
import person
import pygame
import tiledtmxloader
import constants

import cPickle as pk
import menu
try:
    import _path
except:
    pass

#Check / change the conditions for talking to vilager
def iftalk(coll,x,vil,count,herox,heroy,map_name):
    maindict=pk.load(open("./save.p","rb"))
    #which time is hero talking to villager -> 0->first time ,1->second time
    timetalk=0
    #condition -> if hero is collididng to one of the villagers & count is less than 1 (==0) (to show first dialogue)
    #space is pressed, and talking first time (maindict['talk_vil'][map_name][coll]==0)
    if(coll in range(0,len(vil)) and count<1 and x==pygame.K_SPACE\
       and maindict['talk_vil'][map_name][coll]==0):
            #conditions for some special villagers
            #the man giving the weapons
            if(map_name=='./maps/village1.tmx' and coll==2):
                maindict['sheild_first']=1
                maindict['bow_arrow_first']=1
                maindict['arrow_count']=17
                maindict['sheild_hp']=38
                maindict['eqp_armour']='nrml'
            #The lady with burning house taks
            if(map_name=='./maps/village1.tmx' and coll==1 and maindict['b_h_vil']==0):
                return [count+1,coll,1]
            #fishing guy
            if(map_name=='./maps/village2_out1.tmx' and coll==0 and maindict['f_vil']==0):
                return [count+1,coll,1]
            #pirate
            if(map_name=='./maps/ship.tmx' and maindict['pirate_vil']==0):
                maindict['pirate']=1
                pk.dump(maindict,open("./save.p","wb"))
                return [count+1,coll,1]
            #spooky guy in village2 inside
            if(map_name=='./maps/village2_inside.tmx' and maindict['spook']==0 and coll==2):
                return [count+1,coll,1]
            #talking to other villagers
            #talking time made 1
            maindict['talk_vil'][map_name][coll]=1
            timetalk=1
            pk.dump(maindict,open("./save.p","wb"))
            #cound made 1 to start the talking
            count +=1
    #talking again
    elif(coll in range(0,len(vil)) and count<1 and x==pygame.K_SPACE \
         and maindict['talk_vil'][map_name][coll]==1):
            count +=1
            timetalk=2
    #if not colliding with any villager -> count is keot zero -> the talking will not be started
    #no first dialogue will be shown
    elif(coll==None):
        count = 0
        
    return [count,coll,timetalk]
