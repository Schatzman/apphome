#!/usr/bin/env python3.4

import datetime
import json
import os
import pprint
import sys
import tkinter
import time
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def read_yaml(filename_yaml):
    stream = open(filename_yaml, 'r')
    data = yaml.load(stream, Loader=Loader)
    return data

class Window(object):
    def __init__(self):
        self.WIN = tkinter.Tk()
        self.prtcl_name = ''
        self.func = ''
        self.title = '' 
        self.xy = [0,0]
        self.config_file = 'pyapp.yaml'

    def window_closed(self):
        self.WIN.destroy()

    # this is to control conf options
    # DEFAULTS:
    # prtcl_name 'WM_DELETE_WINDOW'
    # func window_closed
    # title "Someone's titley string"
    # x 500
    # y 200
    def configure(self, prtcl_name, resize, func, title, x, y):
        self.WIN.protocol(prtcl_name, func)
        self.WIN.wm_title(title)
        self.WIN.resizable(x,y)

    def auto_configure(self):
        self.yaml_dump = read_yaml(self.config_file)
        cfg_data = self.yaml_dump
        prtcl_name = cfg_data["protocol"]
        resize = cfg_data["resizeable"]
        func = self.window_closed
        title = cfg_data["title"]
        x = cfg_data["width"]
        y = cfg_data["height"]
        self.configure(
            prtcl_name,
            resize,
            func,
            title,
            x,y
            )

class OpCompleteDialog:

    def __init__(self, main):

        top = self.top = tkinter.Toplevel(main)
        info = (
            "Operation complete. See " +
            "file_sys_verify_compare.log for details."
            )

        tkinter.Label(top, text=info).pack()

        button = tkinter.Button(top, text="OK", command=self.ok)
        button.pack(pady=5)

    def ok(self):
        main.WIN.deiconify()
        self.top.destroy()

class AppGUI(object):

    def __init__(self, main):
        self.label_dir_path = tkinter.Label(main.WIN, text="Full path to directory:")
        self.label_dir_path.grid(row=0,column=0)

        self.dir_path_input = tkinter.StringVar()
        self.dir_path_entry = tkinter.Entry(main.WIN, textvariable=self.dir_path_input)
        self.dir_path_entry.grid(row=0,column=1)

        self.label_compare_path = tkinter.Label(main.WIN, text="Path to reference file:")
        self.label_compare_path.grid(row=1,column=0)

        self.compare_path_input = tkinter.StringVar()
        self.compare_path_entry = tkinter.Entry(main.WIN, textvariable=self.compare_path_input)
        self.compare_path_entry.grid(row=1,column=1)

        self.check_var = tkinter.IntVar()

        self.checkbutton_get_ref_list = tkinter.Checkbutton(main.WIN, text="Collect reference file?", variable=self.check_var)
        self.checkbutton_get_ref_list.grid(row=2,column=0)

        self.button = tkinter.Button(main.WIN,text="GO!",command=self.go_callback)
        self.button.grid(row=2,column=1)
        self.main = main

        self.main.WIN.mainloop()

    #TODO
    #implement more buttons
    def go_callback(self):
        #do stuff
        self.create_dialog()
        self.conf_dialog()

    def create_dialog(self):
        self.POP = tkinter.Tk()

    def closed(self):
        print("CALLED CLOSED")
        self.POP.destroy()
        self.top.destroy()
        self.main.WIN.deiconify()
        self.main.WIN.destroy()

    def conf_dialog(self):
        self.POP.wm_title("Operation Complete")
        self.POP.resizable(0,0)
        self.POP.protocol("WM_DELETE_WINDOW", self.closed)
        self.main.WIN.withdraw()
        self.POP.withdraw()
        dialog = OpCompleteDialog(self.POP)
        self.POP.wait_window(dialog.top)

if __name__ == '__main__':
    main = Window()
    main.auto_configure()
    gui = AppGUI(main)