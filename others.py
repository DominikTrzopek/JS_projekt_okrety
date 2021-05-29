from tkinter import messagebox
import random

def make_dictionary(x,y,buttons,ship_list,banned,player=True):
    possible = set()
    for i in range(-3,4):
        if x+i >= 0 and x+i <=9 and ship_list[abs(i)] > 0:
            possible.add(buttons[x+i][y])
        if y+i >= 0 and y+i <= 9 and ship_list[abs(i)] > 0:
            possible.add(buttons[x][y+i])
    to_return = set()
    for i in possible:
        if i not in banned:
            to_return.add(i)
            if(player == True):
                i.configure(bg="grey")
    return to_return

def clear_dictionary(dictionary):
    for button in dictionary:
        button.configure(bg = '#DDDDDD')
    dictionary.clear()

def get_random(max):
    return random.randint(0,max)

def comm(text,tests):
    if tests == False:
        messagebox.showerror("Okrety", text)
    return -1