import random
import others


class Enemy():
    def __init__(self,player_buttons,enemy_buttons,player_taken):
        self.possible_tiles = set()
        self.taken_tiles = set()
        self.banned_tiles = set()
        self.button_grid_player = player_buttons
        self.button_grid_enemy = enemy_buttons
        self.player_taken_tiles = player_taken
        self_middle_point_x = 0
        self_middle_point_y = 0
        self.number_of_ships_list = [4,3,2,1]
        self.where_to_attack = []
        self.indexes = []
        self.unlikely_tiles = set()
        self.destroyed = 0
        self.it = 0
    
    def update_taken_tiles(self):
        for button in self.taken_tiles:
            button.configure(bg = 'yellow')
            
    def update_banned_tiles(self,x,y):
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i >=0 and j >= 0 and i <= 9 and j <= 9:
                    self.banned_tiles.add(self.button_grid_enemy[i][j])
               
    def enemy_ship_placement(self):
        it = 0
        while(it < 10):
            x = others.get_random(9)
            y = others.get_random(9)
            if self.button_grid_enemy[x][y] not in self.banned_tiles:
                self.possible_tiles = others.make_dictionary(x,y,self.button_grid_enemy,self.number_of_ships_list,self.banned_tiles,False)
                x2 = others.get_random(9)
                y2 = others.get_random(9)
                if self.button_grid_enemy[x2][y2] in self.possible_tiles:
                    self.taken_tiles.add(self.button_grid_enemy[x2][y2])
                    diff_x = x2 - x
                    diff_y = y2 - y
                    if diff_x != 0 and diff_y == 0:
                        for i in range(min(x,x+diff_x),max(x,x+diff_x)+1):
                            self.taken_tiles.add(self.button_grid_enemy[i][y])
                            self.update_banned_tiles(i,y) 
                    elif diff_y != 0 and diff_x == 0:
                        for i in range(min(y,y+diff_y),max(y,y+diff_y)+1):           
                            self.taken_tiles.add(self.button_grid_enemy[x][i])
                            self.update_banned_tiles(x,i)
                    elif diff_x == 0 and diff_y == 0:
                        self.update_banned_tiles(x,y)
                    self.number_of_ships_list[max(abs(diff_x),abs(diff_y))] -= 1
                    others.clear_dictionary(self.possible_tiles)
                    #self.update_taken_tiles()
                    it += 1
        self.number_of_ships_list = [4,3,2,1]
    
    def delete_corners(self,x,y):
        self.destroyed += 1
        self.button_grid_player[x][y].configure(bg="red")
        if x-1 >= 0 and y-1 >= 0:
            self.unlikely_tiles.add(self.button_grid_player[x-1][y-1])
            #self.button_grid_player[x-1][y-1].configure(bg = "yellow")
        if x+1 < 10 and y+1 < 10:
            self.unlikely_tiles.add(self.button_grid_player[x+1][y+1])
            #self.button_grid_player[x+1][y+1].configure(bg = "yellow")
        if x-1 >= 0 and y+1 < 10:
            self.unlikely_tiles.add(self.button_grid_player[x-1][y+1])
            #self.button_grid_player[x-1][y+1].configure(bg = "yellow")
        if x+1 < 10 and y-1 >= 0:
            self.unlikely_tiles.add(self.button_grid_player[x+1][y-1])
            #self.button_grid_player[x+1][y-1].configure(bg = "yellow")
            
    def add_next_tile(self,x,y):
        self.it += 1
        if x-1 >= 0:
            self.where_to_attack.append(self.button_grid_player[x-1][y])
            self.indexes.append((x-1,y))
            #self.button_grid_player[x-1][y].configure(bg = "black")
        if x+1 < 10:
            self.where_to_attack.append(self.button_grid_player[x+1][y])
            #self.button_grid_player[x+1][y].configure(bg = "black")
            self.indexes.append((x+1,y))
        if y-1 >= 0:
            self.where_to_attack.append(self.button_grid_player[x][y-1])
            #self.button_grid_player[x][y-1].configure(bg = "black")
            self.indexes.append((x,y-1))
        if y+1 < 10:
            self.where_to_attack.append(self.button_grid_player[x][y+1])
            #self.button_grid_player[x][y+1].configure(bg = "black")
            self.indexes.append((x,y+1))
            
    def get_ship_number(self):
        for i in range(3,-1,-1):
            if self.number_of_ships_list[i] != 0:
                return i
    
    def enemy_attack(self):
        if self.destroyed < 20:
            if len(self.where_to_attack) <= 0:
                for i in range(1,5):
                    if self.it == i:
                         self.number_of_ships_list[i-1] -= 1
                self.it = 0
                while True:
                    x = others.get_random(9)
                    y = others.get_random(9)
                    if self.button_grid_player[x][y] not in self.unlikely_tiles:
                        break
                if self.button_grid_player[x][y] in self.player_taken_tiles:
                    self.delete_corners(x,y)
                    self.add_next_tile(x,y)
                else:
                    self.button_grid_player[x][y].configure(bg="blue")
                self.unlikely_tiles.add(self.button_grid_player[x][y])
            else:           
                rand = others.get_random(len(self.where_to_attack)-1)
                if self.where_to_attack[rand] in self.unlikely_tiles:
                    self.where_to_attack.pop(rand)
                    self.indexes.pop(rand)
                    self.enemy_attack()
                elif self.where_to_attack[rand] in self.player_taken_tiles:
                    self.unlikely_tiles.add(self.button_grid_player[self.indexes[rand][0]][self.indexes[rand][1]])    
                    self.add_next_tile(self.indexes[rand][0],self.indexes[rand][1])          
                    self.delete_corners(self.indexes[rand][0],self.indexes[rand][1])
                else:
                    self.button_grid_player[self.indexes[rand][0]][self.indexes[rand][1]].configure(bg="blue")
                    self.where_to_attack.pop(rand)
                    self.indexes.pop(rand)