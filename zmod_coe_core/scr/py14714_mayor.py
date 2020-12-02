import toee, ctrl_behaviour, utils_item, utils_obj, const_toee, factions_zmod
import const_proto_armor, const_proto_weapon, const_proto_food, const_proto_cloth, const_proto_containers, const_proto_list_weapons, const_proto_list_scrolls
import utils_storage

def san_dialog(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.dialog(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.heartbeat(attachee, triggerer)
	return toee.RUN_DEFAULT

def cvm():
	o = utils_storage.obj_storage_by_alias(CtrlVillageMayor.get_alias())
	if (not o): return None
	if (CtrlVillageMayor.get_name() in o.data):
		result = o.data[CtrlVillageMayor.get_name()]
	else: return None
	return result

class CtrlVillageMayor(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14714

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_dialog] = self.get_proto_id()
		npc.scripts[const_toee.sn_heartbeat] = self.get_proto_id()
		npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)

		utils_item.item_clear_all(npc)

		# create inventory
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, npc, 1, 1)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_GARB_NOBLE_PURPLE, npc, 1, 1)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_LEATHER_BOOTS_WHITE, npc, 1, 1)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOAK_VIOLET, npc, 1, 1)
		
		npc.item_wield_best_all()

		self.vars["shout_mode"] = 1
		self.vars["shout_cooldown"] = 0
		return

	def dialog(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		assert isinstance(triggerer, toee.PyObjHandle)

		self.vars["shout_mode"] = 0
		attachee.turn_towards(triggerer)
		if not attachee.has_met(triggerer):
			triggerer.begin_dialog(attachee, 1)
			return toee.SKIP_DEFAULT
		else:
			triggerer.begin_dialog(attachee, 100)
		return toee.SKIP_DEFAULT

	def heartbeat(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		assert isinstance(triggerer, toee.PyObjHandle)

		if (self.get_var("shout_mode")):
			shout_cooldown = self.get_var("shout_cooldown")
			shout_cooldown += -1
			if (shout_cooldown <= 0):
				shout_cooldown = 5
				attachee.float_line(toee.game.random_range(1, 2), triggerer)
				attachee.rotation = const_toee.rotation_1100_oclock / 11 * toee.game.random_range(0, 11)

			self.vars["shout_cooldown"] = shout_cooldown

		return toee.RUN_DEFAULT

	@classmethod
	def get_alias(self):
		return "mayor_uptal"
