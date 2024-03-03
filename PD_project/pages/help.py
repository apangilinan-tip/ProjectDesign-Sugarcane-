from tkinter import *

class HelpPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        label = Label(self, text="Help Page")
        label.pack(pady=10)

    def exit_app(self):
        self.master.destroy()
