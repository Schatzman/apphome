#!/usr/bin/env python2.7
from pprint import pprint
import random
import sqlite3 as sql
import sys
import time
import Tkinter as Tk
import traceback
import yaml
# GUI 
# GAME LOGIC
# SAVE LOGIC
# 
########### BEGINNING OF GUI #################################################

DEBUG = False

WIN = Tk.Tk()
WIN.wm_title("Game 0000")
WIN.resizable(0,0)

TOP = object

def window_closed():
    global WIN
    WIN.destroy()

WIN.protocol('WM_DELETE_WINDOW', window_closed)

def window_show():
    global WIN
    global TOP
    WIN.deiconify()
    TOP.destroy()

class AppGUI(object):

    def __init__(self):
        self.label_first_thing = Tk.Label(WIN, text="Name:")
        self.label_first_thing.grid(row=0,column=0)

        self.first_thing_input = Tk.StringVar()
        self.first_thing_entry = Tk.Entry(WIN, textvariable=self.first_thing_input)
        self.first_thing_entry.grid(row=0,column=1)

        self.label_second_thing = Tk.Label(WIN, text="Second thing:")
        self.label_second_thing.grid(row=1,column=0)

        self.second_thing_input = Tk.StringVar()
        self.second_thing_entry = Tk.Entry(WIN, textvariable=self.second_thing_input)
        self.second_thing_entry.grid(row=1,column=1)

        self.check_var = Tk.IntVar()

        self.checkbutton_get_ref_list = Tk.Checkbutton(WIN, text="Checkbox?", variable=self.check_var)
        self.checkbutton_get_ref_list.grid(row=2,column=0)

        self.check_var2 = Tk.IntVar()

        self.checkbutton_get_2 = Tk.Checkbutton(WIN, text="Checkbox?", variable=self.check_var2)
        self.checkbutton_get_2.grid(row=3,column=0)

        self.button = Tk.Button(WIN,text="Create character",command=self.go_callback)
        self.button.grid(row=2,column=1)

        WIN.mainloop()

    def go_callback(self):
        self.create_dialog()

    def create_dialog(self):
        global WIN
        WIN.withdraw()
        args = [
            self.first_thing_input.get(),
            self.second_thing_input.get(),
            self.check_var.get()
        ]
        dialog = OpCompleteDialog(WIN, args)
        WIN.wait_window(dialog.top)


class OpCompleteDialog:

    def __init__(self, parent, args):
        global WIN
        global TOP
        global DEBUG
        TOP = self.top = Tk.Toplevel(parent)
        TOP.protocol('WM_DELETE_WINDOW', window_show)
        arg_str = ''
        for arg in args:
            arg_str += str(arg) + ' '
        arg_str = arg_str.strip()
        version_info = db_version()
        info = (
            arg_str +
            "\nIt is done." +
            "\nAlso..." +
            version_info
            )

        Tk.Label(TOP, text=info).pack()
        if DEBUG:
            print "Tk.Label packed."

        button = Tk.Button(TOP, text="OK", command=self.ok)
        button.pack(pady=5)

    def ok(self):
        WIN.deiconify()
        self.top.destroy()

########### END OF GUI #######################################################
##### DATABASE METHODS #######################################################


def db_version():
    sqlite = "\nSQLite Version: "
    version = sqlite + "Unknown"
    try:
        con = sql.connect('core.db')
        c = con.cursor()
        c.execute('SELECT SQLITE_VERSION()')
        version = sqlite + c.fetchone()[0]
    except sql.Error as e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()
    return version

def create_creature_table(db):
    commands = [
        'DROP TABLE IF EXISTS creatures;',
        '''CREATE TABLE IF NOT EXISTS creatures (
            date text,
            name text,
            description text,
            stats text,
            type text,
            id real
            );'''
    ]
    return db_commit(db, commands)

def create_area_table(db):
    commands = [
        'DROP TABLE IF EXISTS areas;',
        '''CREATE TABLE IF NOT EXISTS areas (
            date text,
            name text,
            description text,
            stats text,
            type text,
            id real
            );'''
    ]
    return db_commit(db, commands)

def db_call(db, commands, method):
    result = []
    try:
        con = sql.connect(db)
        c = con.cursor()
        try:
            for command in commands:
                c.execute(command)
            if method == 'commit':
                result = con.commit()
            elif method == 'fetch':
                result = c.fetchall()
        except:
            print traceback.format_exc()
    except:
        print traceback.format_exc()
    finally:
        if con:
            con.close()
        return result

def db_commit(db, commands):
    return db_call(db, commands, 'commit')

def db_query(db, queries):
    return db_call(db, queries, 'fetch')

def get_tables(db):
    queries = ["SELECT * FROM sqlite_master WHERE type='table';"]
    return db_query(db, queries)

########### END OF DB METHODS ################################################
########### BEGINNING OF GAME LOGIC ##########################################

class BaseObject(object):
    def __init__(self, name, description):
        self.id = 0
        self.name = name
        self.description = description
        self.type = 'base'


class Actor(BaseObject):
    def __init__(self, name, description, stats):
        super(Actor, self).__init__(name, description)
        self.type = 'being'
        self.total_xp = 0
        self.next_lvl_xp = 0
        self.next_lvl_xp_cap = 500
        self.level = 1
        self.stats = stats


class Area(BaseObject):
    def __init__(self, name, description):
        super(Area, self).__init__(name, description)
        self.type = 'place'


class GameEngine(object):
    def __init__(self):
        pass

def read_yaml(filename):
    stream = file(filename, 'r')
    result = yaml.load(stream)
    return result

def generate_stats(race, race_dict):
    stat_dict = {}
    if race in race_dict:
        for stat in race_dict[race]:
            stat_dict[stat] = race_dict[race][stat][0] + random.randint(0, race_dict[race][stat][1])
    return stat_dict

def create_creature(name, race, description, race_dict):
    stats = generate_stats(race, race_dict)
    creature = Actor(name, description, stats)
    creature.race = race
    return creature

def level_up(creature):
    creature.level += 1

def gain_exp(creature, xp, silent=False):
    creature.total_xp += xp
    creature.next_lvl_xp += xp
    if creature.next_lvl_xp >= creature.next_lvl_xp_cap:
        level_up(creature)
        if not silent:
            print (
                "%s leveled up! %s is now level %s." % (
                    creature.name,
                    creature.name,
                    str(creature.level)
                    )
                )
        creature.next_lvl_xp = 0
        creature.next_lvl_xp_cap += creature.next_lvl_xp_cap * 0.04
        if creature.level % 2 == 0:
            gain_attr(creature, silent)

def gain_attr(creature, silent=False):
    stat_ls = ['st','dx','cn','in','wi','ch']
    stat = random.randint(0, len(stat_ls) - 1)
    creature.stats[stat_ls[stat]] += 1
    if not silent:
        print (
            "%s's %s increased from %s to %s." % (
                creature.name,
                stat_ls[stat],
                creature.stats[stat_ls[stat]]-1,
                creature.stats[stat_ls[stat]]
                )
            )

def initiative_calculator(combatants):
    for combatant in combatants:
        self.combatant_dict[combatant.name]

def combat_round(attacker, defender):
    attack_roll = random.randint(0, attacker.stats['dx'])
    defense_roll = random.randint(0, defender.stats['dx'])
    if attack_roll > defense_roll:
        damage_roll = random.randint(0, attacker.stats['st'])
        soak_roll = (random.randint(0, defender.stats['cn'])) * 0.5
        damage = int((damage_roll - soak_roll) + 1)
        if damage < 0:
            damage = 0
        s = ''
        if damage != 1:
            s = 's'
        print ("%s hits %s for %s point%s of damage!" % (attacker.name, defender.name, str(damage), s))
    else:
        print ("%s misses %s!" % (attacker.name, defender.name))



########### END OF GAME LOGIC ################################################
########### BEGINNING OF SAVE LOGIC ##########################################

# code here


########### END OF SAVE LOGIC ################################################

# Instantiate the gui to start the app on script execution
if __name__ == '__main__':
    gui_window = AppGUI()
    player = Actor('HeroPerson','The hero of the day!')
    starting_location = Area('Valley of Trials','Where legends are born.')

    