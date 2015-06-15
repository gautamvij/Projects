


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
import talk
import cPickle as pk
from PIL import Image, ImageDraw, ImageFont
import script
import shifty1

try:
    import _path
except:
    pass

#creating the text fot the willagers
#talked-> if the hero is talking again (if there is need to show different text)
def create_menu_vil(which_vil,map_name,talked):
    talkd1=script.text_talk_first
    talkd2=script.text_talk_sec
    
    if talked==1:
        vil_i = str(which_vil)
        txt=talkd1[map_name][vil_i]
    elif talked==2:
        vil_i = str(which_vil)
        txt=talkd2[map_name][vil_i]
    return txt

#creating the inventory menu
def create_menu_inventory(c_pos):
    sv=pk.load(open("./save.p","rb"))
    #loading the base image
    imgtx = Image.open('./images/paper1.png')
    draw = ImageDraw.Draw(imgtx)
    #determining the font
    font1 = ImageFont.truetype("./PAPYRUS.ttf",40)
    font = ImageFont.truetype("./PAPYRUS.ttf",30)
    inv_len=len(sv['misc'])
    #if nothing in inventory
    if inv_len==0:
        #writing on the base image
        draw.text((200,60),'You dont have anything',(0,0,0),font=font1)
        draw.text((240,90),'in your Inventory',(0,0,0),font=font1)
    else:
        #cost and name stored in different lists
        inven=sv['misc']
        inven_item=[]
        inven_cost=[]
        inven_str=[]
        draw.text((300,20),'Inventory',(0,0,0),font=font1)
        for i in range(0,inv_len,2):
            inven_item.append(inven[i])
            inven_cost.append(inven[i+1])

        for i in range(0,inv_len/2):    
            inven_list=inven_item[i]+'   '+str(inven_cost[i])
            inven_str.append(inven_list)

        #snippet for printing inventory in two columns if there are many things
        for j in range(100,420,50):
            if (len(inven_str))!=0:
                draw.text((100,j),inven_str[0],(0,0,0),font=font)
                inven_str.pop(0)
            else:
                break

        for j in range(100,420,50):
            if (len(inven_str))!=0:
                draw.text((500,j),inven_str[0],(0,0,0),font=font)
                inven_str.pop(0)
            else:
                break

    #saving the new image (image with text) as a temporary image
    imgtx.save('./images/inventory.png')
    inven_sprite=person.create_menu_bg(c_pos[0],c_pos[1]-200,'./images/inventory.png')
    
    return inven_sprite

#function to exit a text image if x is pressed
def exit_menu(x):
    while(x!=pygame.K_SPACE):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                x=event.key
        continue

#Creating the save menu
def save_menu(c_pos):
    imgtx = Image.open('./images/paper.png')
    draw = ImageDraw.Draw(imgtx)
    font = ImageFont.truetype("./PAPYRUS.ttf",60)
    draw.text((30,70),'Game Saved',(0,0,0),font=font)
    imgtx.save('./images/savedm.png')
    saved=person.create_menu_bg(c_pos[0],c_pos[1]-768/2+250,'./images/savedm.png')
    return saved

#Creating the health bar
def create_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos):
    sv=pk.load(open("./save.p","rb"))
    hp_max=sv['max_hp']
    hp=hp_max
    #scaling down the hp image according to current hit points(hp) w.r.t. max hp
    c_hp = hp/hp_max * 99
    c_hp=int(c_hp)
    if (c_hp)>0:
        test_image = "./images/hp_bar.png"
        original = Image.open(test_image)
        # Get dimensions of original picture
        width, height = original.size
        left = 0
        top = 0
        #giving the length as required
        right = c_hp
        bottom = height
        #crooing and saving the image
        cropped_example = original.crop((left, top, right, bottom))
        cropped_example.save('./images/test_hp.png')

        #creating the sprite, adding it and then rendering the screen
        c_hp_sprite=person.create_person(c_pos[0]-450,c_pos[1]-380,'./images/test_hp.png')
        sprite_layers[2].add_sprite(c_hp_sprite)
        shifty1.render_update(renderer,sprite_layers,screen)

        pk.dump(sv,open("./save.p","wb"))

        return [c_hp_sprite,hp]

#updating the hp bar
def update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,dmg):
    sv=pk.load(open("./save.p","rb"))
    hp=sv['hp']
    hp_max=sv['max_hp']
    hp=hp-dmg
    ##SAME AS CREATING HP BAR
    c_hp = (hp* 99.0)/hp_max
    c_hp=int(c_hp)
    if (c_hp)>0:
        test_image = "./images/hp_bar.png"
        original = Image.open(test_image)
        # Get dimensions
        width, height = original.size
        left = 0
        top = 0
        right = c_hp
        bottom = height
        cropped_example = original.crop((left, top, right, bottom))
        cropped_example.save('./images/test_hp.png')
        #no need for sprite creating or rendering
        #just changing the image (new cropped image)
        #rendering will be done in outer files/functions
        hp_sprite.image=pygame.image.load('./images/test_hp.png')
    
#Creating the dragon health interface
def create_interface_dragon(renderer,sprite_layers,screen,c_pos):
    interface=person.create_person(c_pos[0]-400,c_pos[1],'./images/dragon_health_interface.png')
    sprite_layers[1].add_sprite(interface)
    shifty1.render_update(renderer,sprite_layers,screen)
    return interface

#Creating dragon health bar -> SIMILAR TO CREATING HERO HP BAR
def create_dragon_hp(renderer,sprite_layers,screen,dhp_sprite,c_pos,dhp):
    c_dhp = (dhp[0]* 400)/100
    c_dhp=int(c_dhp)
    if c_dhp==0:
        c_dhp=1
    test_image = "./images/dragon_health.png"
    original = Image.open(test_image)
    width, height = original.size
    left = 0
    top = 0
    right = c_dhp
    bottom = height
    cropped_example = original.crop((left, top, right, bottom))
    cropped_example.save('./images/test_dhp.png')
    sprite_layers[2].remove_sprite(dhp_sprite)


    c_dhp_sprite=person.create_person(c_pos[0]-400,c_pos[1],'./images/test_dhp.png')
    sprite_layers[2].add_sprite(c_dhp_sprite)
    shifty1.render_update(renderer,sprite_layers,screen)
    return c_dhp_sprite

#Updating the dragon hp bar -> SAME AS UPDATING HERO HP BAR
def update_dhp_bar(renderer,sprite_layers,screen,dhp_sprite,c_pos,dhp):
    c_dhp = (dhp[0]* 400)/100
    c_dhp=int (c_dhp)
    if c_dhp==0:
        c_dhp=1
    test_image = "./images/dragon_health.png"
    original = Image.open(test_image)
    width, height = original.size
    left = 0
    top = 0
    right = c_dhp
    bottom = height
    cropped_example = original.crop((left, top, right, bottom))
    cropped_example.save('./images/test_dhp.png')

    dhp_sprite.image=pygame.image.load('./images/test_dhp.png')
    
#Creating the Level and Gold value
def create_l_g(renderer,sprite_layers,screen,c_pos):
    #loading, creating sprite and rendering of the base image i.e no image -> plain image
    lg=person.create_menu_bg(c_pos[0]-504,c_pos[1]-390,'./images/level_gold_1.png')
    sprite_layers[2].add_sprite(lg)
    shifty1.render_update(renderer,sprite_layers,screen)

    return lg

#Updating level and Gold value
def update_lg(l_g,c_pos):
    lg=pk.load(open("./save.p","rb"))
    level=str(lg['h_level'])
    gold=str(lg['gold'])
    #getting the level and gold values from dictionary
    imgtx = Image.open('./images/level_gold.png')
    draw = ImageDraw.Draw(imgtx)
    font = ImageFont.truetype("./PAPYRUS.ttf",70)
    font2 = ImageFont.truetype("./PAPYRUS.ttf",50)
    #printing them on image
    draw.text((15,0),level,(250,250,250),font=font)
    draw.text((40,70),gold,(250,250,250),font=font2)
    imgtx.save('./images/level_gold_1.png')
    #changing the image
    l_g.image = pygame.image.load('./images/level_gold_1.png')

#creating the interface image for the special arrow
def create_interface_spec_arrow(renderer,sprite_layers,screen,c_pos):
    interface=person.create_person(c_pos[0]-700,c_pos[1]-100,'./images/spec_arrow_interf.png')
    sprite_layers[1].add_sprite(interface)
    shifty1.render_update(renderer,sprite_layers,screen)
    return interface

#creating the special arrow count interface for the dragon fight
def create_s_a(renderer,sprite_layers,screen,c_pos):
    s_a=person.create_menu_bg(c_pos[0]+500,c_pos[1]+350,'./images/spec_arrow_interf_1.png')
    sprite_layers[2].add_sprite(s_a)
    shifty1.render_update(renderer,sprite_layers,screen)

    return s_a

#updating the special arrow count interface -> SAME AS LEVEL AND GOLD INTERFACE
def update_s_a(s_a,c_pos,spec_arrow): 
    imgtx = Image.open('./images/interface_fight_1.png')
    draw = ImageDraw.Draw(imgtx)
    font = ImageFont.truetype("./PAPYRUS.ttf",50)
    spec_arrow=str(spec_arrow)
    draw.text((100,30),spec_arrow,(200,0,0),font=font)
    imgtx.save('./images/spec_arrow_interf_2.png')
    s_a.image = pygame.image.load('./images/spec_arrow_interf_2.png')

#creating the base image for weapons interface (mostly updated in fights) 
def create_interface_fight(renderer,sprite_layers,screen,c_pos):
    interface=person.create_person(c_pos[0]+312,c_pos[1]+150,'./images/interface_fight.png')
    sprite_layers[1].add_sprite(interface)
    shifty1.render_update(renderer,sprite_layers,screen)
    return interface

#creating the values for the weapon/fight interface
def create_f_i(renderer,sprite_layers,screen,c_pos):
    f_i=person.create_menu_bg(c_pos[0]+500,c_pos[1]+350,'./images/interface_fight_1.png')
    sprite_layers[2].add_sprite(f_i)
    shifty1.render_update(renderer,sprite_layers,screen)

    return f_i

#updating the weapon/fight interface
def update_f_i(f_i,c_pos):
    lg=pk.load(open("./save.p","rb"))
    ar_c=str(lg['arrow_count'])
    armor=str(lg['sheild_hp'])
    swrd_have=lg['eqp_weapon']
    #determinig the damage of the melee weapon for the interface
    if(swrd_have==None):
        sword=0
    elif(swrd_have=='dagger'):
        sword=10
    elif(swrd_have=='sw1'):
        sword=15
    elif(swrd_have=='sw2'):
        sword=20
    elif(swrd_have=='sw3'):
        sword=25
    sword=str(sword)  
    #writing the values and changing the image
    imgtx = Image.open('./images/interface_fight_1.png')
    draw = ImageDraw.Draw(imgtx)
    font = ImageFont.truetype("./PAPYRUS.ttf",50)
    draw.text((100,30),ar_c,(200,0,0),font=font)
    draw.text((100,110),armor,(200,0,0),font=font)
    draw.text((100,190),sword,(200,0,0),font=font)
    imgtx.save('./images/interface_fight_2.png')
    f_i.image = pygame.image.load('./images/interface_fight_2.png')


#creating the background of the interface for hp, cp, level and gold
def create_interface(renderer,sprite_layers,screen,c_pos):
    
    interface=person.create_person(c_pos[0]-512,c_pos[1]-384,'./images/interface1.png')
    sprite_layers[1].add_sprite(interface)
    shifty1.render_update(renderer,sprite_layers,screen)
    return interface

#creating the xp bar -> SAME AS CREATING THE HERO HP BAR
def create_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos):
    sv=pk.load(open("./save.p","rb"))
    xp=float(sv['xp'])
    xp_max=float(h(sv['h_level']))
    c_xp = xp/xp_max * 99
    c_xp=int(c_xp)
    #If xp is the image lenght will be zero and then it will be out of range and give error
    #so c_xp is made 1 [not the xp]
    if c_xp==0:
        c_xp=1
    test_image = "./images/exp_bar.png"
    original = Image.open(test_image)
    width, height = original.size
    left = 0
    top = 0
    right = c_xp
    bottom = height
    cropped_example = original.crop((left, top, right, bottom))
    cropped_example.save('./images/test_xp.png')
    sprite_layers[2].remove_sprite(xp_sprite)


    c_xp_sprite=person.create_person(c_pos[0]-400,c_pos[1]-325,'./images/test_xp.png')
    sprite_layers[2].add_sprite(c_xp_sprite)
    shifty1.render_update(renderer,sprite_layers,screen)
    pk.dump(sv,open("./save.p","wb"))
    return c_xp_sprite

#Updating the xp bar
def update_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos,xp_add):
    sv=pk.load(open("./save.p","rb"))
    #SAME AS UPDATING HERO HP BAR
    xp_old=float(sv['xp'])
    xp=float(sv['xp']+xp_add)
    level=sv['h_level'] 
    xp_max=float(h(level))
    if level>1:
        #starting the xp bar from beginning
        xp_max=float(h(level)-h(level-1))
        xp=xp-float(h(level-1))
    if xp<xp_max:
        c_xp = xp/xp_max * 99
        c_xp=int(c_xp)
        if c_xp==0:
            c_xp=1
        test_image = "./images/exp_bar.png"
        original = Image.open(test_image)
        width, height = original.size
        left = 0
        top = 0
        right = c_xp
        bottom = height
        cropped_example = original.crop((left, top, right, bottom))
        cropped_example.save('./images/test_xp.png')

        xp_sprite.image=pygame.image.load('./images/test_xp.png')
        pk.dump(sv,open("./save.p","wb"))
    #if xp exceeds the max xp required for the current level
    else:
        #level is increased
        level+= 1
        #new xp_max created 
        xp_max=float(h(level))
        #similar procedure as in other bars
        xp_max=float(h(level)-h(level-1))
        xp=sv['xp']-float(h(level-1))
        c_xp = xp/xp_max * 99
        c_xp=int(c_xp)
        if c_xp==0:
            c_xp=1
        test_image = "./images/exp_bar.png"
        original = Image.open(test_image)
        width, height = original.size
        left = 0
        top = 0
        right = c_xp
        bottom = height
        cropped_example = original.crop((left, top, right, bottom))
        cropped_example.save('./images/test_xp.png')
        #image changed
        xp_sprite.image=pygame.image.load('./images/test_xp.png')
        #new level, max_hp dumped in the dictionary
        sv['h_level']=level
        sv['max_hp']=100+(level-1)*50
        hp=sv['max_hp']
        sv['hp']=hp
        pk.dump(sv,open("./save.p","wb"))

    return level

#fuctions for decideing max xp_points for ith level: h(x) is the main
def g(x):
    if(x>1):
        res=g(x-1) + (x)*(x+1)*(5)+30
    else:
        res=(x)*(x+1)*(5)+30
    return res

def h(x):
    if x==1:
        res=g(x)
    else:
        res=30+g(x-1)
    return res

#Creating warning messages such as : "not enough gold","someting is missing" etc
#'flag' only used in "Hotel" map and "ship" map
def warning_msg(map_name,renderer,sprite_layers,screen,c_pos,flag):
    ty=pk.load(open("./save.p","rb"))
    #if gold is not enough to travel
    if (map_name=='./maps/ship.tmx' and flag==0):
        imgtx = Image.open('./images/textbox.png')
        draw = ImageDraw.Draw(imgtx)
        font = ImageFont.truetype("./PAPYRUS.ttf",30)
        draw.text((260,70),'Not enough Gold, Laddy',(0,0,0),font=font)
        imgtx.save('./images/ship_conf.png')
        ship_conf=person.create_menu_bg(c_pos[0],c_pos[1]-768/2,'./images/ship_conf.png')
        sprite_layers[2].add_sprite(ship_conf)
        shifty1.render_update(renderer,sprite_layers,screen)
        i=0
        while(i!=1):                       ##Infinite loop until menu is to be removed
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    i=1
            continue
        sprite_layers[2].remove_sprite(ship_conf)

    elif (map_name=='./maps/ship.tmx' and flag==1):
        imgtx = Image.open('./images/textbox.png')
        draw = ImageDraw.Draw(imgtx)
        font = ImageFont.truetype("./PAPYRUS.ttf",30)
        draw.text((260,70),'Gate not accessible right now',(0,0,0),font=font)
        imgtx.save('./images/ship_conf.png')
        ship_conf=person.create_menu_bg(c_pos[0],c_pos[1]-768/2,'./images/ship_conf.png')
        sprite_layers[2].add_sprite(ship_conf)
        shifty1.render_update(renderer,sprite_layers,screen)
        i=0
        while(i!=1):                       ##Infinite loop until menu is to be removed
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    i=1
            continue
        sprite_layers[2].remove_sprite(ship_conf)

    #Flag=0-> showing the first message
    elif (map_name=='./maps/hotel.tmx' and flag==0):
        imgtx = Image.open('./images/textbox.png')
        draw = ImageDraw.Draw(imgtx)
        font = ImageFont.truetype("./PAPYRUS.ttf",30)
        draw.text((260,70),'Welcome to Crossroads Inn',(0,0,0),font=font)
        draw.text((260,110),'(P)ay 50 gold, stay here and recover your health',(0,0,0),font=font)
        draw.text((260,150),'                   Bac(k)',(0,0,0),font=font)
        imgtx.save('./images/warning.png')
        warning=person.create_menu_bg(c_pos[0],c_pos[1]-768/2,'./images/warning.png')
        sprite_layers[2].add_sprite(warning)
        shifty1.render_update(renderer,sprite_layers,screen)
        i=0
        while(i!=1):
            #event handling -> P pressed-> pay 50 gold
            #                  K pressed-> go back
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_k):
                    i=1
                    #"pos" list gives the co-ordinates where the hero will be standing after talking to receptionist
                    #if pos=None -> hero's position remains same
                    pos=None
                    sprite_layers[2].remove_sprite(warning)
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_p):
                    sprite_layers[2].remove_sprite(warning)
                    #if able to pay -> pay gold, increase health -> spawn in the hotel room("pos" list)
                    if(ty['gold']>=50):
                        ty['gold']-=50
                        hero_pos_x = 200
                        hero_pos_y = 920
                        pos=[hero_pos_x,hero_pos_y]
                        ty['hp']=ty['max_hp']
                        i=1
                        pk.dump(ty,open("./save.p","wb"))
                    else :
                        #if pressed pay but dont have enough gold-> next message
                        warning_msg('./maps/hotel.tmx',renderer,sprite_layers,screen,c_pos,1)
            continue
        return pos

    #Not enough gold message for the hotel map
    elif (map_name=='./maps/hotel.tmx' and flag==1):
        imgtx = Image.open('./images/textbox.png')
        draw = ImageDraw.Draw(imgtx)
        font = ImageFont.truetype("./PAPYRUS.ttf",30)
        draw.text((260,70),'You Dont have enough money',(0,0,0),font=font)
        draw.text((260,150),'                   Bac(k)',(0,0,0),font=font)
        imgtx.save('./images/warning.png')
        warning=person.create_menu_bg(c_pos[0],c_pos[1]-768/2,'./images/warning.png')
        sprite_layers[2].add_sprite(warning)
        shifty1.render_update(renderer,sprite_layers,screen)
        i=0
        while(i!=1):
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_k):
                    i=1
            continue
        sprite_layers[2].remove_sprite(warning)

    #A common warning message to some places in the map -> pops up if the
    #condition for the message fulfilled in the parent file/function
    else:
        imgtx = Image.open('./images/textbox.png')
        draw = ImageDraw.Draw(imgtx)
        font = ImageFont.truetype("./PAPYRUS.ttf",30)
        draw.text((260,70),'Something is missing',(0,0,0),font=font)
        imgtx.save('./images/warning.png')
        warning=person.create_menu_bg(c_pos[0],c_pos[1]-768/2,'./images/warning.png')
        sprite_layers[2].add_sprite(warning)
        shifty1.render_update(renderer,sprite_layers,screen)
        return warning