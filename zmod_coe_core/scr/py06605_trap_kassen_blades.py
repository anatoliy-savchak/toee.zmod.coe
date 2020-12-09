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

	dice = toee.dice_new("1d8+1")
	dice_crit = toee.dice_new("2d8+2")

	hot_range_y = (477, 478, 482, 483, 486, 487, 490, 491)
	for pc in toee.game.leader.group_list():
		x, y = utils_obj.loc2sec(pc.location)
		if (not y in hot_range_y): continue
		if (partsys): toee.game.particles(partsys, pc)
		toee.game.sound(4029, 1)
		hit = trap.attack(pc, 10, 19, 0)
		if (hit & toee.D20CAF_HIT):
			dice_ = dice
			if (hit & toee.D20CAF_CRITICAL): dice_ = dice_crit
			pc.damage(attachee, toee.D20DT_SLASHING, dice_, toee.D20DAP_NORMAL, toee.D20A_NONE)
	return