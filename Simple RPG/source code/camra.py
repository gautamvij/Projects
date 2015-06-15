##Camera control for every map
def camera(map_name, renderer, hero):
	if map_name=='./maps/village1.tmx':
		cam_pos_x = hero.rect.centerx
		cam_pos_y = hero.rect.centery
		if hero.rect.centerx <= 519 :
			cam_pos_x = 519
		elif hero.rect.centerx >=2679:
			cam_pos_x = 2679
		if hero.rect.centery >= 2100:
			cam_pos_y = 2100
		elif hero.rect.centery <=407:
			cam_pos_y = 407
		renderer.set_camera_position(cam_pos_x,cam_pos_y)

		return [cam_pos_x,cam_pos_y]

	elif map_name=='./maps/village2_out1.tmx':
		cam_pos_x = hero.rect.centerx
		cam_pos_y = hero.rect.centery
		if hero.rect.centerx <= 512 :
			cam_pos_x = 512
		elif hero.rect.centerx >=1404:
			cam_pos_x = 1404
		if hero.rect.centery >= 560:
			cam_pos_y = 560
		elif hero.rect.centery <=405:
			cam_pos_y = 405
		renderer.set_camera_position(cam_pos_x,cam_pos_y)

		return [cam_pos_x,cam_pos_y]

	elif map_name=='./maps/village2_inside.tmx':
		cam_pos_x = hero.rect.centerx
		cam_pos_y = hero.rect.centery
		if hero.rect.centerx <= 516 :
			cam_pos_x = 516
		elif hero.rect.centerx >=892:
			cam_pos_x = 892
		if hero.rect.centery >= 1458:
			cam_pos_y = 1458
		elif hero.rect.centery <=408:
			cam_pos_y = 408
		renderer.set_camera_position(cam_pos_x,cam_pos_y)

		return [cam_pos_x,cam_pos_y]

	elif map_name=='./maps/ship.tmx':
		cam_pos_x = hero.rect.centerx
		cam_pos_y = hero.rect.centery
		if hero.rect.centerx <= 514 :
			cam_pos_x = 514
		elif hero.rect.centerx >=1404:
			cam_pos_x = 1404
		if hero.rect.centery >= 588:
			cam_pos_y = 588
		elif hero.rect.centery <=385:
			cam_pos_y = 385
		renderer.set_camera_position(cam_pos_x,cam_pos_y)

		return [cam_pos_x,cam_pos_y]
