import toee, debug, tpdp, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls, ctrl_behaviour
import const_proto_potions, utils_obj, const_proto_food, utils_npc, utils_target_list, const_proto_wands, utils_sneak, const_deseases, utils_npc_spells, utils_npc
import const_proto_items, const_proto_rings, const_proto_cloth, const_proto_wondrous, coe_consts

COE_ENCOUNTERS = 6603

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.enter_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_end_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.end_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_exit_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.exit_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_will_kos(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	print("will_kos({}, {})".format(attachee, triggerer))
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.will_kos(attachee, triggerer)
	else: print("san_will_kos ctrl not found")
	return toee.RUN_DEFAULT

class CtrlOrc(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14899

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		#utils_obj.obj_scripts_clear(npc)
		#npc.scripts[const_toee.sn_start_combat] = COE_ENCOUNTERS
		#npc.scripts[const_toee.sn_enter_combat] = COE_ENCOUNTERS

		# create inventory
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		item = utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_LEATHER_BOOTS_COMBAT, npc)
		if (item):
			item.item_flag_set(toee.OIF_NO_LOOT)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_FALCHION, npc)
		npc.item_wield_best_all()
		return

class CtrlWolf(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14050

class CtrlSkeletonEntry(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14186

class CtrlBeetleBombardier(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14768

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlBeetleBombardier, self).created(npc)
		# assign scripts
		#utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = COE_ENCOUNTERS
		npc.scripts[const_toee.sn_enter_combat] = COE_ENCOUNTERS

		npc.condition_add_with_args("Acid_Spray", 10, toee.dice_new("1d4+2").packed, 13)
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None
		if (1):
			m = utils_target_list.AITargetMeasure.by_all()
			m.measure_affected_range = 10
			m.measure_has_los = 1
			foes = utils_target_list.AITargetList(npc, 1, 0, m).rescan()
			target = foes.find_affected_best(1, 1)
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_clear_target()
			tac.add_target_closest()
			if (target and target.target):
				tac.add_target_obj(target.target.id)
				npc.turn_towards(target.target)
			tac.add_approach_single()
			tac.add_python_action(3010)
			tac.add_attack_threatened
			tac.add_ready_vs_approach()
		return tac

class CtrlShadow(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14828

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlShadow, self).created(npc)
		npc.condition_add_with_args("Monster_Ability_Drain_Su", 0, 0, toee.stat_strength, toee.dice_new("1d6").packed, 0)
		npc.condition_add("Monster_Touch_Attack")
		#npc.condition_add("Monster_No_Damage")
		npc.condition_add_with_args("Monster Damage Type", toee.D20DT_SUBDUAL)
		return

class CtrlGolemWoodKassen(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14895


class CtrlSkeletonHumanBloody(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14720
