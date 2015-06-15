import cPickle as pk

try:
    import _path
except:
    pass

init_dict = {#variable for checking if there is a save game
		'save':0,\
		# hit points(health) of the hero 
		'hp':100.0,\
		#maximum hp allowed
		'max_hp':100.0,\
		#the current level of the hero
		'h_level':1,\
		#if hero is having a weapon or not -0/1
		'dagger':0,\
		#if hero is having a sheild or not -0/1
		'sheild_first':0,\
		#if hero is having a bow and arrow
             'bow_arrow_first':0,\
             #number of arrows
             'arrow_count':0,\
             #armor hitt points
             'sheild_hp':0,\
             #maximum armour hp
             'sheild_maxhp':50,\
             #experience points of the hero
             'xp':0,\
             #current gold hero is having
             'gold':0,\
             #the collectables that the hero is carrying
             'misc':[],\
             #if dagger =1 -> which one is hero carrying -> 4 melee weapons in game
             'eqp_weapon':None,\
             #which armor is hero wearing -> 3 types of armor
             'eqp_armour':None,\
             #when game saved -> the current map is stored here
             'last_map':None,\
             #when game saved this saves the index of the portal from where the hero enterd
             #the map -> when game loads -> hero starting pos is same is the starting pos when game was saved	
             'last_frm':0,\
             #if the burning house task is done or not -0/1
             'b_h_vil':0,\
             #if the fishing task is done or not -0/1
             'f_vil':0,\
             #talked to pirate or not -> if scroll taken then only talk will change
             'pirate_vil':0,\
             #if talked to pirate once -> will open the portal to go to scrol task
             'pirate':0,\
             #if the scroll task is done or not -0/1 
             'pirate_map':0,\
             #if talked to the spooky guy or not -0/1
             'spook':0,\
             #so that hero may not get infinite gold by going intunnel again n again -0/1
             'flagtreasure':[0,0,0,0,0,0,0,0,0,0],\
             #so that hero may not get food/treasure again and again in hotel -0/1
             'hotel_treasure':[0,0,0,0],\
             #misc objects check -> taken or not
             'boots':0,\
             'fish_rod':0,\
             'locket':0,\
             'book':0,\
             'rose':0,\
             'lamp':0,\
             #if the hero has talked to a villager in particulat map -0/1
             'talk_vil':dict([('./maps/village2_out1.tmx',[0]),('./maps/village2_inside.tmx',[0,0,0,0,0,0,0]),('./maps/village1.tmx',[0,0,0]),\
               	('./maps/spooky.tmx',[0]),('./maps/ship.tmx',[0])])}

pk.dump(init_dict,open("./newgame.p","wb"))