#!/usr/bin/env python2.7
import random
race_dict = {
	'human'    : {
	    'st':(9,3),
	    'dx':(8,3),
	    'cn':(8,3),			
	    'in':(8,3),
	    'wi':(7,3),
	    'ch':(8,3)
	    },
	'elf'      : {
	    'st':(8,3),
	    'dx':(9,4),
	    'cn':(7,2),
	    'in':(8,3),
	    'wi':(8,3),
	    'ch':(8,3)
	    },
	'dwarf'    : {
	    'st':(9,4),
	    'dx':(7,2),
	    'cn':(9,4),
	    'in':(8,3),
	    'wi':(8,3),
	    'ch':(7,2)
	    },
	'half-elf' : {
	    'st':(8,3),
	    'dx':(8,3),
	    'cn':(8,3),
	    'in':(8,3),
	    'wi':(8,3),
	    'ch':(8,3)
	    },
	'halfling' : {
	    'st':(6,4),
	    'dx':(9,4),
	    'cn':(9,5),
	    'in':(7,2),
	    'wi':(8,3),
	    'ch':(8,3)
	    },
	'gnome'    : {
	    'st':(7,2),
	    'dx':(9,4),
	    'cn':(8,3),
	    'in':(9,4),
	    'wi':(8,2),
	    'ch':(7,2)
	    }
}
def generate_stats(race, race_dict):
	stat_dict = {}
	if race in race_dict:
		for stat in race_dict[race]:
			stat_dict[stat] = race_dict[race][stat][0] + random.randint(0, race_dict[race][stat][1])
	return stat_dict
print generate_stats('elf', race_dict)

def level_up(creature):
	creature.level += 1

def gain_exp(creature, xp):
	creature.total_xp += xp
	creature.next_lvl_xp += xp
	if creature.next_lvl_xp >= creature.next_lvl_xp_cap:
		level_up(creature)
		creature.next_lvl_xp = 0
		creature.next_lvl_xp_cap += creature.next_lvl_xp_cap * 0.08

def attr_gain(creature):
	stat_ls = ['st','dx','cn','in','wi','ch']
	if creature.level % 3 == 0:
		stat = random.randint(0, len(stat_ls))
	creature.stats[stat_ls[stat]] += 1


