import sys
import os
import math
from shifty1 import *
import cPickle as pk
import menu
import pygame
from pygame.locals import *
import sound
import person
import shifty1

#initializing the pygame
pygame.init()

try:
    import _path
except:
    pass

#opening the newgame dictionary
main_dict=pk.load(open("./newgame.p","rb"))
#creating the screen
screen = pygame.display.set_mode((1024,768))
#creating bg music
musicbg=sound.create_music('start')
#creating main menu image
imag='./images/menumain_empty.png'
#story image list
story_img=['./images/story_bg1.png','./images/story_bg2.png','./images/story_bg3.png',\
            './images/story_bg4.png','./images/story_bg5.png','./images/story_bg6.png']
#main loop
while True:
    #loading and blitting the main menu
    img=pygame.image.load(imag)
    img_rect=img.get_rect()
    img_rect.center=(512,393)

    screen.blit(img,img_rect)
    #refreshing the screen
    pygame.display.update()

#------------------Event handling-------------
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            x=event.key
            #NEW GAME
            if x==pygame.K_n:
                #creating a save.p file for using in game -> saving -> handling main conditoions
                #--> no change in newgame dictionary made
                #if save.p exists -> and newgame started -> save.p overwritten
                pk.dump(main_dict,open("./save.p","wb"))
                #to show images of story
                j=0
                while(j<6):
                    img=pygame.image.load(story_img[j])
                    img_rect=img.get_rect()
                    img_rect.center=(512,393)
                    screen.blit(img,img_rect)
                    pygame.display.update()
                    #Infinite loop until image is to be removed
                    i=0
                    while(i!=1):
                        for event in pygame.event.get():
                            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                                i=1
                        continue
                    j+=1
                #when stroy images finished
                musicbg.stop()
                #starting the first map
                demo_pygame('./maps/village1.tmx',0)
            #control menu
            elif x==pygame.K_c:
                imag='./images/control_menu.png'
            #go back to main
            elif x==pygame.K_k:
                imag='./images/menumain_empty.png'
            #load game
            elif x==pygame.K_l:
                main_dict=pk.load(open("./save.p","rb"))
                #load game only if there exists a save game
                if main_dict['save']!=0:
                    mp=main_dict['last_map']
                    frm=main_dict['last_frm']
                    demo_pygame(mp,frm)
                else:
                    imag='./images/nosavedgame.png'
                    #img_rect=img.get_rect()
                    #img_rect.center=(512,393)
                    #screen.blit(img,img_rect)
                    #pygame.display.update()
            #exit the game
            elif (x==pygame.K_ESCAPE or x==pygame.K_q):
                pygame.quit()
