import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon, const_proto_items
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, const_proto_scrolls, const_proto_wands, utils_npc
import startup_zmod, utils_sneak, monster_info, copy, coe_consts, math, utils_locks, utils_trap, const_traps
import py06603_coe_encounters, const_proto_containers, const_proto_list_weapons_masterwork, const_proto_potions, const_proto_wands

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
	ctrl = CtrlCryptLv1.ensure(attachee)
	ctrl.place_encounters(1)
	return toee.RUN_DEFAULT

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	startup_zmod.zmod_templeplus_config_apply()
	if (attachee.map != MAP_ID_CRYPT_LV1): toee.RUN_DEFAULT
	ctrl = CtrlCryptLv1.ensure(attachee)
	ctrl.place_encounters(0)
	return toee.RUN_DEFAULT

def san_heartbeat_disable(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#debug.breakp("san_heartbeat")
	if (attachee.map != MAP_ID_CRYPT_LV1): toee.RUN_DEFAULT
	startup_zmod.zmod_templeplus_config_apply()
	ctrl = cs()
	if (not ctrl):
		ctrl = CtrlCryptLv1.ensure(attachee)
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
	if (CtrlCryptLv1.get_name() in o.data):
		result = o.data[CtrlCryptLv1.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlCryptLv1(ctrl_daemon.CtrlDaemon):
	def __init__(self):
		super(CtrlCryptLv1, self).__init__()
		return

	def created(self, npc):
		super(CtrlCryptLv1, self).created(npc)
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
			#self.place_encounter_k03()
			#self.place_encounter_k04()
			#self.place_encounter_k05()
			#self.place_encounter_k06()
			self.place_encounter_k07()
			#self.place_encounter_k08()
			#self.place_encounter_k09()
			#self.place_encounter_k10()
			#self.place_encounter_k11()

		self.encounters_placed += 1
		self.factions_existance_refresh()
		self.check_sleep_status_update(1)

		#toee.game.fade_and_teleport(0, 0, 0, self.get_map_default(), 479, 494) #smith
		#toee.game.fade_and_teleport(0, 0, 0, self.get_map_default(), 466, 468) #near fontain entrance
		utils_obj.scroll_to_leader()
		return

	def delayed_monsters(self):
		return 1

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		super(CtrlCryptLv1, self).monster_setup(npc, encounter_name, monster_code_name, monster_name, no_draw, no_kos, faction)
		npc.scripts[const_toee.sn_dying] = CRYPT_LV1_DAEMON_SCRIPT
		return

	def get_dialogid_default(self):
		return CRYPT_LV1_DAEMON_DIALOG

	def get_monster_faction_default(self, npc):
		return factions_zmod.FACTION_ENEMY

	def get_monster_prefix_default(self):
		return "CRYPT_LV1"

	def critter_dying(self, attachee, triggerer):
		super(CtrlCryptLv1, self).critter_dying(attachee, triggerer)
		assert isinstance(attachee, toee.PyObjHandle)
		return

	def place_encounter_k01(self):
		self.create_promter_at(utils_obj.sec2loc(480, 499), self.get_dialogid_default(), 10, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Entry Hall", const_toee.rotation_1100_oclock)
		if (not self.delayed_monsters()):
			self.place_monsters_k01()
		return

	def place_monsters_k01(self):
		self.create_npc_at(utils_obj.sec2loc(482, 489), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0500_oclock, "k01", "skeleton1")
		self.create_npc_at(utils_obj.sec2loc(480, 489), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0500_oclock, "k01", "skeleton2")
		self.create_npc_at(utils_obj.sec2loc(479, 489), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0500_oclock, "k01", "skeleton3")
		self.create_npc_at(utils_obj.sec2loc(480, 491), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0500_oclock, "k01", "skeleton4")
		self.create_npc_at(utils_obj.sec2loc(485, 495), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0300_oclock, "k01", "skeleton5")
		self.create_npc_at(utils_obj.sec2loc(476, 495), py06603_coe_encounters.CtrlSkeletonEntry, const_toee.rotation_0600_oclock, "k01", "skeleton6")
		return

	def display_encounter_k01(self):
		print("display_encounter_k01")
		if (self.delayed_monsters()):
			self.place_monsters_k01()
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

	def place_encounter_k04(self):
		self.create_promter_at(utils_obj.sec2loc(488, 470), self.get_dialogid_default(), 40, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Hungry Beetle", const_toee.rotation_0600_oclock)
		if (not self.delayed_monsters()):
			self.place_monsters_k04()
		return

	def place_monsters_k04(self):
		self.create_npc_at(utils_obj.sec2loc(487, 469), py06603_coe_encounters.CtrlBeetleBombardier, const_toee.rotation_0900_oclock, "k04", "beetle1", factions_zmod.FACTION_WILDERNESS_HOSTILE)
		return

	def display_encounter_k04(self):
		print("display_encounter_k04")
		if (self.delayed_monsters()):
			self.place_monsters_k04()
		self.reveal_monster("k04", "beetle1")
		return

	def activate_encounter_k04(self):
		print("activate_encounter_k04")
		self.activate_monster("k04", "beetle1")
		return

	def place_encounter_k05(self):
		self.create_promter_at(utils_obj.sec2loc(498, 459), self.get_dialogid_default(), 50, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Shadowy Shapes", const_toee.rotation_0600_oclock)
		if (not self.delayed_monsters()):
			self.place_monsters_k05()
		return

	def place_monsters_k05(self):
		self.create_npc_at(utils_obj.sec2loc(492, 451), py06603_coe_encounters.CtrlShadow, const_toee.rotation_0600_oclock, "k05", "shadow", factions_zmod.FACTION_ENEMY)

		dagger = toee.game.obj_create(const_proto_weapon.PROTO_WEAPON_DAGGER_PLUS_1, utils_obj.sec2loc(495, 455))
		if (dagger):
			dagger.obj_set_int(toee.obj_f_secretdoor_flags, const_toee.OSDF_SECRET_DOOR)
			dagger.obj_set_int(toee.obj_f_secretdoor_dc, 5)
			dagger.obj_set_int(toee.obj_f_secretdoor_effectname, 1200)

		key = toee.game.obj_create(const_proto_items.PROTO_KEY_IRON_RUSTY, utils_obj.sec2loc(495, 456))
		if (key):
			key.obj_set_int(toee.obj_f_key_key_id, coe_consts.KEY_CRYPT1_DOOR_6_7)
			key.obj_set_int(toee.obj_f_secretdoor_flags, const_toee.OSDF_SECRET_DOOR)
			key.obj_set_int(toee.obj_f_secretdoor_dc, 5)
			key.obj_set_int(toee.obj_f_secretdoor_effectname, 1200)
		return

	def display_encounter_k05(self):
		print("display_encounter_k05")
		if (self.delayed_monsters()):
			self.place_monsters_k05()
		self.reveal_monster("k05", "shadow")
		return

	def activate_encounter_k05(self):
		print("activate_encounter_k05")
		self.activate_monster("k05", "shadow")
		return

	def place_encounter_k03(self):
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
				utils_trap.setup_trap(chest, const_traps.TRAP_PIT_TRAP, const_traps.TRAP_SCRIPT_PIT_TRAP)
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
				utils_trap.setup_trap(chest, const_traps.TRAP_PIT_TRAP, const_traps.TRAP_SCRIPT_PIT_TRAP)
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
				utils_trap.setup_trap(chest, const_traps.TRAP_PIT_TRAP, const_traps.TRAP_SCRIPT_PIT_TRAP)

		if (chest_with_key):
			key = utils_item.item_create_in_inventory(const_proto_items.PROTO_KEY_IRON_RUSTY, chest_with_key)
			if (key):
				key.obj_set_int(toee.obj_f_key_key_id, coe_consts.KEY_CRYPT1_DOOR_2)
				#key.obj_set_int(toee.obj_f_description, toee.game.make_custom_name("Crypt key"))

			locked_door = utils_obj.find_nearest_obj_by_nameid_loc(utils_obj.sec2loc(499, 485), 10, coe_consts.NAME_DOOR_CRYPT1_DOOR_2, toee.OLC_PORTAL)
			if (locked_door):
				locked_door.portal_flag_set(toee.OPF_LOCKED)
				utils_locks.portal_setup_dc(locked_door, utils_locks.LOCK_DC_AVERAGE, coe_consts.KEY_CRYPT1_DOOR_2 \
					, utils_locks.HP_DOOR_WOODEN_GOOD, utils_locks.HARDNESS_DOOR_WOODEN_GOOD, utils_locks.BREAK_DC_DOOR_WOODEN_GOOD)
		return

	def place_encounter_k06(self):
		self.create_promter_at(utils_obj.sec2loc(463, 497), self.get_dialogid_default(), 60, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Key Pool", const_toee.rotation_0700_oclock)

		def do_lock(locked_door, key_id):
			assert isinstance(locked_door, toee.PyObjHandle)
			if (locked_door):
				locked_door.portal_flag_set(toee.OPF_LOCKED)
				utils_locks.portal_setup_dc(locked_door, utils_locks.LOCK_DC_GOOD, key_id \
					, utils_locks.HP_DOOR_WOODEN_STRONG, utils_locks.HARDNESS_DOOR_WOODEN_STRONG, utils_locks.BREAK_DC_DOOR_WOODEN_STRONG)
			return

		do_lock(utils_obj.find_nearest_obj_by_nameid_loc(utils_obj.sec2loc(467, 494), 10, coe_consts.NAME_DOOR_CRYPT1_DOOR_6_7, toee.OLC_PORTAL), coe_consts.KEY_CRYPT1_DOOR_6_7)
		do_lock(utils_obj.find_nearest_obj_by_nameid_loc(utils_obj.sec2loc(460, 494), 10, coe_consts.NAME_DOOR_CRYPT1_DOOR_6_8, toee.OLC_PORTAL), coe_consts.KEY_CRYPT1_DOOR_9_10)
		return

	def display_encounter_k06(self):
		key = toee.game.obj_create(const_proto_items.PROTO_KEY_GOLD, utils_obj.sec2loc(463, 504))
		if (key):
			key.obj_set_int(toee.obj_f_key_key_id, coe_consts.KEY_CRYPT1_DOOR_9_10)
			key.obj_set_int(toee.obj_f_secretdoor_flags, const_toee.OSDF_SECRET_DOOR)
			key.obj_set_int(toee.obj_f_secretdoor_dc, 27)
			key.obj_set_int(toee.obj_f_secretdoor_effectname, 1200)
			key.obj_set_int(toee.obj_f_key_pad_i_1, toee.OIF_IS_MAGICAL)
		return

	def place_encounter_k07(self):
		self.create_promter_at(utils_obj.sec2loc(466, 486), self.get_dialogid_default(), 70, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Room of Reflection", const_toee.rotation_0400_oclock)
		return

	def place_encounter_k08(self):
		self.create_promter_at(utils_obj.sec2loc(460, 488), self.get_dialogid_default(), 80, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "The Gauntlet", const_toee.rotation_0400_oclock)

		door = utils_obj.find_nearest_obj_by_nameid_loc(utils_obj.sec2loc(460, 474), 10, coe_consts.NAME_DOOR_CRYPT1_DOOR_8_9, toee.OLC_PORTAL)
		if (door):
			utils_trap.setup_trap(door, const_traps.TRAP_SCYTHE_20x20_2, 6605)
		else: debug.breakp("no door!")
		return

	def display_encounter_k08(self):
		return

	def place_encounter_k09(self):
		self.create_promter_at(utils_obj.sec2loc(463, 468), self.get_dialogid_default(), 90, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "The Shield Guardian", const_toee.rotation_0400_oclock)
		if (not self.delayed_monsters()):
			self.place_monsters_k09()
		return

	def place_monsters_k09(self):
		self.create_npc_at(utils_obj.sec2loc(463, 460), py06603_coe_encounters.CtrlGolemWoodKassen, const_toee.rotation_0400_oclock, "k09", "golem", factions_zmod.FACTION_ENEMY)
		return

	def display_encounter_k09(self):
		print("display_encounter_k09")
		if (self.delayed_monsters()):
			self.place_monsters_k09()
		self.reveal_monster("k09", "golem")
		return

	def activate_encounter_k09(self):
		print("activate_encounter_k09")
		self.activate_monster("k09", "golem")
		return

	def place_encounter_k10(self):
		self.create_promter_at(utils_obj.sec2loc(458, 451), self.get_dialogid_default(), 100, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Supply Vault", const_toee.rotation_0400_oclock)

		if (not coe_consts.ISDEBUG):
			door = utils_obj.find_nearest_obj_by_nameid_loc(utils_obj.sec2loc(460, 457), 10, coe_consts.NAME_DOOR_CRYPT1_DOOR_9_10, toee.OLC_PORTAL)
			if (door):
				utils_locks.portal_setup_dc(door, utils_locks.LOCK_DC_GOOD, coe_consts.KEY_CRYPT1_DOOR_9_10 \
					, utils_locks.HP_DOOR_WOODEN_STRONG, utils_locks.HARDNESS_DOOR_WOODEN_STRONG, utils_locks.BREAK_DC_DOOR_WOODEN_STRONG)
			else: debug.breakp("no door!")
		return

	def display_encounter_k10(self):
		return

	@staticmethod
	def give_treasure():
		def announce(pc, item):
			assert isinstance(pc, toee.PyObjHandle)
			assert isinstance(item, toee.PyObjHandle)
			if (item): 
				pc.float_text_line("Received {}!".format(item.description), toee.tf_green)
			return item

		def make_new_weapon(pc):
			assert isinstance(pc, toee.PyObjHandle)
			newweapon = None
			weapon = pc.item_worn_at(toee.item_wear_weapon_primary)
			if (weapon):
				protoid = weapon.proto
				if (protoid in const_proto_list_weapons_masterwork.PROTOS_WEAPON_2MASTERWORK):
					protoid = const_proto_list_weapons_masterwork.PROTOS_WEAPON_2MASTERWORK[protoid]
					if (protoid):
						if (not utils_item.item_has(pc, protoid)):
							newweapon = utils_item.item_create_in_inventory(protoid, pc, 1, 1)
							announce(pc, newweapon)
			return newweapon

		def give_scroll(pc, proto):
			assert isinstance(pc, toee.PyObjHandle)
			assert isinstance(proto, int)
			scroll = utils_item.item_create_in_inventory(proto, pc, 1, 1)
			scroll.item_flag_set(toee.OIF_IDENTIFIED)
			announce(pc, scroll)
			return scroll

		def give_fighter_potion(pc):
			assert isinstance(pc, toee.PyObjHandle)
			item = utils_item.item_create_in_inventory(const_proto_potions.PROTO_POTION_OIL_OF_MAGIC_WEAPON, pc, 1, 1)
			item.item_flag_set(toee.OIF_IDENTIFIED)
			announce(pc, item)
			return item

		def give_used_wand(pc, proto, uses):
			assert isinstance(pc, toee.PyObjHandle)
			assert isinstance(proto, int)
			assert isinstance(uses, int)
			wand = utils_item.item_create_in_inventory(proto, pc, 1, 1)
			wand.item_flag_set(toee.OIF_IDENTIFIED)
			wand.obj_set_int(toee.obj_f_item_spell_charges_idx, uses)
			announce(pc, wand)
			return wand

		for pc in toee.game.leader.group_list():
			pcclass1 = pc.char_classes[0]
			if (pcclass1 == toee.stat_level_barbarian):
				give_fighter_potion(pc)
				if (not make_new_weapon(pc)):
					give_scroll(pc, const_proto_potions.PROTO_POTION_OF_BULLS_STRENGTH)

			elif (pcclass1 == toee.stat_level_bard):
				give_scroll(pc, const_proto_scrolls.PROTO_SCROLL_OF_CATS_GRACE)
				if (not make_new_weapon(pc)):
					give_scroll(pc, const_proto_scrolls.PROTO_SCROLL_OF_CONFUSION_LESSER)

			elif (pcclass1 == toee.stat_level_cleric):
				give_scroll(pc, const_proto_scrolls.PROTO_SCROLL_OF_RESTORATION_LESSER)
				give_used_wand(pc, const_proto_wands.PROTO_WAND_OF_CURE_LIGHT_WOUNDS, 10)

			elif (pcclass1 == toee.stat_level_druid):
				give_scroll(pc, const_proto_scrolls.PROTO_SCROLL_OF_BARKSKIN)
				give_used_wand(pc, const_proto_wands.PROTO_WAND_OF_PRODUCE_FLAME, 10)

			elif (pcclass1 == toee.stat_level_fighter):
				give_fighter_potion(pc)
				if (not make_new_weapon(pc)):
					give_scroll(pc, const_proto_potions.PROTO_POTION_OF_BULLS_STRENGTH)

			elif (pcclass1 == toee.stat_level_monk):
				give_scroll(pc, const_proto_potions.PROTO_POTION_OF_CURE_LIGHT_WOUNDS)
				if (not make_new_weapon(pc)):
					give_scroll(pc, const_proto_potions.PROTO_POTION_OF_OWLS_WISDOM)

			elif (pcclass1 == toee.stat_level_paladin):
				give_fighter_potion(pc)
				#give_scroll(pc, const_proto_potions.PROTO_POTION_OF_CURE_LIGHT_WOUNDS) # eagle splendor
				if (not make_new_weapon(pc)):
					give_scroll(pc, const_proto_potions.PROTO_POTION_OF_CURE_LIGHT_WOUNDS)

			elif (pcclass1 == toee.stat_level_ranger):
				give_fighter_potion(pc)
				if (not make_new_weapon(pc)):
					give_scroll(pc, const_proto_potions.PROTO_POTION_OF_CATS_GRACE)

			elif (pcclass1 == toee.stat_level_rogue):
				give_scroll(pc, const_proto_potions.PROTO_POTION_OF_CURE_LIGHT_WOUNDS)
				if (not make_new_weapon(pc)):
					give_scroll(pc, const_proto_potions.PROTO_POTION_OF_INVISIBILITY)

			elif (pcclass1 == toee.stat_level_sorcerer):
				give_scroll(pc, const_proto_scrolls.PROTO_SCROLL_OF_SCORCHING_RAY)
				give_used_wand(pc, const_proto_wands.PROTO_WAND_OF_MAGIC_MISSILES_1ST, 10)

			elif (pcclass1 == toee.stat_level_wizard):
				give_scroll(pc, const_proto_scrolls.PROTO_SCROLL_OF_WEB)
				#give_used_wand(pc, const_proto_wands.PROTO_WAND_OF_MAGE_ARMOR, 10)
				if (not utils_item.item_has(pc, const_proto_wands.PROTO_WAND_OF_DISRUPT_UNDEAD)):
					give_used_wand(pc, const_proto_wands.PROTO_WAND_OF_DISRUPT_UNDEAD, 50)
				else: give_used_wand(pc, const_proto_wands.PROTO_WAND_OF_MAGIC_MISSILES_1ST, 10)

			else:
				give_fighter_potion(pc)
				if (not make_new_weapon(pc)):
					give_scroll(pc, const_proto_potions.PROTO_POTION_OF_BULLS_STRENGTH)
		return

	def activate_encounter_k10(self):
		CtrlCryptLv1.give_treasure()
		#	import py06604_daemon_crypt_lv1
		#	py06604_daemon_crypt_lv1.CtrlCryptLv1.give_treasure()
		return

	def place_encounter_k11(self):
		p1 = self.create_promter_at(utils_obj.sec2loc(472, 478), self.get_dialogid_default(), 110, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Supply Vault", const_toee.rotation_0200_oclock)
		p2 = self.create_promter_at(utils_obj.sec2loc(481, 478), self.get_dialogid_default(), 110, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Supply Vault", const_toee.rotation_0700_oclock)
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

		if (1):
			loc = utils_obj.sec2loc(477, 478)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_WOODEN_MEDIUM, loc)
			if (chest):
				chest.move(loc, -8.485282, -8.485282)
				chest.rotation = math.radians(const_toee.rotation_grad_south_east)
				utils_trap.setup_trap(chest, const_traps.TRAP_POISON_DARTS, 6606)
				utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_SMALL_MASTERWORK_WOODEN, chest, 1, 1)
		return

	def display_encounter_k11(self):
		return
