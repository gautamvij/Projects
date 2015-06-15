

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
import menu
import collision
import shifty1
from PIL import Image, ImageDraw, ImageFont

try:
    import _path
except:
    pass


##THE SHOPPING MENU FUNCTION
def shop(c_pos,renderer,sprite_layers,screen,l_g):
	#variables for two while loops
	shopping = True
	inner = True
	sv=pk.load(open("./save.p","rb"))
	
	#costs of three swords
	costs1=100
	costs2=200
	costs3=300
	#cost of one arrow
	costa=5
	#cost of two armors
	costa1=100
	costa2=150
	#if discount is applicable
	if (sv['f_vil']==1):
		costs1-=30
		costs2-=50
		costs3-=70
		costa1-=30
		costa2-=50
	#list for number keys
	numkey=[pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6\
	,pygame.K_7,pygame.K_8]

	#main shopping loop
	while shopping:
		##Base image for upper and lower menu is same
		#Creating tne upper message using the base image
		imgtx = Image.open('./images/textbox.png')
		draw = ImageDraw.Draw(imgtx)
		font = ImageFont.truetype("./PAPYRUS.ttf",30)
		draw.text((270,70),'Welcome!!!',(0,0,0),font=font)
		imgtx.save('./images/shop1.png')
		## the above menu box
		shop_menu1=person.create_menu_bg(c_pos[0],c_pos[1]-768/2,'./images/shop1.png')
		
		imgtx2 = Image.open('./images/textbox.png')
		draw = ImageDraw.Draw(imgtx2)
		font = ImageFont.truetype("./PAPYRUS.ttf",30)
		draw.text((270,20),'What do you want to do?',(0,0,0),font=font)
		draw.text((350,60),'(B)uy',(0,0,0),font=font)
		draw.text((350,100),'(S)ell',(0,0,0),font=font)
		draw.text((350,140),'(L)eave',(0,0,0),font=font)
		imgtx2.save('./images/shop2.png')
		##lower menu box
		shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
		state='m'

		##states -> tell in which menu the player currently is
		#helps to navigate to next menu -> eg. "2" can be option on many menus leading to different ones
		while inner:
			#storing the gold, dagger, arrow count, and armor
			gold=sv['gold']
			sword_have=sv['dagger']
			arrow_c=sv['arrow_count']
			armr_hav=sv['sheild_first']

			##-------------------------Shopping start-------------------
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					x=event.key
					##MAIN ---> BUY
					if(x==pygame.K_b and state=='m'):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						draw.text((270,20),'What do you want to buy?',(0,0,0),font=font)
						draw.text((350,60),'Swords (1)           Armor(4)',(0,0,0),font=font)
						draw.text((350,100),'Arrow (2)           Bac(k)',(0,0,0),font=font)
						draw.text((350,140),'Repair Armor (3)',(0,0,0),font=font)						
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						#state changed to b-> buy menu
						state='b'
					##MAIN -> LEAVE
					elif(x==pygame.K_l and state=='m'):
						shopping = False
						inner=False

					##BACK TO -> MAIN -- FROM ALL
					elif(x==pygame.K_k and (state=='b' or state=='s' or state=='a' or state=='r1' \
						or state=='r2' or state=='r3' or state=='r4' or state=='arm' or\
						state=='conf' or state=='sl' or state=='ss' or state=='inv')):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						draw.text((270,20),'What do you want to do?',(0,0,0),font=font)
						draw.text((350,60),'(B)uy',(0,0,0),font=font)
						draw.text((350,100),'(S)ell',(0,0,0),font=font)
						draw.text((350,140),'(L)eave',(0,0,0),font=font)
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='m'

					##BUY -> SWORDS
					elif(x==pygame.K_1 and (state=='b')):
						sprite_layers[2].remove_sprite(shop_menu2)
						#print 'back'
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						swrd1='Longsword (1)      ' + str(costs1)
						swrd2='Two-Edged sword (2)      ' + str(costs2)
						swrd3='Katana (3)      ' + str(costs3)
						draw.text((350,20),swrd1,(0,0,0),font=font)
						draw.text((350,60),swrd2,(0,0,0),font=font)
						draw.text((350,100),swrd3,(0,0,0),font=font)
						draw.text((350,140),'Bac(k)',(0,0,0),font=font)
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='s'

					##BUY -> ARMOR
					elif(x==pygame.K_4 and (state=='b')):
						sprite_layers[2].remove_sprite(shop_menu2)
						#print 'back'
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						armr1='Leather(1)      ' + str(costa1)
						armr2='Chainmail (2)      ' + str(costa2)
						draw.text((350,20),armr1,(0,0,0),font=font)
						draw.text((350,60),armr2,(0,0,0),font=font)
						draw.text((350,140),'Bac(k)',(0,0,0),font=font)
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='arm'

					#ARMOR -> BUYING ARMOR 1
					elif(x==pygame.K_1 and (state=='arm')):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						#if able to buy
						if (gold>=costa1):
							#Check that player can always buy/keep a sword
							if (gold-costa1<100 and sword_have==0):
								draw.text((350,60),'If you Buy this you cannot buy a sword',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
							else:
								draw.text((350,20),'You bought Leather armor',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
								#if armor bought -> gold decrease, shield yes, its max hp, and total hp updated
								sv['gold']=gold-costa1
								sv['sheild_first']=1
								sv['sheild_maxhp']=60
								sv['sheild_hp']=60
								sv['eqp_armour']='lth'
								pk.dump(sv,open("./save.p","wb"))
						#insufficient gold
						else:
							draw.text((350,20),'You Dont have enough gold',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='conf'

					#ARMOR -> BUYING ARMOR 2
					elif(x==pygame.K_2 and (state=='arm')):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						if armr_hav==1:
							draw.text((350,20),'You already have an armor...',(0,0,0),font=font)
							draw.text((350,60),'First you must sell it',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						elif (gold>=costa2):
							#Check that player can always buy/keep a sword
							if (gold-costa2<100 and sword_have==0):
								draw.text((350,60),'If you Buy this you cannot buy a sword',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
							else:
								draw.text((350,20),'You bought Chainmail',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
								sv['gold']=gold-costa2
								sv['sheild_first']=1
								sv['sheild_maxhp']=70
								sv['sheild_hp']=70
								sv['eqp_armour']='chn'
								pk.dump(sv,open("./images/save.p","wb"))
						else:
							draw.text((350,20),'You Dont have enough gold',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='conf'

					#SWORDS -> BUYING SWORD 1
					#same as buying an armor
					elif(x==pygame.K_1 and (state=='s')):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						if sword_have==1:
							draw.text((350,20),'You already have a sword...',(0,0,0),font=font)
							draw.text((350,60),'First you must sell it',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						elif (gold>=costs1):
							draw.text((350,20),'You bought Longsword',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
							sv['gold']=gold-costs1
							sv['dagger']=1
							#every melee weapon have different damage -> need to update which weapon
							sv['eqp_weapon']='sw1'
							pk.dump(sv,open("./save.p","wb"))
						else:
							draw.text((350,20),'You Dont have enough gold',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='conf'

					#SWORDS -> BUYING SWORD 2
					elif(x==pygame.K_2 and (state=='s')):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						if sword_have==1:
							draw.text((350,20),'You already have a sword...',(0,0,0),font=font)
							draw.text((350,60),'First you must sell it',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						elif (gold>=costs2):
							sv['gold']=gold-costs2
							sv['dagger']=1
							sv['eqp_weapon']='sw2'
							pk.dump(sv,open("./save.p","wb"))
							draw.text((350,20),'You bought Two-Edged Sword',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
							
						else:
							draw.text((350,20),'You Dont have enough gold',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='conf'

					#SWORDS -> BUYING SWORD 3
					elif(x==pygame.K_3 and (state=='s')):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						if sword_have==1:
							draw.text((350,20),'You already have a sword...',(0,0,0),font=font)
							draw.text((350,60),'First you must sell it',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						elif (gold>=costs3):
							draw.text((350,20),'You bought Katana',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
							sv['gold']=gold-costs3
							sv['dagger']=1
							sv['eqp_weapon']='sw3'
							pk.dump(sv,open("./save.p","wb"))
						else:
							draw.text((350,20),'You Dont have enough gold',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='conf'

					#ARROWS -> BUYING ARROWS 1
					#same as armor and swords
					elif(x==pygame.K_1 and (state=='a')):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						if (gold>=costa):
							#Check that player can always buy/keep a sword
							if (gold-costa<100 and sword_have==0):
								draw.text((350,60),'If you buy this you cannot buy a sword',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
							else:
								draw.text((350,20),'You bought one arrow',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
								sv['gold']=gold-costa
								sv['arrow_count'] +=1
								pk.dump(sv,open("./save.p","wb"))
						else:
							draw.text((350,20),'You Dont have enough gold',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='conf'

					#ARROWS -> BUYING ARROWS 2 (10 arrows at price of 8)
					elif(x==pygame.K_2 and (state=='a')):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						if (gold>=costa*8):
							#Check that player can always buy/keep a sword
							if ((gold-(costa*8))<100 and sword_have==0):
								draw.text((350,60),'If you Buy this you cannot buy a sword',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
							else:
								draw.text((350,20),'You bought a big arrow pock',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
								sv['gold']=gold-(costa*8)
								sv['arrow_count'] +=10
								pk.dump(sv,open("./save.p","wb"))
						else:
							draw.text((350,20),'You Dont have enough gold',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='conf'

					#ARROWS -> BUYING ARROWS 3 (20 arrows at price of 18)
					elif(x==pygame.K_3 and (state=='a')):
						sprite_layers[2].remove_sprite(shop_menu2)
						#print 'back'
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						if (gold>=costa*18):
							#Check that player can always buy/keep a sword
							if ((gold-(costa*18))<100 and sword_have==0):
								draw.text((350,60),'If you Buy this you cannot buy a sword',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
							else:
								draw.text((350,20),'You bought a huge arrow pack',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
								sv['gold']=gold-(costa*18)
								sv['arrow_count'] +=20
								pk.dump(sv,open("./save.p","wb"))
						else:
							draw.text((350,20),'You Dont have enough gold',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='conf'

					#BUY -> ARROWS
					elif(x==pygame.K_2 and (state=='b')):
						sprite_layers[2].remove_sprite(shop_menu2)
						#print 'back'
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						draw.text((350,20),'Buy arrow (1)      5 Gold',(0,0,0),font=font)
						draw.text((350,60),'Buy 10 arrows (2)      40 Gold',(0,0,0),font=font)
						draw.text((350,100),'Buy 20 arrows (3)      90 Gold',(0,0,0),font=font)
						draw.text((350,140),'Bac(k)',(0,0,0),font=font)
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='a'

					#BUY TO REPAIR ARMOR (condition -> armor health ful )
					elif(x==pygame.K_3 and (state=='b') and sv['sheild_first']==1\
					and sv['sheild_hp']==sv['sheild_maxhp']):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						draw.text((350,20),'Your armor is already at full health',(0,0,0),font=font)
						draw.text((350,140),'Bac(k)',(0,0,0),font=font)
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='r1'

					#BUY TO REPAIR ARMOR (condition -> armor health not full)
					elif(x==pygame.K_3 and (state=='b') and sv['sheild_first']==1\
					and sv['sheild_hp']<['sheild_maxhp']):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						draw.text((350,20),'(R)epair armor      30 Gold',(0,0,0),font=font)
						draw.text((350,140),'Back',(0,0,0),font=font)
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='r2'

					#BUY TO REPAIR ARMOR (condition -> no armor )
					elif(x==pygame.K_3 and (state=='b') and sv['sheild_first']==0):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						draw.text((350,20),'You have no armor to repair',(0,0,0),font=font)
						draw.text((350,140),'Bac(k)',(0,0,0),font=font)
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='r4'

					#REPAIR ARMOR -> NEXT (condition -> armr health not full )
					elif(x==pygame.K_r and (state=='r2')):
						sprite_layers[2].remove_sprite(shop_menu2)
						#if able to pay
						#Check that player can always buy/keep a sword
						if gold>=30:
							if (gold-30<100 and sword_have==0):
								draw.text((350,60),'If you repair this you cannot buy a sword',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
							else:
								sv['gold']=gold-30
								sv['sheild_hp']=50
								pk.dump(sv,open("./save.p","wb"))
								imgtx2 = Image.open('./images/textbox.png')
								draw = ImageDraw.Draw(imgtx2)
								font = ImageFont.truetype("./PAPYRUS.ttf",30)
								draw.text((350,20),'Your Armor is repaired',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								imgtx2.save('./images/shop2.png')
						#insufficient gold
						else:
							draw.text((350,20),'You Dont have enough gold',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
							imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='r3'

					#MAIN -> SELL
					elif(x==pygame.K_s and state=='m'):
						sprite_layers[2].remove_sprite(shop_menu2)
						#print 'menu'
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						draw.text((270,20),'What do you want to sell?',(0,0,0),font=font)
						draw.text((350,60),'Swords (1)',(0,0,0),font=font)
						draw.text((350,100),'From Inventory (2)',(0,0,0),font=font)
						draw.text((350,160),'Bac(k)',(0,0,0),font=font)
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='sl'

					#SELL -> SWORD
					elif(x==pygame.K_1 and state=='sl'):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						draw.text((350,60),'Sell your Sword (1)',(0,0,0),font=font)
						draw.text((350,150),'Bac(k)',(0,0,0),font=font)
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='ss'

					#SELL SWORD -> NEXT
					elif(x==pygame.K_1 and state=='ss'):
						wpn=sv['eqp_weapon']
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						#if have no sword
						if wpn==None:
							draw.text((350,60),'You Dont have any sword',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
						#if have sword
						#Check that player can always buy/keep a sword
						elif((gold+costs1-30)<100):
							draw.text((350,60),'If you sell this you cannot buy another one',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
						else:
							if wpn=='sw1':
								sv['gold']=gold+costs1-30
							elif wpn=='sw2':
								sv['gold']=gold+costs2-60
							elif wpn=='sw2':
								sv['gold']=gold+costs3-120
							elif wpn=='dagger':
								sv['gold']=gold+50
							sv['eqp_weapon']=None
							sv['dagger']=0
							pk.dump(sv,open("./save.p","wb"))
							wpn='You sold '+wpn
							draw.text((350,60),wpn,(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='conf'

					#SELL -> SELL FROM INVENTORY
					elif(x==pygame.K_2 and state=='sl'):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)

						inv_len=len(sv['misc'])
						#inventory empty
						if inv_len==0:
							draw.text((350,60),'You dont have anything to sell',(0,0,0),font=font)
							draw.text((350,140),'Bac(k)',(0,0,0),font=font)
						#Creating the text to show up
						else:
							inven=sv['misc']
							inven_item=[]#item names
							inven_cost=[]#item cost
							inven_str=[]#list for their concat string
							for i in range(0,inv_len,2):
								inven_item.append(inven[i])
								inven_cost.append(inven[i+1])

							#concatinating (along with "Back")
							for i in range(0,inv_len/2):	
								inven_list=inven_item[i]+'   '+str(inven_cost[i])+' ('+str(i+1)+')'
								inven_str.append(inven_list)
							inven_str.append('Bac(k)')

							#snippet for printing in two rows
							for j in range(20,150,40):
								if (len(inven_str))!=0:
									draw.text((350,j),inven_str[0],(0,0,0),font=font)
									inven_str.pop(0)
								else:
									break

							for j in range(20,150,40):
								if (len(inven_str))!=0:
									draw.text((700,j),inven_str[0],(0,0,0),font=font)
									inven_str.pop(0)
								else:
									break

						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='inv'

					#selecting item to sell from inventory
					elif(x in numkey and state=='inv'):
						sprite_layers[2].remove_sprite(shop_menu2)
						imgtx2 = Image.open('./images/textbox.png')
						draw = ImageDraw.Draw(imgtx2)
						font = ImageFont.truetype("./PAPYRUS.ttf",30)
						inv_len=len(sv['misc'])
						inven=sv['misc']
						#creation of concat string list
						inven_item=[]
						inven_cost=[]
						inven_str=[]
						for i in range(0,inv_len,2):
							inven_item.append(inven[i])
							inven_cost.append(inven[i+1])

						for i in range(0,inv_len/2):
							if int (chr(x))==i+1:
								item_str='You sold '+inven_item[i]
								#adding the gold to hero's gold
								sv['gold']=gold+inven_cost[i]
								#Poping the sold item
								sv['misc'].pop(i*2)
								sv['misc'].pop(i*2)
								draw.text((350,60),item_str,(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
								pk.dump(sv,open("./save.p","wb"))
							elif int(chr(x))>inv_len/2:
								draw.text((350,60),'Not that many items here',(0,0,0),font=font)
								draw.text((350,140),'Bac(k)',(0,0,0),font=font)
						imgtx2.save('./images/shop2.png')
						shop_menu2=person.create_menu_bg(c_pos[0],c_pos[1]+768/2-270,'./images/shop2.png')
						state='conf'

				#updating the gold interface
				menu.update_lg(l_g,c_pos)
				#removing all the sprites and adding the fresh ones
				sprite_layers[2].remove_sprite(shop_menu1)
				sprite_layers[2].remove_sprite(shop_menu2)
				sprite_layers[2].add_sprite(shop_menu1)
				sprite_layers[2].add_sprite(shop_menu2)
				#rendering
				shifty1.render_update(renderer,sprite_layers,screen)


		if shopping==False:
			#removing the sprites when leaving
			sprite_layers[2].remove_sprite(shop_menu1)
			sprite_layers[2].remove_sprite(shop_menu2)
			shifty1.render_update(renderer,sprite_layers,screen)