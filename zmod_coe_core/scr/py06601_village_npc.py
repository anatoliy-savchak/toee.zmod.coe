import toee, ctrl_behaviour, utils_item, utils_obj, const_toee, factions_zmod
import const_proto_armor, const_proto_weapon, const_proto_food, const_proto_cloth

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
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

class CtrlVillageSmith(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14587 #Dwarf Warrior

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_dialog] = VILLAGE_NPC_DIALOG
		npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)

		utils_item.item_clear_all(npc)

		# create inventory
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_COAT_LONG_BLACK, npc, 1, 1)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_LEATHER_BOOTS_BLACK, npc, 1, 1)
		
		npc.item_wield_best_all()
		return

	def dialog(self, attachee, triggerer):
		return toee.RUN_DEFAULT
