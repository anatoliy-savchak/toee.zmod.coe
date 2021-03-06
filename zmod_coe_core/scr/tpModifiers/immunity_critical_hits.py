import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Immunity_Critical_Hits"

print("Registering " + GetConditionName())
###################################################

def OnD20QueryTrue(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	#toee.game.create_history_from_pattern(65, attachee, toee.OBJ_HANDLE_NULL) # is immune to ~critical hit~[TAG_CRITICAL_HIT]
	evt_obj.return_val = 1
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_Critter_Is_Immune_Critical_Hits, OnD20QueryTrue, ())

