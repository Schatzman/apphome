#!/usr/bin/env python2.7
import sqlite3 as sql
import sys
import time
import Tkinter as Tk
import traceback

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


########### END OF GUI #######################################################
########### BEGINNING OF GAME LOGIC ##########################################

class BaseObject(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.stats = {}
        self.type = 'base'

class Actor(BaseObject):
    def __init__(self, name, description):
        super(Actor, self).__init__(name, description)
        self.type = 'being'

class Area(BaseObject):
    def __init__(self, name, description):
        super(Area, self).__init__(name, description)
        self.type = 'place'


########### END OF GAME LOGIC ################################################
########### BEGINNING OF SAVE LOGIC ##########################################

# code here


########### END OF SAVE LOGIC ################################################

# Instantiate the gui to start the app on script execution
if __name__ == '__main__':
    gui_window = AppGUI()
    player = Actor('HeroPerson','The hero of the day!')
    starting_location = Area('Valley of Trials','Where legends are born.')

    