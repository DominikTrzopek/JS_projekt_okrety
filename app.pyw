from tkinter import *
import main

def main_window(cell_size):
    """
    fukcja uruchamiająca funkcję start (właściwą aplikację) z modułu main,
    cell_size - wielkość pojedyńczej komórki
    """
    main.start(cell_size)
    

#tworzenie okna do wyboru rozdzielczości
option_window = Tk()
option_window.title("Opcje")
option_window.geometry("240x380")
#tworzenie etykiety "Wybierz rozdzielczość okna"
show_text = Label(option_window, text="Wybierz rozdzielczość okna")
show_text.place(x = 20)
show_text.config(font = ("Arial",12))
#tworzenie przycisków 
button1 = Button(option_window,text = "450x575",command= lambda: [option_window.destroy(),main_window(25)])
button1.place(x = 30, y = 35, width = 180, height = 100)

button2 = Button(option_window,text = "540x690",command= lambda: [option_window.destroy(),main_window(30)])
button2.place(x = 30, y = 150, width = 180, height = 100)

button3 = Button(option_window,text = "630x805",command= lambda: [option_window.destroy(),main_window(35)])
button3.place(x = 30, y = 265, width = 180, height = 100)

option_window.mainloop()
