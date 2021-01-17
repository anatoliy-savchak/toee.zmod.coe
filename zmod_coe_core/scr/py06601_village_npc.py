import toee, ctrl_behaviour, utils_item, utils_obj, const_toee, factions_zmod, utils_npc, const_animate
import const_proto_armor, const_proto_weapon, const_proto_food, const_proto_cloth, const_proto_containers, const_proto_list_weapons, const_proto_list_scrolls, const_proto_list_cloth
import random

VILLAGE_NPC_DIALOG = 6601

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_dialog(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.dialog(attachee, triggerer)
	return toee.RUN_DEFAULT

class CtrlVillagePersonRandom(ctrl_behaviour.CtrlBehaviour):
	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		#npc.scripts[const_toee.sn_dialog] = VILLAGE_NPC_DIALOG
		npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)
		utils_item.item_clear_all(npc)

		self.make_up(npc)
		self.dress_up(npc)
		return

	def make_up(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		gender = npc.obj_get_int(toee.obj_f_critter_gender)
		hairStyle = utils_npc.HairStyle.from_npc(npc)
		if (gender == toee.gender_female):
			hairStyle.style = const_toee.hair_styles_human_woman[toee.game.random_range(0, len(const_toee.hair_styles_human_woman)-1)]
		else: hairStyle.style = const_toee.hair_styles_human_gentleman[toee.game.random_range(0, len(const_toee.hair_styles_human_gentleman)-1)]
		hairStyle.color = const_toee.hair_colors_human[toee.game.random_range(0, len(const_toee.hair_colors_human)-1)]
		hairStyle.update_npc(npc)

		# need to recheck
		if (0):
			height = 100
			if (gender == toee.gender_female):
				height = int(160/180*100 - 20 + toee.game.random_range(1, 20))
			else:
				height = int(100 - 20 + toee.game.random_range(1, 20))
			npc.obj_set_int(toee.obj_f_critter_height, height)
		return

	def dress_up(self, npc):
		# create inventory
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, npc, 1, 1)
		robe = toee.game.random_range(const_proto_cloth.PROTO_CLOTH_GARB_VILLAGER_BLUE, const_proto_cloth.PROTO_CLOTH_GARB_VILLAGER_RED)
		if (robe):
			utils_item.item_create_in_inventory(robe, npc, 1, 1)
		if (npc.obj_get_int(toee.obj_f_critter_gender) == toee.gender_male):
			cloak = const_proto_list_cloth.PROTO_CLOTH_CLOAKS[toee.game.random_range(0, len(const_proto_list_cloth.PROTO_CLOTH_CLOAKS)-1)]
			if (cloak):
				utils_item.item_create_in_inventory(cloak, npc, 1, 1)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_LEATHER_BOOTS_BLACK, npc, 1, 1)
		npc.item_wield_best_all()
		return

class CtrlVillageManRandom(CtrlVillagePersonRandom):
	@classmethod
	def get_proto_id(cls):
		return 14702

class CtrlVillageWomanRandom(CtrlVillagePersonRandom):
	@classmethod
	def get_proto_id(cls):
		return 14703

class CtrlVillageAnimal(ctrl_behaviour.CtrlBehaviour):
	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		utils_obj.obj_scripts_clear(npc)
		utils_item.item_clear_all(npc)
		npc.faction_add(factions_zmod.FACTION_WILDERNESS_INDIFFERENT)
		return

class CtrlVillageAnimalPig(CtrlVillageAnimal):
	@classmethod
	def get_proto_id(cls):
		return 14368

class CtrlVillageAnimalChecken(CtrlVillageAnimal):
	@classmethod
	def get_proto_id(cls):
		return 14362

class CtrlVillageAnimalFarmDog(CtrlVillageAnimal):
	@classmethod
	def get_proto_id(cls):
		return 14048

class VillagePlaces:
	TAVERN_PORCH = (488, 466) # 10 ft before entrance
	TAVERN_DOORSTEP = (488, 463) # 0 ft before entrance
	TAVERN_ENTRY = (488, 461) # 5 ft after entrance
	BORDER_WEST_ENTRY = (505, 472) # 5 ft after west (of tavern) border
	VILLAGE_SQUARE_WEST_ENTRANCE = (492, 470) # 5 ft after far west (of fontain)
	VILLAGE_SQUARE_NORTH_ENTRANCE = (469, 464) # 5 ft after far north (of fontain)
	VILLAGE_SQUARE_SOUTH_ENTRANCE = (469, 497) # 5 ft after far south (of fontain)
	VILLAGE_SQUARE_CORNER_WEST_NORTH = (492, 464)
	VILLAGE_SQUARE_CORNER_WEST_SOUTH = (493, 389)
	VILLAGE_SQUARE_CORNER_EAST_NORTH = (465, 464)
	VILLAGE_SQUARE_CORNER_EAST_SOUTH = (465, 491)
	CHURCH_PORCH = (494, 487) # 10 ft before entrance
	CHURCH_DOORSTEP = (494, 490) # 0 ft before entrance
	CHURCH_ENTRY = (493, 492) # 5 ft after entrance
	CHURCH_CORNER_WEST_NORTH = (498, 491) 
	CHURCH_CORNER_EAST_NORTH = (490, 491) 
	CHURCH_CORNER_AISLE_WEST_SOUTH = (498, 501) 
	CHURCH_CORNER_AISLE_EAST_SOUTH = (490, 501) 
	CHURCH_TRANSEPT_CENTER = (495, 502)

	GENERAL_STORE_PORCH = (479, 493) # 10 ft before entrance
	GENERAL_STORE_DOORSTEP = (479, 496) # 0 ft before entrance
	GENERAL_STORE_ENTRY = (479, 498) # 5 ft after entrance
	GENERAL_STORE_STAND_1 = (483, 498)
	GENERAL_STORE_STAND_2 = (476, 499)
	GENERAL_STORE_STAND_3 = (483, 501)
	GENERAL_STORE_BEFORE_COUNTER = (478, 504)

	@staticmethod
	def scene_church_prey(wp, num):
		assert isinstance(wp, list)
		assert isinstance(num, int)
		wp.append(utils_npc.Waypoint(VillagePlaces.CHURCH_PORCH[0], VillagePlaces.CHURCH_PORCH[1], const_toee.rotation_0500_oclock, 0))
		wp.append(utils_npc.Waypoint(VillagePlaces.CHURCH_TRANSEPT_CENTER[0], VillagePlaces.CHURCH_TRANSEPT_CENTER[1], const_toee.rotation_0500_oclock, 5000, utils_npc.WaypointFlag.Delay | utils_npc.WaypointFlag.Animate \
			, 32 + const_animate.NormalAnimType.Conceal, 32 + const_animate.NormalAnimType.ConcealIdle, 32 + const_animate.NormalAnimType.Unconceal))

		x, y = VillagePlaces.get_random_church_stand()
		wp.append(utils_npc.Waypoint(x, y, const_toee.rotation_0500_oclock, 5000, utils_npc.WaypointFlag.Delay | utils_npc.WaypointFlag.Animate | utils_npc.WaypointFlag.FixedRotation \
			, 32 + const_animate.NormalAnimType.Examine, 32 + const_animate.NormalAnimType.FeatTrack))
		return

	@staticmethod
	def get_random_store_stand():
		r = toee.game.random_range(1, 3)
		if (r == 2): return VillagePlaces.GENERAL_STORE_STAND_2
		if (r == 3): return VillagePlaces.GENERAL_STORE_STAND_3
		return VillagePlaces.GENERAL_STORE_STAND_1

	@staticmethod
	def get_random_church_stand():
		x = VillagePlaces.CHURCH_CORNER_AISLE_EAST_SOUTH[0] - 1 + toee.game.random_range(1, VillagePlaces.CHURCH_CORNER_AISLE_WEST_SOUTH[0] - VillagePlaces.CHURCH_CORNER_AISLE_EAST_SOUTH[0])
		y = VillagePlaces.CHURCH_CORNER_EAST_NORTH[1] - 1 + toee.game.random_range(1, VillagePlaces.CHURCH_CORNER_AISLE_EAST_SOUTH[1] - VillagePlaces.CHURCH_CORNER_EAST_NORTH[1])
		return x, y

	@staticmethod
	def scene_general_store(wp, num):
		assert isinstance(wp, list)
		assert isinstance(num, int)
		wp.append(utils_npc.Waypoint(VillagePlaces.GENERAL_STORE_PORCH[0], VillagePlaces.GENERAL_STORE_PORCH[1], const_toee.rotation_0500_oclock, 0))
		stand_count_to_examine = toee.game.random_range(1, 10)
		#stand_count_to_examine = 3
		for i in range(1, stand_count_to_examine):
			stand_coords = VillagePlaces.get_random_store_stand()
			wp.append(utils_npc.Waypoint(stand_coords[0], stand_coords[1], const_toee.rotation_0500_oclock, 1000, utils_npc.WaypointFlag.Delay | utils_npc.WaypointFlag.Animate | utils_npc.WaypointFlag.FixedRotation \
				, 32 + const_animate.NormalAnimType.Examine))

		wp.append(utils_npc.Waypoint(VillagePlaces.GENERAL_STORE_BEFORE_COUNTER[0], VillagePlaces.GENERAL_STORE_BEFORE_COUNTER[1], const_toee.rotation_0500_oclock, 1000, utils_npc.WaypointFlag.Delay | utils_npc.WaypointFlag.Animate | utils_npc.WaypointFlag.FixedRotation \
			, 32 + const_animate.NormalAnimType.Picklock))
		return

	@staticmethod
	def scene_wander_square(wp, num):
		assert isinstance(wp, list)
		assert isinstance(num, int)
		for i in range(0, toee.game.random_range(5, 10)):
			stand_coords = VillagePlaces.get_random_sqare_place()
			wp.append(utils_npc.Waypoint(stand_coords[0], stand_coords[1], const_toee.rotation_0500_oclock, 5000 * toee.game.random_range(1, 10), utils_npc.WaypointFlag.Delay | utils_npc.WaypointFlag.Animate \
				, 32 + const_animate.NormalAnimType.Examine))
		return

	@staticmethod
	def get_random_sqare_place():
		x = VillagePlaces.VILLAGE_SQUARE_CORNER_EAST_NORTH[0] - 1 + toee.game.random_range(1, VillagePlaces.VILLAGE_SQUARE_CORNER_WEST_NORTH[0] - VillagePlaces.VILLAGE_SQUARE_CORNER_EAST_SOUTH[0])
		y = VillagePlaces.VILLAGE_SQUARE_CORNER_WEST_NORTH[1] - 1 + toee.game.random_range(1, VillagePlaces.VILLAGE_SQUARE_CORNER_EAST_SOUTH[1] - VillagePlaces.VILLAGE_SQUARE_CORNER_WEST_NORTH[1])
		if (x >= 473 and x <= 478 and y >= 477 and y <= 482):
			return VillagePlaces.get_random_sqare_place()
		return x, y

class CtrlVillageRandomWanderer(CtrlVillagePersonRandom):
	def make_day_route(self, npc):
		crowd_place = self.get_var("crowd_place")
		waypoints = list()
		if (not crowd_place is None):
			waypoints.append(utils_npc.Waypoint(crowd_place[0], crowd_place[1], const_toee.rotation_0500_oclock, 1000 * toee.game.random_range(1, 10), utils_npc.WaypointFlag.Delay | utils_npc.WaypointFlag.FixedRotation))
		else:
			x, y = VillagePlaces.get_random_sqare_place()
			waypoints.append(utils_npc.Waypoint(x, y, const_toee.rotation_1100_oclock, 1000 * toee.game.random_range(1, 10), utils_npc.WaypointFlag.Delay))

			VillagePlaces.scene_wander_square(waypoints, 1)
			steps = list(range(3))
			steps_random = random.sample(steps, len(steps))
			for step in steps_random:
				if (step == 0):
					VillagePlaces.scene_wander_square(waypoints, 1)
				elif (step == 1):
					VillagePlaces.scene_church_prey(waypoints, 1)
				elif (step == 2):
					VillagePlaces.scene_general_store(waypoints, 1)

		npc.npc_waypoints_set(waypoints)
		npc.npc_flag_set(toee.ONF_WAYPOINTS_DAY)
		npc.npc_flag_unset(toee.ONF_WAYPOINTS_NIGHT)
		return

	@classmethod
	def get_proto_id(cls):
		if (toee.game.random_range(0, 1)): return 14702 # man
		return 14703 # woman

class CtrlVillageWandererWoman(CtrlVillageRandomWanderer):
	@classmethod
	def get_proto_id(cls):
		return 14703