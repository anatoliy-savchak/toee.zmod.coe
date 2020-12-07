import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, const_proto_scrolls, const_proto_wands, utils_npc
import startup_zmod, utils_sneak, monster_info, copy, coe_consts, math, utils_locks
import py06603_coe_encounters, const_proto_containers

MAP_ID_CRYPT_LV1 = 5128
CRYPT_LV1 = "CRYPT_LV1"
CRYPT_LV1_DAEMON_SCRIPT = 6604
CRYPT_LV1_DAEMON_ID = "G_506CD5D3_2D09_446F_AA0A_75B0281582B2"
CRYPT_LV1_DAEMON_DIALOG = 6604

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_new_map")
	if (attachee.map != MAP_ID_CRYPT_LV1): toee.RUN_DEFAULT
	ctrl = CtrlCRYPT_LV1.ensure(attachee)
	ctrl.place_encounters(1)
	return toee.RUN_DEFAULT

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	startup_zmod.zmod_templeplus_config_apply()
	if (attachee.map != MAP_ID_CRYPT_LV1): toee.RUN_DEFAULT
	ctrl = CtrlCRYPT_LV1.ensure(attachee)
	ctrl.place_encounters(0)
	return toee.RUN_DEFAULT

def san_heartbeat_disable(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#debug.breakp("san_heartbeat")
	if (attachee.map != MAP_ID_CRYPT_LV1): toee.RUN_DEFAULT
	startup_zmod.zmod_templeplus_config_apply()
	ctrl = cs()
	if (not ctrl):
		ctrl = CtrlCRYPT_LV1.ensure(attachee)
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
		pass
	return toee.RUN_DEFAULT

def cs():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(CRYPT_LV1_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlCRYPT_LV1.get_name() in o.data):
		result = o.data[CtrlCRYPT_LV1.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlCRYPT_LV1(ctrl_daemon.CtrlDaemon):
	def __init__(self):
		super(CtrlCRYPT_LV1, self).__init__()
		return

	def created(self, npc):
		super(CtrlCRYPT_LV1, self).created(npc)
		npc.scripts[const_toee.sn_dialog] = CRYPT_LV1_DAEMON_SCRIPT
		return

	@staticmethod
	def get_name():
		return "CtrlCryptLv1"

	@classmethod
	def get_alias(self):
		return "crypt_lv1" # utils_storage.ca("CRYPT_LV1")

	def get_map_default(self):
		return MAP_ID_CRYPT_LV1

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
			#self.place_encounter_k01()
			self.place_chests()

		self.encounters_placed += 1
		self.factions_existance_refresh()
		self.check_sleep_status_update(1)

		#toee.game.fade_and_teleport(0, 0, 0, self.get_map_default(), 479, 494) #smith
		#toee.game.fade_and_teleport(0, 0, 0, self.get_map_default(), 466, 468) #near fontain entrance
		utils_obj.scroll_to_leader()
		return

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		super(CtrlCRYPT_LV1, self).monster_setup(npc, encounter_name, monster_code_name, monster_name, no_draw, no_kos, faction)
		npc.scripts[const_toee.sn_dying] = CRYPT_LV1_DAEMON_SCRIPT
		return

	def get_dialogid_default(self):
		return CRYPT_LV1_DAEMON_DIALOG

	def get_monster_faction_default(self, npc):
		return factions_zmod.FACTION_ENEMY

	def get_monster_prefix_default(self):
		return "CRYPT_LV1"

	def place_encounter_k01(self):
		self.create_promter_at(utils_obj.sec2loc(480, 499), self.get_dialogid_default(), 10, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Entry Hall", const_toee.rotation_1100_oclock)
		self.create_npc_at(utils_obj.sec2loc(482, 489), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0500_oclock, "k01", "skeleton1")
		self.create_npc_at(utils_obj.sec2loc(480, 489), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0500_oclock, "k01", "skeleton2")
		self.create_npc_at(utils_obj.sec2loc(479, 489), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0500_oclock, "k01", "skeleton3")
		self.create_npc_at(utils_obj.sec2loc(480, 491), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0500_oclock, "k01", "skeleton4")
		self.create_npc_at(utils_obj.sec2loc(485, 495), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0300_oclock, "k01", "skeleton5")
		self.create_npc_at(utils_obj.sec2loc(476, 495), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0600_oclock, "k01", "skeleton6")
		return

	def display_encounter_k01(self):
		print("display_encounter_k01")
		self.reveal_monster("k01", "skeleton1")
		self.reveal_monster("k01", "skeleton2")
		self.reveal_monster("k01", "skeleton3")
		self.reveal_monster("k01", "skeleton4")
		self.reveal_monster("k01", "skeleton5")
		self.reveal_monster("k01", "skeleton6")
		return

	def activate_encounter_k01(self):
		print("activate_encounter_k01")
		self.activate_monster("k01", "skeleton1")
		self.activate_monster("k01", "skeleton2")
		self.activate_monster("k01", "skeleton3")
		self.activate_monster("k01", "skeleton4")
		self.activate_monster("k01", "skeleton5")
		self.activate_monster("k01", "skeleton6")
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
		super(CtrlCRYPT_LV1, self).critter_dying(attachee, triggerer)
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

	def place_chests(self):

		chest_with_key_num = toee.game.random_range(1, 3)
		chest_with_key = None
		# first chest
		if (1):
			loc = utils_obj.sec2loc(494, 508)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_WOODEN_MEDIUM, loc)
			if (chest):
				chest.move(loc, -8.485282, -8.485282)
				chest.rotation = math.radians(const_toee.rotation_grad_south_east)
				chest.obj_set_int(toee.obj_f_secretdoor_flags, const_toee.OSDF_SECRET_DOOR)
				chest.obj_set_int(toee.obj_f_secretdoor_dc, 5)
				chest.obj_set_int(toee.obj_f_secretdoor_effectname, 1200)
				if (chest_with_key_num == 1): chest_with_key = chest
		# second chest
		if (1):
			loc = utils_obj.sec2loc(503, 498)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_WOODEN_MEDIUM, loc)
			if (chest):
				chest.move(loc, -8.485282, -14.1421356)
				chest.rotation = math.radians(const_toee.rotation_grad_south_west)
				chest.obj_set_int(toee.obj_f_secretdoor_flags, const_toee.OSDF_SECRET_DOOR)
				chest.obj_set_int(toee.obj_f_secretdoor_dc, 5)
				chest.obj_set_int(toee.obj_f_secretdoor_effectname, 1200)
				if (chest_with_key_num == 2): chest_with_key = chest
		# third chest
		if (1):
			loc = utils_obj.sec2loc(494, 487)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_WOODEN_MEDIUM, loc)
			if (chest):
				chest.move(loc, -9.899495, -12.7279215)
				chest.rotation = math.radians(const_toee.rotation_grad_south_east)
				chest.obj_set_int(toee.obj_f_secretdoor_flags, const_toee.OSDF_SECRET_DOOR)
				chest.obj_set_int(toee.obj_f_secretdoor_dc, 5)
				chest.obj_set_int(toee.obj_f_secretdoor_effectname, 1200)
				if (chest_with_key_num == 3): chest_with_key = chest

		if (chest_with_key):
			key = utils_item.item_create_in_inventory(10001, chest_with_key)
			if (key):
				key.obj_set_int(toee.obj_f_key_key_id, coe_consts.KEY_CRYPT1_DOOR_2)
				#key.obj_set_int(toee.obj_f_description, toee.game.make_custom_name("Crypt key"))

			locked_door = utils_obj.find_nearest_obj_by_nameid_loc(utils_obj.sec2loc(499, 485), 10, coe_consts.NAME_DOOR_CRYPT1_DOOR_2, toee.OLC_PORTAL)
			if (locked_door):
				locked_door.portal_flag_set(toee.OPF_LOCKED)
				utils_locks.portal_setup_dc(locked_door, utils_locks.LOCK_DC_AVERAGE, coe_consts.KEY_CRYPT1_DOOR_2 \
					, utils_locks.HP_DOOR_WOODEN_GOOD, utils_locks.HARDNESS_DOOR_WOODEN_GOOD, utils_locks.BREAK_DC_DOOR_WOODEN_GOOD)
		return