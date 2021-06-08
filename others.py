from tkinter import messagebox
import random

def make_set(x,y,buttons,ship_list,banned,player=True):
    """
    tworzy zbiór składający się z pól na których może zostać umieszczony okręt
    x,y - koordynaty pola
    ship_list - lista zawierająca informację o okrętach pozostałych do rozmieszczenia
    banned - zbiór niedozwolonych pól
    player - zmienna decydującą o tym czy zmieniać kolor przeycisków należących do tworzonego zbioru
    zwraca utworzony zbiór
    """
    possible = set()
    for i in range(-3,4):
        if x+i >= 0 and x+i <=9 and ship_list[abs(i)] > 0:
            possible.add(buttons[x+i][y])
        if y+i >= 0 and y+i <= 9 and ship_list[abs(i)] > 0:
            possible.add(buttons[x][y+i])
    to_return = set(i for i in possible if i not in banned)
    for i in possible:
        if i not in banned:
            if(player == True):
                i.configure(bg="grey")
    return to_return

def clear_set(set_to_clear):
    """
    czyści zbiór
    set_to_clear - zbiór do wyczyszczenia
    """
    for button in set_to_clear:
        button.configure(bg = '#DDDDDD')
    set_to_clear.clear()

def get_random(max):
    """
    zwraca losowa liczbe z przedziału 0, max
    """
    return random.randint(0,max)

def comm(text,tests):
    """
    wyświetla komunikaty o błędzie
    """
    if tests == False:
        messagebox.showerror("Okrety", text)
    return -1
