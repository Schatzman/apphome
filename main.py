import time
import Tkinter as Tk
import traceback

WIN = Tk.Tk()
WIN.protocol('WM_DELETE_WINDOW', window_closed)
WIN.wm_title("Fucky Fun App")
WIN.resizable(0,0)

top = object

def window_closed():
    global WIN
    WIN.destroy()

def window_show():
    global WIN
    global top
    WIN.deiconify()
    top.destroy()

class AppGUI(object):

    def __init__(self):
        self.label_first_thing = Tk.Label(WIN, text="First thing:")
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

        self.button = Tk.Button(WIN,text="DO!",command=self.go_callback)
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
        global top
        top = self.top = Tk.Toplevel(parent)
        top.protocol('WM_DELETE_WINDOW', window_show)
        arg_str = ''
        for arg in args:
            arg_str += str(arg) + ' '
        arg_str = arg_str.strip()
        info = (
            arg_str +
            "\nIt is done."
            )

        Tk.Label(top, text=info).pack()

        button = Tk.Button(top, text="OK", command=self.ok)
        button.pack(pady=5)

    def ok(self):
        WIN.deiconify()
        self.top.destroy()

if __name__ == '__main__':
    gui_window = AppGUI()
