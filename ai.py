import random
import others


class Enemy():
    def __init__(self,player_buttons,enemy_buttons,player_taken):
        #zbiór z polami na którch przeciwnik może umieścić okręt
        self.possible_tiles = set()
        #zbiór z polami na których okręty zostały umieszczone
        self.taken_tiles = set()
        #zbiór pól niedozwolonych do wyboru przy umieszczaniu okrętu
        self.banned_tiles = set()
        #siatka z polami gracza
        self.button_grid_player = player_buttons
        #siatka z polami przeciwnika
        self.button_grid_enemy = enemy_buttons
        #pola z okrętami rozmieszczonymi przez gracza
        self.player_taken_tiles = player_taken
        #numer kolumny i wiersza pola, który wylosował komputer
        self_middle_point_x = 0
        self_middle_point_y = 0
        #ilosc statkow
        self.number_of_ships_list = [i for i in range(4,0,-1)]
        #lista z polami w które komputer będzie strzelał w celu określenia orientacji okrętu gracza
        self.where_to_attack = []
        #indeksy pól z listy where_to_attack
        self.indexes = []
        #zbiór pól na których nie mógł zostać umieszczony okręt gracza
        self.unlikely_tiles = set()
        #ilość staków gracza zniczonych przez komputer
        self.destroyed = 0
        #iterator
        self.it = 0
    
    def update_taken_tiles(self):
        """
        pokazuje rozmieszczenie statków przeciwnika
        """
        for button in self.taken_tiles:
            button.configure(bg = 'yellow')
            
    def update_banned_tiles(self,x,y):
        """
        uaktualnia zbiór niedozwolonych pól
        x,y - koordynaty pola
        """
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i >=0 and j >= 0 and i <= 9 and j <= 9:
                    self.banned_tiles.add(self.button_grid_enemy[i][j])
               
    def enemy_ship_placement(self):
        """
        ustawienie statków przez przeciwnika
        """
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
        self.number_of_ships_list = [i for i in range(4,0,-1)]
    
    def delete_corners(self,x,y):
        """
        dodaje do unlikely_tiles pola sąsiadujące rogami z trafionym okrętem gracza
        x,y koordynaty trafionego okrętu
        """
        self.destroyed += 1
        self.button_grid_player[x][y].configure(bg="red")
        #sprawdzenie czy sąsiad istnieje
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
        """
        dodaje do where_to_attack pola sąsiadujące bokami z trafionym okrętem gracza
        x,y koordynaty trafionego okrętu
        """
        self.it += 1
        #sprawdzenie czy sąsiad istnieje
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
             
    def enemy_attack(self):
        """
        atakowanie oktętów gracza
        """
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
