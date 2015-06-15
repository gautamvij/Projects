

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
import tunnel3
from shop_gui import *
from PIL import Image, ImageDraw, ImageFont
import camra
import sound
import goodtunnel
import climb_mountain
import maze_code
import maze_code2
import knifehouse1
import fish
import hotel
import spooky
import tunnel2_4
import pal_lava
import palace

try:
    import _path
except:
    pass

def demo_pygame(file_name,frm):
   
    ##FILE NAME GIVES THE CURRENT MAP
    if(file_name=='./maps/tunnel3.tmx'):
        tunnel3.main()
    elif(file_name=='./maps/tunnel.tmx'):
        goodtunnel.main()
    elif(file_name=='./maps/mountainclimbing.tmx'):
        climb_mountain.main()
    elif(file_name=='./maps/maze.tmx'):
        maze_code.main()
    elif(file_name=='./maps/maze2.tmx'):
        maze_code2.main()
    elif(file_name=='./maps/hotel.tmx'):
        hotel.main()
    elif(file_name=='./maps/tunnel2_4.tmx'):
        tunnel2_4.main(frm)
    elif(file_name=='./maps/palace.tmx'):
        pal_lava.main()
    elif(file_name=='./maps/palace_final.tmx'):
        palace.main()
    

    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    # init pygame and set up a screen
    pygame.display.set_caption("tiledtmxloader - " + file_name + \
                                                        " - keys: arrows, 0-9")
    screen_width = min(1024, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load the images using pygame
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    # prepare map rendering
    assert world_map.orientation == "orthogonal"

    # renderer
    renderer = tiledtmxloader.helperspygame.RendererPygame()


    #loading the main dictionary into "savegame"
    #pk.dump(savegame,open("./save.p","wb")) -> donates dumping/saving the updated
    #dictionaty "savegame" to the "save.p" file so that can be used again with the updated values
    savegame=pk.load(open("./save.p","rb"))

    ##Creating hero
    #getting the entry position depending on the map 
    starting = entry(file_name,frm)
    hero_pos_x = starting[0]
    hero_pos_y = starting[1]
    #creating the hero sprite 
    hero = person.create_person(hero_pos_x, hero_pos_y,'./images/hero_d2.png')
    
    ##Creating villagers
    #villager count is 0 if no villager on the current map
    vcount=0
    #defining the villager directions
    muv='up'
    mdv='down'
    mrv='right'
    mlv='left'
    #no direction -> not moving
    no=''
    #creating the villager sprites
    #villagers created according to map
    vil=person.create_villager(file_name)
    vcount=len(vil)
    ##Giving initial random direction to every villager
    #initializing the variable
    drc=no
    #the villager direction list
    drctn = []
    #using randint to decide direction
    for i in range(0,vcount):
        a=random.randint(1,10)
        if(a==1):
            drc=muv
        elif(a==2):
            drc=mrv
        elif(a==3):
            drc=mdv
        elif(a==4):
            drc=mlv
        elif (a<=10):
            drc=no

        drctn.append(drc)


    # cam_offset is for scrolling
    cam_world_pos_x = hero.rect.centerx
    cam_world_pos_y = hero.rect.centery

    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height)

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    # filter layers
    sprite_layers = [layer for layer in sprite_layers if not layer.is_object_group]

    # add the hero the the right layer, it can be changed using 0-9 keys
    sprite_layers[1].add_sprite(hero)
    
    ##Adding the villager sprites
    i=0
    for i in range(0,vcount):
        sprite_layers[1].add_sprite(vil[i]['sprte'])

    ##Misc object sprites
    #creating the sprite
    misc=person.create_misc(file_name)
    #adding the sprites
    if misc!=None:
        mcount=len(misc)
        i=0
        while(i>=0 and i<mcount):
            ##check if any misc is already taken
            if (savegame[misc[i]['name']]==0):                
                sprite_layers[1].add_sprite(misc[i]['sprte'])
                i+=1
            else:
                misc.pop(i)
                mcount=len(misc)

    # variables for the main loop
    clock = pygame.time.Clock()
    running = True
    speed = 4

    ##Sign board for the tunnel riddle
    portal_board=None
    if(file_name=='./maps/village1.tmx'):
        portal_board=pygame.Rect(81*32,9*32,40,80)
        signboard=person.create_person(81*32,9*32,'./images/signboard.png')
        sprite_layers[2].add_sprite(signboard)

    ##The variables for changing the movement pictures -> to give animation to movement
    mr=ml=md=mu=0
    vmr=vml=vmd=vmu=0

    # set up timer for fps printing
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    #Creating portals -> For map changing
    portals = person.create_portal(file_name)
    #Creating the shopping portal
    shop_portal=person.create_shop_portal(file_name)

    #Variable for the quests/tasks/side missions
    villager_job=0
    #To check if ship is on the shore in "Ship.tmx" map (pirate ship)
    ship_present=0
    #Initial value of portal -> if True -> map changes
    portal=False
    #check for the river sound in Burning village map -> heard only if close to river
    flag_crossed=0
    #This is check for talking to villager -> talks to villager-> shows the first dialog box-> if 1
    count=0


    ###FOR INTERFACE
    #initiaizing variables from savegame
    hp=savegame['hp']
    hp_max=savegame['max_hp']
    #camera postion stored in c_pos
    c_pos=camra.camera(file_name,renderer,hero)
    #variable for turning the interface on and off       
    interf_toggle=0
    #creating the background for health bar, xp bar
    interface=menu.create_interface(renderer,sprite_layers,screen,c_pos)
    #creating the health bar sprite and creating the bar
    hp_sprite=person.create_person(c_pos[0],c_pos[1],'./images/hp_bar.png')
    [hp_sprite,hp]=menu.create_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos)
    #creating the xp bar sprite and creating the bar
    xp_sprite=person.create_person(c_pos[0],c_pos[1],'./images/exp_bar.png')
    xp_sprite=menu.create_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos)
    #creating the level and gold sprite
    l_g=menu.create_l_g(renderer,sprite_layers,screen,c_pos)
    #creating the weapons interface background and values
    f_i=menu.create_f_i(renderer,sprite_layers,screen,c_pos)
    interf_fight=menu.create_interface_fight(renderer,sprite_layers,screen,c_pos)



    ##Aditional background music that turns onn and off
    add=None
    #Creating the main background music
    musicbg=sound.create_music(file_name)
    
    #Creating the additional full time running background music
    if file_name=='./maps/village2_out1.tmx':
        music_add=sound.create_music_add('./sounds/vil2add.ogg')
    

#---------------------------------------
    """MAIN  GAME LOOP"""
    while running:
        #fixing the FPS
        dt = clock.tick(50)

        ##Checking for map exit -> -1 no change -> !=-1 Specific portal number
        change_map = exit_map(hero,portals)
        if change_map!=-1:
            portal = True
            #Giving the nextmap's name and frm -> "frm"-> tells if the player came from which map
            # -> to give the respective starting position 
            nextlevel=next_map(file_name,change_map)
            


            ##Giving the warning messages wherever needed
            #In Ship map -> warning for not enough gold
            if (file_name=='./maps/ship.tmx' and (savegame['pirate']==0 or savegame['pirate_map']==1)):
                portal=False
                warning=menu.warning_msg(file_name,renderer,sprite_layers,screen,c_pos,1)
                ##Infinite loop until menu is to be removed
                i=0
                while(i!=1):
                    for event in pygame.event.get():
                        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                            i=1
                    continue
                sprite_layers[2].remove_sprite(warning)
                hero_pos_x -=10
            #In burning village map -> "Something is missing" if player do not have a melee weapon
            elif(file_name=='./maps/village1.tmx' and savegame['dagger']==0):
                portal=False
                warning=menu.warning_msg(file_name,renderer,sprite_layers,screen,c_pos,0)
                ##Infinite loop until menu is to be removed
                i=0
                while(i!=1):
                    for event in pygame.event.get():
                        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                            i=1
                    continue
                sprite_layers[2].remove_sprite(warning)
                hero_pos_y +=10
            #In village2 inside -> "Something is missing" if no melee weapon or not talked to the spooky guy
            elif(file_name=='./maps/village2_inside.tmx' and (savegame['eqp_weapon']==None or savegame['spook']==0) and (change_map==1 or change_map==2)):
                portal=False
                warning=menu.warning_msg(file_name,renderer,sprite_layers,screen,c_pos,0)
                ##Infinite loop until menu is to be removed
                i=0
                while(i!=1):
                    for event in pygame.event.get():
                        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                            i=1
                    continue
                sprite_layers[2].remove_sprite(warning)
                hero_pos_y +=10
            
            
        #Quit the while loop if portal is true
        if portal==True:
            running=False

        ##loading the main dictionary into "savegame"
        savegame=pk.load(open("./save.p","rb"))
        
        #Getting the current camera position
        c_pos=camra.camera(file_name,renderer,hero)
               
        ##IN Ship map to move the ship when hreo reaches a certain point
        if(file_name=='./maps/ship.tmx' and hero_pos_x>14*32 and ship_present==0):
            #Creating the addtional bg music (which continues once started)
            music_add=sound.create_music_add('./sounds/pirate.ogg')
            music_add.set_volume(0.7)

            ship_moving = True
            #Creating the Ship sprite and adding it
            ship=person.create_person(9*32,29*32,'./images/ship.png')
            sprite_layers[1].add_sprite(ship)
            #while function for the ship moving
            while(ship_moving):
                #moving the ship
                ship.rect.top -=1
                #rendering the screen to keep the screen updated
                render_update(renderer,sprite_layers,screen)
                #Stopping the ship
                if(ship.rect.top<7*32):
                    #Ship reached the shore
                    ship_present=1
                    i=0
                    while(i!=30):
                        i=i+1
                        continue
                    #changing to second image
                    ship.image=pygame.image.load('./images/ship2.png')
                    render_update(renderer,sprite_layers,screen)
                    ##adding some delay to ship image change
                    while(i!=60):
                        i=i+1
                        continue
                    #changing to third image and 
                    ship.image=pygame.image.load('./images/ship3.png')
                    ship.rect.top=4*32
                    ship.rect.right += 32
                    #Coming out of while loop
                    ship_moving=False
                    #Creating the Captian as villger in the format in which other villagers are added in person file
                    vil=[{'sprte':person.create_person(5*32,5*32-16,'./images/cappy.png'),\
                    'toplx':None,'toply':None,'w':None,'h':None}]
                    #adding the Captian
                    sprite_layers[1].add_sprite(vil[0]['sprte'])


        ##MOVING THE HERO
        mov = movements.hero_move(mr,ml,md,mu,hero_pos_x,hero_pos_y,hero,speed,sprite_layers,vil,misc)
        #The variables for the animation images returned from the movement fucntion
        #Then the same variables are passed again to keep the animation smoother
        mr = mov[0]
        ml = mov[1]
        md = mov[2]
        mu = mov[3]
        #position variables -> called and passed again
        hero_pos_x = mov[4]
        hero_pos_y = mov[5]
        #hypothetical rectagle -> where the hero will move next?
        #used to check collision against villagers
        hero_hypo = mov[7]



        
        #Additional bg music (on/off)
        if (file_name=='./maps/village1.tmx' and hero_pos_y<=28*32 and flag_crossed==0):
            add=sound.create_music_add('./sounds/river.ogg')
            ##to check wether first time crossed or other
            flag_crossed=1

        elif (file_name=='./maps/village1.tmx' and hero_pos_y>=28*32 and flag_crossed==1):
            sound.stop_soundfx(add)
            flag_crossed=0







        ##Moving the villager if there is one
        if (vil!=None):
            ##Moving the villager -> the function gives the old direction in which the villagers were
            ##travelling. In every loop they take one step
            drctn=movements.move_villager(drctn,speed,vil,hero_hypo,vmu,vmr,vmd,vml,file_name)
            
            ##Gives the index of colliding vilager 
            coll=movements.colliding_other_living(vil,hero_hypo)    
        
        #Checking if there is any misc
        elif(misc!=None):
            collm=movements.colliding_other_living(misc,hero_hypo)


        #Moving the interface with camera
        interface.rect.topleft=(c_pos[0]-512,c_pos[1]-384)
        hp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-382)
        xp_sprite.rect.topleft=(c_pos[0]-400,c_pos[1]-345)
        l_g.rect.topleft=(c_pos[0]-508,c_pos[1]-381)
        f_i.rect.bottomright=(c_pos[0]+500,c_pos[1]+350)
        interf_fight.rect.bottomright=(c_pos[0]+512,c_pos[1]+384)
      
#-------------------------- EVENT HANDLING ---------------------------------
        for event in pygame.event.get():
            #Updating the interface whenever an event happens
            menu.update_lg(l_g,c_pos)
            menu.update_hp_bar(renderer,sprite_layers,screen,hp_sprite,c_pos,0)
            menu.update_xp_bar(renderer,sprite_layers,screen,xp_sprite,c_pos,0)
            menu.update_f_i(f_i,c_pos)

            #For Key pressed event
            if event.type == pygame.KEYDOWN:
                x=event.key

                if(x==pygame.K_ESCAPE):
                    pygame.quit()

                #Saving the game
                elif(x==pygame.K_s):
                    #saving the present file name
                    savegame['last_map']=file_name
                    #saving the present frm-> where to put the hero when game loaded
                    savegame['last_frm']=frm
                    #to allow the load game function to work
                    savegame['save']=1
                    pk.dump(savegame,open("./save.p","wb"))
                    sv=menu.save_menu(c_pos)
                    sound.create_soundfx('./sounds/savegame.ogg')
                    sprite_layers[2].add_sprite(sv)
                    render_update(renderer,sprite_layers,screen)
                    menu.exit_menu(x)
                    sprite_layers[2].remove_sprite(sv)

                #Printing the dictionary
                elif(x==pygame.K_q):
                    print savegame
            

                #Starting the shopping interface
                elif(x==pygame.K_SPACE and shop_portal!=None and pygame.Rect.colliderect(hero.rect, shop_portal)):
                    shop(c_pos,renderer,sprite_layers,screen,l_g)

                #Showing the tunnel riddle
                elif(x==pygame.K_SPACE and portal_board!=None and pygame.Rect.colliderect(hero.rect, portal_board)):
                    riddle=person.create_person(hero.rect.centerx,hero.rect.centery+200,'./images/tunnel_riddle.png')
                    sprite_layers[2].add_sprite(riddle)
                    (renderer,sprite_layers,screen) = render_update(renderer,sprite_layers,screen)
                    ##Infinite loop until menu is to be removed
                    i=0
                    while(i!=1):
                        for event in pygame.event.get():
                            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                                i=1
                        continue
                    sprite_layers[2].remove_sprite(riddle)

                ##Showing the Travel option of the ship
                elif(file_name=='./maps/ship.tmx' and ship_present==1 and x==pygame.K_SPACE and collision.checkCollision(hero,ship)):
                    #creating the menu
                    imgtx = Image.open('./images/textbox.png')
                    draw = ImageDraw.Draw(imgtx)
                    font = ImageFont.truetype("./PAPYRUS.ttf",30)
                    draw.text((260,70),'Are you sure you want to travel?',(0,0,0),font=font)
                    draw.text((260,110),'(Y)es         (N)o',(0,0,0),font=font)
                    imgtx.save('./images/ship_conf.png')
                    ship_conf=person.create_menu_bg(c_pos[0],c_pos[1]-768/2,'./images/ship_conf.png')
                    sprite_layers[2].add_sprite(ship_conf)
                    render_update(renderer,sprite_layers,screen)
                    ##Infinite loop until menu is to be removed
                    result='x'
                    while(result=='x'):
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                x=event.key
                                if(x==pygame.K_y):
                                    result='y'
                                else:
                                    result='n'
                                    break
                    sprite_layers[2].remove_sprite(ship_conf)
                    render_update(renderer,sprite_layers,screen)
                    #Checking the conditions if pressed 'y' -> want to travel
                    if(result=='y'):
                        #condition for job done and then gold does not matter
                        if(savegame['talk_vil']['./maps/ship.tmx'][0]==1):
                            pirate_mapchange=1
                            running =False
                        #condition for job not done but have gold
                        elif(savegame['gold']>=50):
                            savegame['gold']-=50
                            pk.dump(savegame,open("./save.p","wb"))
                            pirate_mapchange=1
                            running =False
                        #condition for job not done and not enough gold
                        elif(savegame['gold']<50 and savegame['pirate_map']==0):
                            menu.warning_msg(file_name,renderer,sprite_layers,screen,c_pos,0)
                            break

                #Key pressed near a collectable object
                elif(x==pygame.K_SPACE and misc!=None):
                    i=0
                    l=len(misc)
                    while (i>=0 and i<l):
                        if pygame.Rect.colliderect(hero.rect, misc[i]['sprte'].rect):
                            savegame['misc'].append(misc[i]['name'])
                            savegame['misc'].append(misc[i]['value'])
                            savegame[misc[i]['name']]=1
                            pk.dump(savegame,open("./save.p","wb"))
                            sprite_layers[1].remove_sprite(misc[i]['sprte'])
                            misc.pop(i)
                        else: i+=1
                        l=len(misc)

                #toggling the interface off
                elif(x==pygame.K_f and interf_toggle==0):
                    sprite_layers[2].remove_sprite(hp_sprite)
                    sprite_layers[2].remove_sprite(xp_sprite)
                    sprite_layers[1].remove_sprite(interface)
                    sprite_layers[2].remove_sprite(l_g)
                    sprite_layers[1].remove_sprite(interf_fight)
                    sprite_layers[2].remove_sprite(f_i)
                    interf_toggle=1

                #toggling the interface on
                elif(x==pygame.K_f and interf_toggle==1):
                    sprite_layers[2].add_sprite(hp_sprite)
                    sprite_layers[2].add_sprite(xp_sprite)
                    sprite_layers[1].add_sprite(interface)
                    sprite_layers[2].add_sprite(l_g)
                    sprite_layers[1].add_sprite(interf_fight)
                    sprite_layers[2].add_sprite(f_i)
                    interf_toggle=0

                ##Making the Inventory
                elif(x==pygame.K_i):
                    sound.create_soundfx('./sounds/inventory.ogg')
                    inven=menu.create_menu_inventory(c_pos)
                    sprite_layers[2].add_sprite(inven)
                    render_update(renderer,sprite_layers,screen)
                    ##Infinite loop until inventory is to be removed
                    while(x!=pygame.K_SPACE):
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                x=event.key
                        continue
                    sprite_layers[2].remove_sprite(inven)
                    render_update(renderer,sprite_layers,screen)


                #------------------TALKING TO VILLAGER------------------
                #Give the required values for showing the talk to villager number 'coll' (line 394)
                if (vil!=None):
                    talk_result=talk.iftalk(coll,x,vil,count,hero_pos_x,hero_pos_y,file_name)##Gives : count(for checking if talking)
                                                                                        ##coll (which villager he's talking to)
                                                                                      ##talktime(talking again or not)
                #if no villager colliding                                                                            
                else:
                    talk_result=None

                #talk_result[0] -> count --- shows the talking interface only if count is 1-> talking to someone
                #count remains 0 as called before mainloop
                if(talk_result[0]==1):
                    ##gives back the text for respective villager
                    menutext=menu.create_menu_vil(coll,file_name,talk_result[2])
                    ##variable to check for for how many number of times the loop should work
                    dialog_show=0
                    sound.create_soundfx('./sounds/talk.ogg')
                    ##gives the name of the created image
                    txtim=person.create_text_img('./images/textbox.png',menutext,dialog_show)
                    ##gives the sprite for the menu image
                    menu_ui=person.create_menu_bg(c_pos[0],c_pos[1]-768/2,txtim)
                    sprite_layers[2].add_sprite(menu_ui)
                    render_update(renderer,sprite_layers,screen)

                    #the loop for showing text box (again and again)
                    while(dialog_show<len(menutext)):
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                x=event.key
                                #for the villagers that have Yes/No option
                                if (dialog_show==len(menutext)-1):
                                    if x==pygame.K_y:
                                        if(file_name=='./maps/village1.tmx' and coll==1 and savegame['b_h_vil']==0):
                                            #sound created as this 'add' variable is closing when going out of village1
                                            #main reason -> prevent error
                                            add=sound.create_music_add('./sounds/river.ogg')
                                            savegame['b_h_vil']=1
                                            villager_job=1
                                            running =False
                                            sprite_layers[2].remove_sprite(menu_ui)  
                                            dialog_show+=1
                                        elif(file_name=='./maps/village2_out1.tmx' and coll==0 and savegame['f_vil']==0):
                                            savegame['f_vil']=1
                                            villager_job=2
                                            running =False
                                            sprite_layers[2].remove_sprite(menu_ui)  
                                            dialog_show+=1
                                        elif(file_name=='./maps/village2_inside.tmx' and coll==2 and savegame['spook']==0):
                                            savegame['spook']=1
                                            villager_job=3
                                            running =False
                                            sprite_layers[2].remove_sprite(menu_ui)  
                                            dialog_show+=1
                                    elif x==pygame.K_n:
                                        sprite_layers[2].remove_sprite(menu_ui)  
                                        dialog_show+=1
                                #all other villagers
                                if(x==pygame.K_SPACE):
                                    ##remove the prev text image
                                    sprite_layers[2].remove_sprite(menu_ui)
                                    ##indicates for the next one
                                    dialog_show +=1
                                    ##for not going in the loop again
                                    if dialog_show==len(menutext):                      
                                        break
                                ##if any other key pressed
                                elif(x!=pygame.K_SPACE):
                                    continue
                                ##for not going in the loop again
                                elif dialog_show==len(menutext):
                                    break
                                sound.create_soundfx('./sounds/talk.ogg')
                                #next text image created and its sprite created and added
                                txtim=person.create_text_img('./images/textbox.png',menutext, \
                                                             dialog_show)
                                menu_ui=person.create_menu_bg(c_pos[0],c_pos[1]-768/2,\
                                              txtim)
                                
                                sprite_layers[2].add_sprite(menu_ui)
                        render_update(renderer,sprite_layers,screen)
                    if x==pygame.K_SPACE:
                        ##an infite loop till 'x' is pressed
                        menu.exit_menu(x)
                    sprite_layers[2].remove_sprite(menu_ui)
                    #--------------------TALKING ENDS-------------------

#----------------------------- EVENT HANDLING ENDED ----------------------------

        # adjust camera according to the hero's position, follow him
        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0, 0, 0))

        # render the map
        for sprite_layer in sprite_layers:
            if sprite_layer.is_object_group:
                continue
            else:
                renderer.render_layer(screen, sprite_layer)
        pygame.display.flip()

    """------------------------------------- OUT OF MAIN GAME LOOP----------------------------------"""

    #stopping the additional background music
    if (file_name=='./maps/village2_out1.tmx' or file_name=='./maps/ship.tmx'):
        music_add.stop()
    #stopping the fluctuating bg music
    #'add' created (in line 585) to prevent error in this snippet
    if(file_name=='./maps/village1.tmx' ):
        sound.stop_soundfx(add)
    musicbg.stop()

    #If portal was the reason for stopping the game loop
    if portal==True:
        #name of next map and respective frm
        mp=nextlevel[0]
        frm=nextlevel[1]
        #calling the map
        demo_pygame(mp,frm)

    #If main loop ended because of a side task
    if villager_job==1:
        knifehouse1.main()
    elif villager_job==2:
        fish.main()
    elif villager_job==3:
        spooky.main()

    #when pressed 'yes' to the ship travel
    if pirate_mapchange==1:
        demo_pygame('./maps/village2_out1.tmx',0)

   
#-------------------------------------------

#function to render and update the screen
def render_update(renderer,sprite_layers,screen):
    for sprite_layer in sprite_layers:
        if sprite_layer.is_object_group:
            continue
        else:
            renderer.render_layer(screen,sprite_layer)
    pygame.display.flip()
    return (renderer,sprite_layers,screen)
