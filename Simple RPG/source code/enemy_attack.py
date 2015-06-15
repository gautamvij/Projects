import sys
import os
import math
import random
import time
import movements1
import person
import pygame
import tiledtmxloader
import person
import sound
from PIL import Image, ImageDraw, ImageFont
import cPickle as pk


# enemy's movements
def move_enemy(enm,right_enm,left_enm,dx_enm,speed):       
    i = 0
    for i in range(len(enm)):
        rand_enm = random.randint(0,100)
        if enm[i].rect.right >= right_enm[i] or rand_enm == 28 :
            dx_enm[i]=-1 
        elif enm[i].rect.left <= left_enm[i] or rand_enm == 11:
            dx_enm[i]=1
        enm[i].rect.centerx += (speed*dx_enm[i])

# direction update of enemies (change the attacking side of enemy according to 'y' coordinate of hero)
def dir_update(enm,hero,dy_enm):  
    i = 0
    for i in range(len(enm)):
        if(hero.rect.centery > enm[i].rect.centery):
            dy_enm[i] = 1
        else:
            dy_enm[i] = -1

# after direction update change the image too (image update)
def image_update(enm,image_var,dy_enm,images): 
    for i in range(len(enm)):
        if image_var[i]==15:
            image_var[i] = 0
        if dy_enm[i]==1:
            if (0<= image_var[i] <=4) and (enm[i].image != images[0]): enm[i].image = pygame.image.load(images[0])
            elif 5<= image_var[i] <=9: enm[i].image = pygame.image.load(images[1])
            else: enm[i].image = pygame.image.load(images[2])
        else:
            if 0<= image_var[i] <=4: enm[i].image = pygame.image.load(images[3])
            elif 5<= image_var[i] <=9: enm[i].image = pygame.image.load(images[4])
            else: enm[i].image = pygame.image.load(images[5])
        image_var[i] += 1

# function to choose type of the weapon
def weap_type(number):      
    if number==1 : return 3
    weap_no = random.randint(0,35)
    if 0 <= weap_no <10 :
        no = 1
    elif 10 <= weap_no <= 35 :
        no = 2
    return no

# Creating enemies's weapons
def create_weapons(weap_list,sprite_layers,enm,weap_dir,dy_enm,number):  
    i = 0
    for i in range(len(enm)):
        rand_attack = random.randint(0,500)
        if 0<= rand_attack <25:                          
            w = weap_type(number)
            if w==1:
                weap_list.append(person.create_person(enm[i].rect.centerx,(enm[i].rect.centery)+((dy_enm[i])*64),'./images/attack9.png'))
            else:
                weap_list.append(person.create_person(enm[i].rect.centerx,(enm[i].rect.centery)+((dy_enm[i])*64),'./images/attack2.png'))
            sprite_layers[2].add_sprite(weap_list[len(weap_list)-1])
            weap_dir.append(0)
            weap_dir.append(dy_enm[i])

def create_arrow(arrow_list,arrow_dir,drctn,hero,sprite_layers):
    # shooting arrow after pressing 'w'
    # append arrows in a list
    if(drctn=='right'):
        arrow_list.append(person.create_person((hero.rect.centerx)+64,hero.rect.centery,'./images/attack4_3.png'))
        arrow_dir.append(1)
        arrow_dir.append(0)
    elif(drctn=='left'):
        arrow_list.append(person.create_person((hero.rect.centerx)-64,hero.rect.centery,'./images/attack4_1.png'))
        arrow_dir.append(-1)
        arrow_dir.append(0)
    elif(drctn=='up'):
        arrow_list.append(person.create_person(hero.rect.centerx,(hero.rect.centery)-64,'./images/attack4_2.png'))
        arrow_dir.append(0)
        arrow_dir.append(-1)
    elif(drctn=='down'):
        arrow_list.append(person.create_person(hero.rect.centerx,(hero.rect.centery)+64,'./images/attack4_4.png'))
        arrow_dir.append(0)
        arrow_dir.append(1)
    sprite_layers[1].add_sprite(arrow_list[len(arrow_list)-1])

def create_specialarrow(specialarrow_list,specialarrow_dir,drctn,hero,sprite_layers):
    # shooting arrow after pressing 'w'
    # append arrows in a list
    if(drctn=='right'):
        specialarrow_list.append(person.create_person((hero.rect.centerx)+64,hero.rect.centery,'./images/specialarrow_1.png'))
        specialarrow_dir.append(1)
        specialarrow_dir.append(0)
    elif(drctn=='left'):
        specialarrow_list.append(person.create_person((hero.rect.centerx)-64,hero.rect.centery,'./images/specialarrow_2.png'))
        specialarrow_dir.append(-1)
        specialarrow_dir.append(0)
    elif(drctn=='up'):
        specialarrow_list.append(person.create_person(hero.rect.centerx,(hero.rect.centery)-64,'./images/specialarrow_3.png'))
        specialarrow_dir.append(0)
        specialarrow_dir.append(-1)
    elif(drctn=='down'):
        specialarrow_list.append(person.create_person(hero.rect.centerx,(hero.rect.centery)+64,'./images/specialarrow_4.png'))
        specialarrow_dir.append(0)
        specialarrow_dir.append(1)
    sprite_layers[1].add_sprite(specialarrow_list[len(specialarrow_list)-1])

# creating score slide for turn based fights
def create_score(i):
    if i == 0:
        i = "Miss"
    else :
        i = "-"+str(i)
    img = Image.open("./images/background.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./DroidSans.ttf",33)
    draw.text((1,5),i,(255,255,255),font=font)
    img.save('./images/sample-out.png')
    
# remove enemy sprite after its health becomes zero
def remove_enm(HP_ENM,enm,dx_enm,right_enm,left_enm,dy_enm,sprite_layers,gold,heart):   
    i = 0
    l = len(enm)
    while(i<l and i>=0):
        if HP_ENM[i] <= 0:
            savegame=pk.load(open("./save.p","rb"))
            savegame['xp']+=10
            pk.dump(savegame,open("./save.p","wb"))
            if 0<random.randint(0,100)<40:
                # random function to decide if enemy leaves heart (which increases hp of hero)
                heart.append(person.create_person(enm[i].rect.centerx,enm[i].rect.centery-((dy_enm[i])*32),'./images/heart.png'))
                sprite_layers[1].add_sprite(heart[(len(heart))-1])
            elif 40<= random.randint(0,100)<100:
                # random function to decide if enemy leaves gold
                gold.append(person.create_person(enm[i].rect.centerx,enm[i].rect.centery-((dy_enm[i])*32),'./images/gold.png'))
                sprite_layers[1].add_sprite(gold[(len(gold))-1])
            sprite_layers[1].remove_sprite(enm[i])
            enm.pop(i)
            HP_ENM.pop(i)
            dx_enm.pop(i)
            right_enm.pop(i)
            left_enm.pop(i)
            dy_enm.pop(i)
        else:
            i +=1
        l = len(enm)

def remove_weapon(hero,enm,weap_list,weap_dir,point,sprite_layers):  
    savegame=pk.load(open("./save.p","rb"))
    # remove weapons if they collide with hero
    # decrease the HP of player if it collides with any of enemies
    # if player has armor then both armor and hero shares the half of the loss
    j = 0
    for j in range(len(enm)):
        if pygame.sprite.collide_rect(hero,enm[j]):
            weap_sound = sound.create_soundfx('./sounds/weapon_touch.ogg')
            sound.volume(weap_sound,0.4)
            if savegame['sheild_hp']>0:
                savegame['sheild_hp'] -= (point/2)
                savegame['hp'] -= (point/2)
                if savegame['sheild_hp']<0:
                    savegame['sheild_hp'] = 0        
            else :
                savegame['hp'] -= point
            pk.dump(savegame,open("./save.p","wb"))    
            
    i = 0
    l = len(weap_list)
    while (i<l and i>=0):
        if pygame.sprite.collide_rect(hero,weap_list[i]):
            weap_sound = sound.create_soundfx('./sounds/weapon_touch.ogg')
            sound.volume(weap_sound,0.7)
            if savegame['sheild_hp']>0:
                savegame['sheild_hp'] -= (point/2)
                savegame['hp'] -= (point/2)
                if savegame['sheild_hp']<0:
                    savegame['sheild_hp'] = 0 
            else:
                savegame['hp'] -= point
            sprite_layers[2].remove_sprite(weap_list[i])
            weap_list.pop(i)
            weap_dir.pop(2*i)
            weap_dir.pop(2*i)
        elif movements1.check_collision(weap_list[i].rect.centerx, weap_list[i].rect.centery, 5*weap_dir[2*i],5*weap_dir[(2*i)+1],weap_list[i].rect.width,\
                                        5, sprite_layers[3]) == (0,0):
            sprite_layers[2].remove_sprite(weap_list[i])
            weap_list.pop(i)
            weap_dir.pop(2*i)
            weap_dir.pop(2*i)
        else :
            weap_list[i].rect.centerx += 5*weap_dir[2*i]
            weap_list[i].rect.centery += 5*weap_dir[(2*i)+1]
            i += 1
        l = len(weap_list)
        pk.dump(savegame,open("./save.p","wb"))

def remove_arrow(arrow_list,enm,HP_ENM,arrow_dir,sprite_layers,point):   
    # remove arrows if they collide with enemies or go out of field of view
    # decrease the HP of enemy if arrow collides with enemy
    i = 0
    l = len(arrow_list)
    while (i<l and i>=0):
        j=0
        check = 0
        for j in range(len(enm)):
            if pygame.sprite.collide_rect(enm[j],arrow_list[i]):
                if point==10.0:
                    specialarrow_sound = sound.create_soundfx('./sounds/specialarrow_touch.ogg')
                    sound.volume(specialarrow_sound,0.4)
                else:
                    arrow_sound = sound.create_soundfx('./sounds/arrow_touch.ogg')
                    sound.volume(arrow_sound,0.4)
                HP_ENM[j] -= point
                check = 1
                break
        if check==1 or movements1.check_collision(arrow_list[i].rect.centerx, arrow_list[i].rect.centery, 8*arrow_dir[2*i],8*arrow_dir[(2*i)+1],\
                                                  arrow_list[i].rect.width, 5, sprite_layers[3]) == (0,0):
            sprite_layers[1].remove_sprite(arrow_list[i])
            arrow_list.pop(i)
            arrow_dir.pop(2*i)
            arrow_dir.pop(2*i)
        else :
            arrow_list[i].rect.centerx += 25*arrow_dir[2*i]
            arrow_list[i].rect.centery += 25*arrow_dir[(2*i)+1]
            i += 1
        l = len(arrow_list)

# to create the sword sprite to attack on enemies
def attack(drctn,hero,mon,HP_ENM):
    savegame=pk.load(open("./save.p","rb"))
    result = -1
    if(drctn=='right'):
        sword_rect=pygame.Rect(hero.rect.right,hero.rect.centery,40,30)
    elif(drctn=='left'):
        sword_rect=pygame.Rect(hero.rect.left-30,hero.rect.centery,40,30)
    elif(drctn=='up'):
        sword_rect=pygame.Rect(hero.rect.centerx,hero.rect.top,30,40)
    elif(drctn=='down'):
        sword_rect=pygame.Rect(hero.rect.centerx,hero.rect.bottom,30,40)
        
    i=0
    for i in range(0,len(mon)):
        if pygame.Rect.colliderect(mon[i].rect,sword_rect):
            sword_sound = sound.create_soundfx('./sounds/sword.ogg')
            sound.volume(sword_sound,0.4)
            result = i
            break
    else:
        del sword_rect
        result = len(mon)+1
   
    if(result != (len(mon)+1)):
        swrd_have=savegame['eqp_weapon']
        if(swrd_have==None):
            sword_dmg=0
        elif(swrd_have=='dagger'):
            sword_dmg=10.0
        elif(swrd_have=='sw1'):
            sword_dmg=15.0
        elif(swrd_have=='sw2'):
            sword_dmg=20.0
        elif(swrd_have=='sw3'):
            sword_dmg=25.0
        HP_ENM[result] -= sword_dmg

