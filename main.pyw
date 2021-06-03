from tkinter import *
import player

def start(cell_size = 30):
    """
    tworzenie root i uruchomienie aplikacji
    """
    root = Tk()
    player.Ships_app(cell_size,root)
    root.mainloop()

if __name__ == "__main__":
    start()
