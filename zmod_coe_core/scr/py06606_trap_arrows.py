import toee, debug, utils_obj

def san_trap(trap, triggerer):
	assert isinstance(triggerer, toee.PyObjHandle)
	assert isinstance(trap, toee.PyTrap)

	trap_trigger_kassen_blades(trap.obj, triggerer, trap.partsys, trap)
	return toee.SKIP_DEFAULT

def trap_trigger_kassen_blades(attachee, triggerer, partsys, trap):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	assert isinstance(trap, toee.PyTrap)

	dice = toee.dice_new("1d8")
	dice_crit = toee.dice_new("2d8")

	toee.game.particles("Trap-Darts2", trap.obj)
	toee.game.sound(4023,1)

	hot_range_x = (470, 484)
	hot_range_y = (471, 485)
	for pc in toee.game.leader.group_list():
		x, y = utils_obj.loc2sec(pc.location)
		if ((x < hot_range_x[0]) or (x > hot_range_x[1])): continue
		if ((y < hot_range_y[0]) or (y > hot_range_y[1])): continue
		hit = trap.attack(pc, 10, 19, 0)
		if (hit & toee.D20CAF_HIT):
			dice_ = dice
			if (hit & toee.D20CAF_CRITICAL): dice_ = dice_crit
			pc.damage(attachee, toee.D20DT_SUBDUAL, dice_, toee.D20DAP_SLASHING, toee.D20A_NONE)
	return