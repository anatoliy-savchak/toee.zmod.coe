import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon, const_proto_items
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, const_proto_scrolls, const_proto_wands, utils_npc
import startup_zmod, utils_sneak, monster_info, copy, coe_consts, math, utils_locks, utils_trap, const_traps
import py06603_coe_encounters, const_proto_containers, const_proto_list_weapons_masterwork, const_proto_potions, const_proto_wands

CRYPT_LV2 = "CRYPT_LV2"
CRYPT_LV2_DAEMON_SCRIPT = 6607
CRYPT_LV2_DAEMON_ID = "G_16F9F268_872B_4580_9344_68FF73AB960B"
CRYPT_LV2_DAEMON_DIALOG = 6607

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_new_map")
	if (attachee.map != coe_consts.MAP_ID_CRYPT_LV2): toee.RUN_DEFAULT
	ctrl = CtrlCryptLv2.ensure(attachee)
	ctrl.place_encounters(1)
	return toee.RUN_DEFAULT

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	startup_zmod.zmod_templeplus_config_apply()
	if (attachee.map != coe_consts.MAP_ID_CRYPT_LV2): toee.RUN_DEFAULT
	ctrl = CtrlCryptLv2.ensure(attachee)
	ctrl.place_encounters(0)
	return toee.RUN_DEFAULT

def san_heartbeat_disable(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#debug.breakp("san_heartbeat")
	if (attachee.map != coe_consts.MAP_ID_CRYPT_LV2): toee.RUN_DEFAULT
	startup_zmod.zmod_templeplus_config_apply()
	ctrl = cs()
	if (not ctrl):
		ctrl = CtrlCryptLv2.ensure(attachee)
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
	if (attachee.name == coe_consts.PORTAL_CRYPT_OF_EVERFLAME_2ROAD_2EVERFLAME):
		toee.game.fade_and_teleport(0, 0, 0, coe_consts.MAP_ID_ROAD2COE, 468, 507)
		return toee.SKIP_DEFAULT
	elif (attachee.name == coe_consts.PORTAL_CRYPT_OF_EVERFLAME_2CRYPT_OF_EVERFLAME_BELOW):
		toee.game.fade_and_teleport(0, 0, 0, coe_consts.MAP_ID_CRYPT_LV2, 468, 507)
	elif (attachee.name == coe_consts.NAME_WHEEL):
		cs().do_wheel_click(attachee, triggerer)
	elif (attachee.name == coe_consts.NAME_WELL):
		return cs().do_well_click(attachee, triggerer)
	return toee.RUN_DEFAULT

def cs():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(CRYPT_LV2_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlCryptLv2.get_name() in o.data):
		result = o.data[CtrlCryptLv2.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	assert isinstance(result, CtrlCryptLv2)
	return result

class CtrlCryptLv2(ctrl_daemon.CtrlDaemon):
	def __init__(self):
		super(CtrlCryptLv2, self).__init__()
		return

	def created(self, npc):
		super(CtrlCryptLv2, self).created(npc)
		npc.scripts[const_toee.sn_dialog] = CRYPT_LV2_DAEMON_SCRIPT
		return

	@staticmethod
	def get_name():
		return "CtrlCryptLV2"

	@classmethod
	def get_alias(self):
		return "crypt_LV2" # utils_storage.ca("CRYPT_LV2")

	def get_map_default(self):
		return coe_consts.MAP_ID_CRYPT_LV2

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
			pass
			#self.place_encounter_k13()
			#self.place_encounter_k14()
			#self.place_encounter_k15()
			self.place_encounter_k16()

		self.encounters_placed += 1
		self.factions_existance_refresh()
		self.check_sleep_status_update(1)

		utils_obj.scroll_to_leader()
		return

	def delayed_monsters(self):
		return 0

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		super(CtrlCryptLv2, self).monster_setup(npc, encounter_name, monster_code_name, monster_name, no_draw, no_kos, faction)
		npc.scripts[const_toee.sn_dying] = CRYPT_LV2_DAEMON_SCRIPT
		return

	def get_dialogid_default(self):
		return CRYPT_LV2_DAEMON_DIALOG

	def get_monster_faction_default(self, npc):
		return factions_zmod.FACTION_ENEMY

	def get_monster_prefix_default(self):
		return "CRYPT_LV2"

	def critter_dying(self, attachee, triggerer):
		super(CtrlCryptLv2, self).critter_dying(attachee, triggerer)
		assert isinstance(attachee, toee.PyObjHandle)
		return

	def place_encounter_k13(self):
		self.create_promter_at(utils_obj.sec2loc(499, 481), self.get_dialogid_default(), 130, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Crossroads", const_toee.rotation_0700_oclock)
		return

	def place_encounter_k14(self):
		self.create_promter_at(utils_obj.sec2loc(506, 468), self.get_dialogid_default(), 140, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Angry Frogs", const_toee.rotation_0500_oclock)
		if (not self.delayed_monsters()):
			self.place_monsters_k14()
		return

	def place_monsters_k14(self):
		self.create_npc_at(utils_obj.sec2loc(508, 457), py06603_coe_encounters.CtrlGiantFrog, const_toee.rotation_0500_oclock, "k14", "frog1")
		self.create_npc_at(utils_obj.sec2loc(503, 457), py06603_coe_encounters.CtrlGiantFrog, const_toee.rotation_0500_oclock, "k14", "frog2")
		self.create_npc_at(utils_obj.sec2loc(506, 461), py06603_coe_encounters.CtrlGiantFrog, const_toee.rotation_0500_oclock, "k14", "frog3")
		return

	def display_encounter_k14(self):
		print("display_encounter_k14")
		if (self.delayed_monsters()):
			self.place_monsters_k14()
		self.reveal_monster("k14", "frog1")
		self.reveal_monster("k14", "frog2")
		self.reveal_monster("k14", "frog3")
		return

	def activate_encounter_k14(self):
		print("activate_encounter_k14")
		self.activate_monster("k14", "frog1")
		self.activate_monster("k14", "frog2")
		self.activate_monster("k14", "frog3")
		return

	def place_encounter_k15(self):
		self.create_promter_at(utils_obj.sec2loc(495, 468), self.get_dialogid_default(), 150, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Azure Fungus", const_toee.rotation_0500_oclock)
		self.place_monsters_k15()
		return

	def place_monsters_k15(self):
		self.create_npc_at(utils_obj.sec2loc(495, 466), py06603_coe_encounters.CtrlFungusArea, const_toee.rotation_0500_oclock, "k15", "fungus", None, 0, 0)

		body = toee.game.obj_create(14774, utils_obj.sec2loc(498, 463))
		body.obj_set_int(toee.obj_f_hp_damage, 50)

		body = toee.game.obj_create(14774, utils_obj.sec2loc(498, 464))
		body.obj_set_int(toee.obj_f_hp_damage, 50)

		body = toee.game.obj_create(14774, utils_obj.sec2loc(497, 463))
		body.obj_set_int(toee.obj_f_hp_damage, 50)

		body = toee.game.obj_create(14721, utils_obj.sec2loc(497, 467))
		body.obj_set_int(toee.obj_f_hp_damage, 50)
		return

	def place_encounter_k16(self):
		self.create_promter_at(utils_obj.sec2loc(484, 459), self.get_dialogid_default(), 160, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Angry Frogs", const_toee.rotation_0800_oclock)
		if (not self.delayed_monsters()):
			self.place_monsters_k16()
		return

	def place_monsters_k16(self):
		self.create_npc_at(utils_obj.sec2loc(477, 459), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0800_oclock, "k16", "skeleton1")
		self.create_npc_at(utils_obj.sec2loc(475, 460), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0800_oclock, "k16", "skeleton2")
		self.create_npc_at(utils_obj.sec2loc(477, 461), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0800_oclock, "k16", "skeleton3")

		self.create_npc_at(utils_obj.sec2loc(477, 464), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0800_oclock, "k16", "skeleton4")
		self.create_npc_at(utils_obj.sec2loc(476, 466), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0800_oclock, "k16", "skeleton5")
		self.create_npc_at(utils_obj.sec2loc(478, 467), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0800_oclock, "k16", "skeleton6")

		self.create_npc_at(utils_obj.sec2loc(479, 462), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0800_oclock, "k16", "skeleton7")
		self.create_npc_at(utils_obj.sec2loc(479, 465), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0800_oclock, "k16", "skeleton8")
		return

	def display_encounter_k16(self):
		print("display_encounter_k16")
		if (self.delayed_monsters()):
			self.place_monsters_k16()
		self.reveal_monster("k16", "skeleton1")
		self.reveal_monster("k16", "skeleton2")
		self.reveal_monster("k16", "skeleton3")
		self.reveal_monster("k16", "skeleton4")
		self.reveal_monster("k16", "skeleton5")
		self.reveal_monster("k16", "skeleton6")
		self.reveal_monster("k16", "skeleton7")
		self.reveal_monster("k16", "skeleton8")
		return

	def activate_encounter_k16(self):
		print("activate_encounter_k16")
		self.activate_monster("k16", "skeleton1")
		self.activate_monster("k16", "skeleton2")
		self.activate_monster("k16", "skeleton3")
		self.activate_monster("k16", "skeleton4")
		self.activate_monster("k16", "skeleton5")
		self.activate_monster("k16", "skeleton6")
		self.activate_monster("k16", "skeleton7")
		self.activate_monster("k16", "skeleton8")
		return

	def do_wheel_click(self, wheel, pc):
		assert isinstance(wheel, toee.PyObjHandle)
		assert isinstance(pc, toee.PyObjHandle)

		portcullis = utils_obj.find_nearest_obj_by_nameid_loc(utils_obj.sec2loc(483, 497), 10, coe_consts.NAME_DOOR_CRYPT1_DOOR_19_20, toee.OLC_PORTAL)
		if (portcullis):
			locked = portcullis.portal_flags_get() & toee.OPF_LOCKED
			msg = None
			if (locked): 
				portcullis.portal_flag_unset(toee.OPF_LOCKED)
				msg = "Sound of distant door unlocking..."
			else: 
				portcullis.portal_flag_set(toee.OPF_LOCKED)
				msg = "Sound of distant door locking..."
		wheel.float_text_line(msg)
		return

	def do_well_click(self, wheel, pc):
		assert isinstance(wheel, toee.PyObjHandle)
		assert isinstance(pc, toee.PyObjHandle)

		now = toee.game.time.time_game_in_hours2(toee.game.time)
		yesterday = now - 24
		store = utils_storage.obj_storage(pc)
		fountain_last_used = None
		if ("fountain_last_used" in store.data):
			fountain_last_used = store.data["fountain_last_used"]
		if (not fountain_last_used or fountain_last_used <= yesterday):
			fountain_last_used = now
			store.data["fountain_last_used"] = fountain_last_used
			pc.float_text_line("Refreshing!", toee.tf_green)
			potion = utils_item.item_create_in_inventory(const_proto_potions.PROTO_POTION_OF_CURE_MODERATE_WOUNDS, pc, 1, 0)
			#potion = toee.game.obj_create(const_proto_potions.PROTO_POTION_OF_CURE_MODERATE_WOUNDS, pc.location)
			if (potion):
				pc.use_item(potion)
			potion = utils_item.item_create_in_inventory(const_proto_potions.PROTO_POTION_OF_RESTORATION, pc, 1, 0)
			#potion = toee.game.obj_create(const_proto_potions.PROTO_POTION_OF_RESTORATION, pc.location)
			if (potion):
				pc.use_item(potion)
		else:
			pc.float_text_line("Already used today", toee.tf_yellow)

		return toee.SKIP_DEFAULT