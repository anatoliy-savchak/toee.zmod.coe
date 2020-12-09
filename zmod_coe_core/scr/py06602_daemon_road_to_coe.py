import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, const_proto_scrolls, const_proto_wands, utils_npc
import startup_zmod, utils_sneak, monster_info, copy, coe_consts
import py06603_coe_encounters

ROAD2COE = "road2coe"
ROAD2COE_DAEMON_SCRIPT = 6602
ROAD2COE_DAEMON_ID = "G_A2A17BEF_C82B_4021_B305_1857DF8D8A71"
ROAD2COE_DAEMON_DIALOG = 6602

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_new_map")
	if (attachee.map != coe_consts.MAP_ID_ROAD2COE): toee.RUN_DEFAULT
	ctrl = CtrlRoad2Coe.ensure(attachee)
	ctrl.place_encounters(1)
	return toee.RUN_DEFAULT

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	startup_zmod.zmod_templeplus_config_apply()
	if (attachee.map != coe_consts.MAP_ID_ROAD2COE): toee.RUN_DEFAULT
	ctrl = CtrlRoad2Coe.ensure(attachee)
	ctrl.place_encounters(0)
	return toee.RUN_DEFAULT

def san_heartbeat_disable(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#debug.breakp("san_heartbeat")
	if (attachee.map != coe_consts.MAP_ID_ROAD2COE): toee.RUN_DEFAULT
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
	if (attachee.name == coe_consts.PORTAL_ROAD_2EVERFLAME_2KASSEN):
		toee.game.fade_and_teleport(0, 0, 0, 5126, 468, 507)
		return toee.SKIP_DEFAULT
	elif (attachee.name == coe_consts.PORTAL_ROAD_2EVERFLAME_2CRYPT_OF_EVERFLAME):
		toee.game.fade_and_teleport(0, 0, 0, coe_consts.MAP_ID_CRYPT_LV1, 480, 508)
	return toee.RUN_DEFAULT

def cs():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(ROAD2COE_DAEMON_ID)
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
		npc.scripts[const_toee.sn_dialog] = ROAD2COE_DAEMON_SCRIPT
		return

	@staticmethod
	def get_name():
		return "CtrlRoad2Coe"

	@classmethod
	def get_alias(self):
		return "road2coe" # utils_storage.ca("road2coe")

	def get_map_default(self):
		return coe_consts.MAP_ID_ROAD2COE

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
			self.place_encounter_j01()
			self.place_encounter_j02()

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

	def place_encounter_j01(self):
		self.create_promter_at(utils_obj.sec2loc(479, 475), self.get_dialogid_default(), 10, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "First Fight", const_toee.rotation_1100_oclock)
		npc = self.create_npc_at(utils_obj.sec2loc(487, 471), py06603_coe_encounters.CtrlOrc, const_toee.rotation_0200_oclock, "j01", "orc1")[0]
		#npc.condition_add("Deal_Subdual_Damage")

		npc = self.create_npc_at(utils_obj.sec2loc(476, 470), py06603_coe_encounters.CtrlOrc, const_toee.rotation_0800_oclock, "j01", "orc2")[0]
		#npc.condition_add("Deal_Subdual_Damage")

		npc = self.create_npc_at(utils_obj.sec2loc(473, 474), py06603_coe_encounters.CtrlOrc, const_toee.rotation_0800_oclock, "j01", "orc3")[0]
		#npc.condition_add("Deal_Subdual_Damage")
		return

	def display_encounter_j01(self):
		print("display_encounter_j01")
		self.reveal_monster("j01", "orc1")
		self.reveal_monster("j01", "orc2")
		self.reveal_monster("j01", "orc3")
		return

	def activate_encounter_j01(self):
		print("activate_encounter_j01")
		self.activate_monster("j01", "orc1")
		self.activate_monster("j01", "orc2")
		self.activate_monster("j01", "orc3")
		return

	def place_encounter_j02(self):
		self.create_promter_at(utils_obj.sec2loc(465, 485), self.get_dialogid_default(), 20, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Wolfs", const_toee.rotation_1100_oclock)
		self.create_npc_at(utils_obj.sec2loc(456, 488), py06603_coe_encounters.CtrlWolf, const_toee.rotation_0800_oclock, "j02", "wolf1", factions_zmod.FACTION_WILDERNESS_HOSTILE)
		self.create_npc_at(utils_obj.sec2loc(458, 491), py06603_coe_encounters.CtrlWolf, const_toee.rotation_0900_oclock, "j02", "wolf2", factions_zmod.FACTION_WILDERNESS_HOSTILE)
		self.create_npc_at(utils_obj.sec2loc(461, 493), py06603_coe_encounters.CtrlWolf, const_toee.rotation_0100_oclock, "j02", "wolf3", factions_zmod.FACTION_WILDERNESS_HOSTILE)
		return

	def display_encounter_j02(self):
		print("display_encounter_j02")
		self.reveal_monster("j02", "wolf1")
		self.reveal_monster("j02", "wolf2")
		self.reveal_monster("j02", "wolf3")
		return

	def activate_encounter_j02(self):
		print("activate_encounter_j02")
		self.activate_monster("j02", "wolf1")
		self.activate_monster("j02", "wolf2")
		self.activate_monster("j02", "wolf3")
		return

	def critter_dying(self, attachee, triggerer):
		super(CtrlRoad2Coe, self).critter_dying(attachee, triggerer)
		assert isinstance(attachee, toee.PyObjHandle)

		if (attachee.proto == py06603_coe_encounters.CtrlOrc.get_proto_id()):
			npc1 = self.get_monsterinfo_and_npc_and_ctrl("j01", "orc1")[1]
			npc2 = self.get_monsterinfo_and_npc_and_ctrl("j01", "orc2")[1]
			npc3 = self.get_monsterinfo_and_npc_and_ctrl("j01", "orc3")[1]
			if ((not npc1 or not utils_npc.npc_is_alive(npc1)) and (not npc2 or not utils_npc.npc_is_alive(npc2)) and (not npc3 or not utils_npc.npc_is_alive(npc3))):
				for pc in toee.game.party:
					pc.obj_set_int(toee.obj_f_hp_damage, 0)
				toee.game.party[0].float_text_line("It was illusion!", toee.tf_green)
				toee.game.create_history_freeform("\n{}: It was illusion!\n".format(toee.game.party[0].description))
		return
