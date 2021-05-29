from tkinter import *
import player

def start(cell_size):
    root = Tk()
    player.Ships_app(cell_size,root)
    root.mainloop()