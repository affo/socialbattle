# Algorithms taken from http://www.gamefaqs.com/ps2/459841-final-fantasy-xii/faqs/45900
LEVEL_BONUS = {
	1: {'HP': (10, 11), 'MP': (3, 5)},
	2: {'HP': (11, 13), 'MP': (3, 5)},
	3: {'HP': (12, 14), 'MP': (3, 5)}, 
	4: {'HP': (13, 15), 'MP': (3, 5)},
	5: {'HP': (14, 16), 'MP': (3, 5)},
	6: {'HP': (15, 17), 'MP': (3, 5)},
	7: {'HP': (16, 19), 'MP': (3, 5)},
	8: {'HP': (17, 20), 'MP': (3, 5)},
	9: {'HP': (18, 21), 'MP': (3, 5)},
	10: {'HP': (19, 22), 'MP': (3, 5)},
	11: {'HP': (20, 23), 'MP': (4, 7)},
	12: {'HP': (21, 25), 'MP': (4, 7)},
	13: {'HP': (22, 26), 'MP': (4, 7)},
	14: {'HP': (23, 27), 'MP': (4, 7)},
	15: {'HP': (24, 28), 'MP': (4, 7)},
	16: {'HP': (25, 29), 'MP': (4, 7)},
	17: {'HP': (26, 31), 'MP': (4, 7)},
	18: {'HP': (27, 32), 'MP': (4, 7)},
	19: {'HP': (28, 33), 'MP': (4, 7)},
	20: {'HP': (29, 34), 'MP': (4, 7)},
	21: {'HP': (30, 35), 'MP': (4, 7)},
	22: {'HP': (31, 37), 'MP': (4, 7)},
	23: {'HP': (32, 38), 'MP': (4, 7)},
	24: {'HP': (33, 39), 'MP': (4, 7)},
	25: {'HP': (34, 40), 'MP': (4, 7)},
	26: {'HP': (33, 39), 'MP': (4, 7)},
	27: {'HP': (32, 38), 'MP': (4, 7)},
	28: {'HP': (31, 37), 'MP': (4, 7)},
	29: {'HP': (30, 35), 'MP': (4, 7)},
	30: {'HP': (29, 34), 'MP': (5, 9)},
	31: {'HP': (28, 33), 'MP': (5, 9)},
	32: {'HP': (27, 32), 'MP': (5, 9)},
	33: {'HP': (26, 31), 'MP': (5, 9)},
	34: {'HP': (25, 29), 'MP': (5, 9)},
	35: {'HP': (27, 32), 'MP': (5, 9)},
	36: {'HP': (29, 34), 'MP': (5, 9)},
	37: {'HP': (31, 37), 'MP': (5, 9)},
	38: {'HP': (33, 39), 'MP': (5, 9)},
	39: {'HP': (35, 41), 'MP': (5, 9)},
	40: {'HP': (37, 44), 'MP': (5, 9)},
	41: {'HP': (39, 46), 'MP': (5, 9)},
	42: {'HP': (41, 49), 'MP': (5, 9)},
	43: {'HP': (43, 51), 'MP': (5, 9)},
	44: {'HP': (45, 53), 'MP': (4, 7)},
	45: {'HP': (47, 56), 'MP': (4, 7)},
	46: {'HP': (49, 58), 'MP': (4, 7)},
	47: {'HP': (51, 61), 'MP': (4, 7)},
	48: {'HP': (53, 63), 'MP': (4, 7)},
	49: {'HP': (55, 65), 'MP': (4, 7)},
	50: {'HP': (53, 63), 'MP': (4, 7)},
	51: {'HP': (51, 61), 'MP': (4, 7)},
	52: {'HP': (49, 58), 'MP': (4, 7)},
	53: {'HP': (47, 56), 'MP': (4, 7)},
	54: {'HP': (45, 53), 'MP': (4, 7)},
	55: {'HP': (43, 51), 'MP': (4, 7)},
	56: {'HP': (41, 49), 'MP': (4, 7)},
	57: {'HP': (39, 46), 'MP': (4, 7)},
	58: {'HP': (37, 44), 'MP': (4, 7)},
	59: {'HP': (35, 41), 'MP': (4, 7)},
	60: {'HP': (33, 39), 'MP': (4, 7)},
	61: {'HP': (31, 37), 'MP': (3, 5)},
	62: {'HP': (29, 34), 'MP': (3, 5)},
	63: {'HP': (27, 32), 'MP': (3, 5)},
	64: {'HP': (25, 29), 'MP': (3, 5)},
	65: {'HP': (23, 27), 'MP': (3, 5)},
	66: {'HP': (21, 25), 'MP': (3, 5)},
	67: {'HP': (19, 22), 'MP': (3, 5)},
	68: {'HP': (20, 23), 'MP': (3, 5)},
	69: {'HP': (21, 25), 'MP': (3, 5)},
	70: {'HP': (22, 26), 'MP': (3, 5)},
	71: {'HP': (23, 27), 'MP': (3, 5)},
	72: {'HP': (24, 28), 'MP': (3, 5)},
	73: {'HP': (25, 29), 'MP': (3, 5)},
	74: {'HP': (26, 31), 'MP': (3, 5)},
	75: {'HP': (27, 32), 'MP': (3, 5)},
	76: {'HP': (28, 33), 'MP': (3, 5)},
	77: {'HP': (29, 34), 'MP': (3, 5)},
	78: {'HP': (30, 35), 'MP': (3, 5)},
	79: {'HP': (31, 37), 'MP': (3, 5)},
	80: {'HP': (32, 38), 'MP': (3, 5)},
	81: {'HP': (33, 39), 'MP': (2, 3)},
	82: {'HP': (34, 40), 'MP': (2, 3)},
	83: {'HP': (35, 41), 'MP': (2, 3)},
	84: {'HP': (36, 43), 'MP': (2, 3)},
	85: {'HP': (37, 44), 'MP': (2, 3)},
	86: {'HP': (38, 45), 'MP': (2, 3)},
	87: {'HP': (39, 46), 'MP': (2, 3)},
	88: {'HP': (40, 47), 'MP': (2, 3)},
	89: {'HP': (41, 49), 'MP': (2, 3)},
	90: {'HP': (42, 50), 'MP': (2, 3)},
	91: {'HP': (43, 51), 'MP': (1, 1)},
	92: {'HP': (44, 52), 'MP': (1, 1)},
	93: {'HP': (45, 53), 'MP': (1, 1)},
	94: {'HP': (46, 55), 'MP': (1, 1)},
	95: {'HP': (47, 56), 'MP': (1, 1)},
	96: {'HP': (48, 57), 'MP': (1, 1)},
	97: {'HP': (49, 58), 'MP': (1, 1)},
	98: {'HP': (50, 59), 'MP': (1, 1)},
	99: {'HP': (51, 61), 'MP': (1, 1)},
}

# stat: (BASE, MODIFIER)
BASE_STATS = {
	'HP': (46, 1.48),
	'MP': (45, 0.54),
	'STR': (23, 70),
	'MAG': (20, 57),
	'SPD': (24, 18),
	'VIT': (24, 48),
}

# CS-MOD, character's speed modifier
# spd: cs-mod
CS_MOD = {
	1: 0.136,
	2: 0.136,
	3: 0.136,
	4: 0.136,
	5: 0.136,
	6: 0.136,
	7: 0.136,
	8: 0.136,
	9: 0.136,
	10: 0.136,
	11: 0.136,
	12: 0.136,
	13: 0.136,
	14: 0.136,
	15: 0.136,
	16: 0.136,
	17: 0.136, 
	18: 0.136,
	19: 0.136,
	20: 0.136,
	21: 0.136,
	22: 0.136,
	23: 0.136,
	23: 0.136,
	24: 0.133,
	25: 0.133,
	26: 0.130,
	27: 0.130,
	28: 0.130,
	29: 0.127,
	30: 0.127,
	31: 0.127,
	32: 0.124,
	33: 0.124,
	34: 0.124,
	35: 0.124,
	36: 0.124,
	37: 0.121,
	38: 0.121,
	39: 0.121,
	40: 0.121,
	41: 0.119,
	42: 0.119,
	43: 0.119,
	44: 0.119,
	45: 0.119,
	46: 0.119,
	47: 0.116,
	48: 0.116,
	49: 0.116,
	50: 0.116,
	51: 0.116,
	52: 0.116,
	53: 0.116,
	54: 0.116,
	55: 0.116,
	56: 0.116,
	57: 0.113,
	58: 0.113,
	59: 0.113,
	60: 0.113,
	61: 0.113,
	62: 0.113,
	63: 0.113,
	64: 0.113,
	65: 0.113,
	66: 0.113,
	67: 0.113,
	68: 0.113,
	69: 0.113,
	70: 0.113,
	71: 0.113,
	72: 0.113,
	73: 0.110,
	74: 0.110,
	75: 0.110,
	76: 0.110,
	77: 0.110,
	78: 0.110,
	79: 0.110,
	80: 0.110,
	81: 0.110,
	82: 0.110,
	83: 0.110,
	84: 0.110,
	85: 0.110,
	86: 0.110,
	87: 0.110,
	88: 0.110,
	89: 0.110,
	90: 0.110,
	91: 0.110,
	92: 0.110,
	93: 0.110,
	94: 0.107,
	95: 0.107,
	96: 0.107,
	97: 0.107,
	98: 0.107,
	99: 0.107,
}
from socialbattle.api.models import Ability
PHYSICAL = Ability.ELEMENTS[6][0]
WHITE = Ability.ELEMENTS[5][0]

import random
# MAX HP/MP = (Base HP/MP + Sum of HP/MP Bonus up to this level) x HP/MP Modifier
# Other stats =Base + (Level x Modifier)/128
def get_stat(level, stat):
	if stat == 'HP' or stat == 'MP':
		def reduce_function(accum, level):
			lo = LEVEL_BONUS[level][stat][0]
			high = LEVEL_BONUS[level][stat][1]
			return accum + random.randint(lo, high)

		r = range(1, level)
		bonuses = reduce(reduce_function, r)
		new_stat = (BASE_STATS[stat][0] + bonuses) * BASE_STATS[stat][1]
	else:
		new_stat = BASE_STATS[stat][0] + (level * BASE_STATS[stat][1]) / 128
	return int(round(new_stat))

# Exp = 0.1*Lv^4 + 4.2*Lv^3 + 6.1*Lv^2 + 1.4*Lv - 11.4
def get_exp(level):
	exp = 0.1 * level**4 + 4.2 * level**3 + 6.1 * level**2 + 1.4 * level - 11.4
	return int(round(exp))

# if physical:
# 	DMG = [ATK x RANDOM(1~1.125) - DEF] x [1 + STR x (Lv+STR)/256]
# if black:
# 	DMG = [POW x RANDOM(1~1.125) - MDEF] x [2 + MAG x (Lv+MAG)/256)]
# if white:
# 	HEAL = POW x RANDOM(1~1.125) x [2 + MAG x (Lv+MAG)/256)]
def calculate_damage(attacker, attacked, ability):
	if ability.element == PHYSICAL:
		dmg = (attacker.atk * random.uniform(1, 1.125) - attacked.defense) \
				* (1 + attacker.stre * (attacker.level + attacker.stre) / 256)
		if dmg < 0:
			dmg = 0
	elif ability.element == WHITE:
		dmg = - (ability.power * random.uniform(1, 1.125)) \
			* (2 + attacker.mag * (attacker.level + attacker.mag) / 256)
	else:
		dmg = (ability.power * random.uniform(1, 1.125) - attacked.mdefense) \
			* (2 + attacker.mag * (attacker.level + attacker.mag) / 256)
		if dmg < 0:
			dmg = 0

	return int(round(dmg))

# Charge Time = [CT x CS-MOD + RAN0.5] x L-MOD x B-MOD x ST-MOD
# We will ignore L-MOB, B-MOD and ST-MOD
def get_charge_time(attacker, item_or_ability):
	if not item_or_ability:
		ctf = 26 #means 'unarmed'... as ffxii does
	else:
		ctf = item_or_ability.ctf
	cs_mod = CS_MOD[attacker.spd]
	return ctf * cs_mod * random.uniform(0, 0.5)