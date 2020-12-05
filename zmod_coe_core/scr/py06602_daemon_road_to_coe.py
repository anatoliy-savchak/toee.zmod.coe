import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, const_proto_scrolls, const_proto_wands, utils_npc
import startup_zmod, utils_sneak, monster_info, copy, coe_consts

MAP_ID_ROAD2COE = 5127
ROAD2COE = "road2coe"
ROAD2COE_DAEMON_SCRIPT = 6502
ROAD2COE_DAEMON_ID = "G_777CFFCC_1864_4C4D_B05F_ECE4C6EF4B18"
ROAD2COE_DAEMON_DIALOG = 6502

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print(attachee.id)
	debug.breakp("san_new_map")
	if (attachee.map != MAP_ID_ROAD2COE): toee.RUN_DEFAULT
	ctrl = CtrlRoad2Coe.ensure(attachee)
	ctrl.place_encounters(1)
	return toee.RUN_DEFAULT

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	startup_zmod.zmod_templeplus_config_apply()
	if (attachee.map != MAP_ID_ROAD2COE): toee.RUN_DEFAULT
	ctrl = CtrlRoad2Coe.ensure(attachee)
	ctrl.place_encounters(0)
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#debug.breakp("san_heartbeat")
	if (attachee.map != MAP_ID_ROAD2COE): toee.RUN_DEFAULT
	startup_zmod.zmod_templeplus_config_apply()
	ctrl = cs()
	if (not ctrl):
		ctrl = CtrlRoad2Coe.ensure(attachee)
		ctrl.place_encounters(1)
	if (ctrl):
		ctrl.heartbeat()
	return toee.RUN_DEFAULT

def san_dying(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	c = cs()
	if (c):
		c.critter_dying(attachee, triggerer)
	storage = utils_storage.obj_storage_by_id(attachee.id)
	if (storage):
		cb = storage.get_data(ctrl_behaviour.CtrlBehaviour.get_name())
		if ("dying" in dir(cb)):
			cb.dying(attachee, triggerer)
	return toee.RUN_DEFAULT


def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))
	return toee.RUN_DEFAULT

def cs():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(VILLAGE_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlRoad2Coe.get_name() in o.data):
		result = o.data[CtrlRoad2Coe.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlRoad2Coe(ctrl_daemon.CtrlDaemon):
	def __init__(self):
		super(CtrlRoad2Coe, self).__init__()
		return

	def created(self, npc):
		super(CtrlRoad2Coe, self).created(npc)
		npc.scripts[const_toee.sn_dialog] = VILLAGE_DAEMON_SCRIPT
		return

	@staticmethod
	def get_name():
		return "CtrlRoad2Coe"

	@classmethod
	def get_alias(self):
		return "road2coe" # utils_storage.ca("road2coe")

	def get_map_default(self):
		return MAP_ID_ROAD2COE

	def place_encounters(self, new_map):
		print("new_map: {}".format(new_map))
		print("place_encounters.encounters_placed == {}".format(self.encounters_placed))
		startup_zmod.zmod_templeplus_config_apply()
		startup_zmod.zmod_conditions_apply_pc()

		if (self.encounters_placed and new_map == 0): return

		this_entrance_time = toee.game.time.time_game_in_hours2(toee.game.time)
		print("this_entrance_time == {}".format(this_entrance_time))
		if (not self.encounters_placed):
			self.first_entered_shrs = this_entrance_time
		self.last_entered_shrs = this_entrance_time
		if (not self.last_leave_shrs):
			self.last_leave_shrs = this_entrance_time

		if (not self.encounters_placed):
			self.place_exits()

		self.encounters_placed += 1
		self.factions_existance_refresh()
		self.check_sleep_status_update(1)

		#toee.game.fade_and_teleport(0, 0, 0, self.get_map_default(), 479, 494) #smith
		#toee.game.fade_and_teleport(0, 0, 0, self.get_map_default(), 466, 468) #near fontain entrance
		utils_obj.scroll_to_leader()
		return

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		super(CtrlRoad2Coe, self).monster_setup(npc, encounter_name, monster_code_name, monster_name, no_draw, no_kos, faction)
		npc.scripts[const_toee.sn_dying] = ROAD2COE_DAEMON_SCRIPT
		return

	def get_dialogid_default(self):
		return ROAD2COE_DAEMON_DIALOG

	def get_monster_faction_default(self, npc):
		return factions_zmod.FACTION_WILDERNESS_HOSTILE

	def get_monster_prefix_default(self):
		return "road2coe"

	def place_exits(self):
		return