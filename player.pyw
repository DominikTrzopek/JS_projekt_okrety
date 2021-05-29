from tkinter import *
from tkinter import ttk
import random
import others
import ai

class Ships_app():
    def __init__(self,cell_size,root, tests = False):
        self.row_number = 23
        self.column_number = 18
        self.cell_size = cell_size
        self.click_count = 0
        self.click_x = 0
        self.click_y = 0
        self.possible_tiles = set()
        self.taken_tiles = set()
        self.banned_tiles = set()
        self.fired_at = set()
        self.game_started = False
        self.who_start = others.get_random(9)
        self.destroyed = 0
        self.skip = False
        self.tests = tests

        #tworzenie okna
        self.game_window = root
        self.game_window.title("Okrety")

        #tworzenie siatki na przyciski
        self.frame = ttk.Frame(self.game_window, width=self.cell_size*self.column_number, height=self.cell_size*self.row_number)
        self.frame.grid_propagate(False)
        for x in range(0,self.row_number):
            self.frame.rowconfigure(x, minsize=self.cell_size, weight = 1)
        for x in range(0,self.column_number):
            self.frame.columnconfigure(x, minsize=self.cell_size, weight = 1)
        self.frame.grid(row = 0, column = 0)

        #dodanie przycisków  
        self.button_grid_player = self.button_array(11,self.place_ships)
        self.button_grid_enemy = self.button_array(0,self.attack_enemy)          
        #numeracja wierszy i kolumn
        self.numerate_array()

        #przyciski start i reset
        self.game_font = ("Arial",int(self.cell_size/3))
        self.start_button = Button(self.frame,width=10,font = self.game_font,text = "start",borderwidth = 3,command= lambda: self.start_game())
        self.start_button.place(x = self.cell_size * 12, y = self.cell_size * 21)
        self.reset_button = Button(self.frame,width = 10,font = self.game_font,text = "reset",borderwidth = 3,command= lambda: self.reset_game())
        self.reset_button.place(x = self.cell_size * 12, y = self.cell_size * 19)

        #ilosc statkow
        self.number_of_ships_list = [4,3,2,1]
        self.label_4_mast = self.number_of_ships("czteromasztowce",1,17)
        self.label_3_mast = self.number_of_ships("trójmasztowce",2,16)
        self.label_2_mast = self.number_of_ships("dwumasztowce",3,15)
        self.label_1_mast = self.number_of_ships("jednomasztowce",4,14)
        
        self.enemy = None
    
    def close_window(self):
        self.game_window.destroy()
    
    def button_array(self,offset,function):
        buttons = [[0 for x in range(10)] for x in range(10)]
        for x in range(10):
            for y in range(10):
                buttons[x][y] = Button(self.frame,bg = '#DDDDDD',borderwidth= 3,command= lambda x1=x, y1=y: function(x1,y1))
                buttons[x][y].grid(column=x + 1, row=y + 1 + offset,sticky="wens")
        return buttons

    def numerate_array(self):
        myfont = ("Arial",int(self.cell_size/2))
        for x in range(22):
            for y in range(11):
                if (x == 0 or y == 0) and x != y and x != 11:
                    if x < 11:
                        label = Label(self.game_window, text = str(x - 1 + y))
                    else:
                        label = Label(self.game_window, text = str(x - 12 + y))
                    label.place(x = y*self.cell_size, y = x * self.cell_size)
                    label.config(font = myfont)
        for y in range(10):
            label = Label(self.game_window, text = str(y))
            label.place(x = y*self.cell_size + self.cell_size, y = x * self.cell_size + self.cell_size)
            label.config(font = myfont)

    def number_of_ships(self,ship_name,ships_left,offset):
        label = Label(self.game_window, text = ship_name + " " +str(ships_left))
        label.place(x = self.cell_size * 12, y = self.cell_size * offset)
        label.config(font = self.game_font)
        return label
    
    def update_labels(self):
        self.label_4_mast.configure(text = "czteromasztowce" + " " + str(self.number_of_ships_list[3]))
        self.label_3_mast.configure(text = "trójmasztowce" + " " + str(self.number_of_ships_list[2]))
        self.label_2_mast.configure(text = "dwumasztowce" + " " + str(self.number_of_ships_list[1]))
        self.label_1_mast.configure(text = "jednomasztowce" + " " + str(self.number_of_ships_list[0]))
        
    def update_taken_tiles(self):
        for button in self.taken_tiles:
            button.configure(bg = 'green')
    
    def update_banned_tiles(self,x,y):
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i >=0 and j >= 0 and i <= 9 and j <= 9:
                    self.banned_tiles.add(self.button_grid_player[i][j])
                    #self.button_grid_player[i][j].configure(bg="yellow")
            
    def place_ships(self,x,y):
        return_val = 1
        if self.game_started == False:
            action_done = False
            if self.button_grid_player[x][y] not in self.banned_tiles:
                if self.click_count == 1:
                    if self.button_grid_player[x][y] in self.possible_tiles:
                        self.taken_tiles.add(self.button_grid_player[x][y])
                        diff_x = x - self.click_x
                        diff_y = y - self.click_y
                        if diff_x != 0 and diff_y == 0:
                            for i in range(min(self.click_x,self.click_x+diff_x),max(self.click_x,self.click_x+diff_x)+1):
                                self.taken_tiles.add(self.button_grid_player[i][y])
                                self.update_banned_tiles(i,y)
                        elif diff_y != 0 and diff_x == 0:
                            for i in range(min(self.click_y,self.click_y+diff_y),max(self.click_y,self.click_y+diff_y)+1):           
                                self.taken_tiles.add(self.button_grid_player[x][i])
                                self.update_banned_tiles(x,i)
                        elif diff_x == 0 and diff_y == 0:
                            self.update_banned_tiles(x,y)
                        self.number_of_ships_list[max(abs(diff_x),abs(diff_y))] -= 1
                    else:
                        return_val = others.comm("Niepoprawne rozmieszczenie okrętów",self.tests)
                    others.clear_dictionary(self.possible_tiles)
                    self.update_taken_tiles()
                    self.click_count -= 1
                    action_done = True
                if self.click_count == 0 and action_done == False:
                    self.click_x = x
                    self.click_y = y
                    self.click_count += 1
                    self.possible_tiles = others.make_dictionary(x,y,self.button_grid_player,self.number_of_ships_list,self.banned_tiles)
                self.update_labels()
            else:
                return_val = others.comm("Niepoprawne rozmieszczenie okrętów",self.tests)
        else:
            return_val = others.comm("Próba strzelania we własny okręt",self.tests) - 1
        return return_val
            
    def start_game(self):
        if self.game_started == True:
            others.comm("Gra już rozpoczęta",self.tests)
            return -1 
        for i in range(0,4):
            if self.number_of_ships_list[i] != 0:
                others.comm("Nie rozmieszczono wszystkich okrętów",self.tests)
                return -1
        self.enemy = ai.Enemy(self.button_grid_player,self.button_grid_enemy,self.taken_tiles)
        self.enemy.enemy_ship_placement()
        self.number_of_ships_list = self.enemy.number_of_ships_list
        self.update_labels()
        self.game_started = True
        self.destroyed = 0
        self.who_start = others.get_random(9)
        if self.who_start <= 5:
            self.enemy.enemy_attack()
        
            
    def reset_game(self):
        self.possible_tiles.clear()
        self.taken_tiles.clear()
        self.banned_tiles.clear()
        self.fired_at.clear()
        self.click_count = 0
        for x in range(0,10):
            for y in range(0,10):
                self.button_grid_player[x][y].config(bg = "#DDDDDD")
                self.button_grid_enemy[x][y].config(bg = "#DDDDDD")
        self.number_of_ships_list = [4,3,2,1]
        self.update_labels()
        self.game_started = False
        self.skip = False
        
    def player_attack(self,x,y):
        return_val = 1
        if self.game_started == True:
            if self.button_grid_enemy[x][y] not in self.fired_at:
                if self.button_grid_enemy[x][y] in self.enemy.taken_tiles:
                    self.button_grid_enemy[x][y].configure(bg="red")
                    self.destroyed += 1
                    return_val = 2
                else:
                    self.button_grid_enemy[x][y].configure(bg="blue")
                self.fired_at.add(self.button_grid_enemy[x][y])
            else:
                return_val = others.comm("W to miejsce juz strzelano!",self.tests)
                self.skip = True
            if self.destroyed >= 20:
                return_val = others.comm("Wygrana!",self.tests) + 1
                self.reset_game()
        return return_val
         
    def attack_enemy(self,x,y):
        return_val = 1
        if self.game_started == True:
            self.player_attack(x,y)
            if self.destroyed < 20 and self.skip == False:
                self.enemy.enemy_attack()
                self.number_of_ships_list = self.enemy.number_of_ships_list
            self.skip = False
            self.update_labels()
            if self.enemy.destroyed >= 20:
                return_val = others.comm("Przegrana!",self.tests) + 1
                self.reset_game()
        else:
                return_val = others.comm("Rozmieść okręty!",self.tests) 
        return return_val