import toee, ctrl_behaviour, utils_item, utils_obj, const_toee, factions_zmod, utils_npc
import const_proto_armor, const_proto_weapon, const_proto_food, const_proto_cloth, const_proto_containers, const_proto_list_weapons, const_proto_list_scrolls

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
		hairStyle = utils_npc.HairStyle.from_npc(npc)
		if (npc.obj_get_int(toee.obj_f_critter_gender) == toee.gender_female):
			hairStyle.style = const_toee.hair_styles_human_woman[toee.game.random_range(0, len(const_toee.hair_styles_human_woman)-1)]
		else: hairStyle.style = const_toee.hair_styles_human_gentleman[toee.game.random_range(0, len(const_toee.hair_styles_human_gentleman)-1)]
		hairStyle.color = const_toee.hair_colors_human[toee.game.random_range(0, len(const_toee.hair_colors_human)-1)]
		hairStyle.update_npc(npc)
		# make hair style
		# make hair color

		# make height
		return

	def dress_up(self, npc):
		# create inventory
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, npc, 1, 1)
		robe = toee.game.random_range(const_proto_cloth.PROTO_CLOTH_GARB_VILLAGER_BLUE, const_proto_cloth.PROTO_CLOTH_GARB_VILLAGER_RED)
		if (robe):
			utils_item.item_create_in_inventory(robe, npc, 1, 1)
		if (npc.obj_get_int(toee.obj_f_critter_gender) == toee.gender_male):
			cloak = const_proto_cloth.PROTO_CLOAKS[toee.game.random_range(0, len(const_proto_cloth.PROTO_CLOAKS)-1)]
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
