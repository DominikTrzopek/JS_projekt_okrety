from unittest import TestCase
from unittest.mock import patch as patch
import player
import ai
from tkinter import *

class TestApp(TestCase):
    #1
    def test_wrong_ship_placement_diagonal(self):
        #given
        root = Tk()
        app = player.Ships_app(1,root,True)
        x1 = 4
        y1 = 4
        x2 = 5
        y2 = 5
        #when 
        val = app.place_ships(x1,y1)
        val = app.place_ships(x2,y2)
        #then
        self.assertNotEqual(val,1)
    #1
    def test_wrong_ship_placement_tooclose(self):
        #given
        root = Tk()
        app = player.Ships_app(1,root,True)
        x1 = 4,4
        x2 = 4,7
        x3 = 5,4
        x4 = 5,7       
        #when 
        val1 = app.place_ships(x1[0],x1[1])
        val2 = app.place_ships(x2[0],x2[1])
        val3 = app.place_ships(x3[0],x3[1])
        val4 = app.place_ships(x4[0],x4[1])
        #then
        self.assertNotEqual(val3,1)
        self.assertNotEqual(val4,1)
    #3 
    def test_shoot_empty_tile(self):
        #given
        root = Tk()
        app = player.Ships_app(1,root,True)
        x = 4
        y = 5
        #when 
        val = app.player_attack(x,y)
        #then
        self.assertEqual(val,1)
    #4
    def test_shoot_enemy_ship(self):
        #given
        root = Tk()
        app = player.Ships_app(1,root,True)
        x = 4
        y = 5
        enemy = ai.Enemy(app.button_grid_player,app.button_grid_enemy,app.taken_tiles)
        enemy.taken_tiles.add(enemy.button_grid_enemy[x][y])
        app.game_started = True
        app.enemy = enemy
        #when       
        val = app.player_attack(x,y)
        #then
        self.assertEqual(val,2)
    #5
    def test_shoot_own_ship(self):
        #given
        root = Tk()
        app = player.Ships_app(1,root,True)
        x = 4
        y = 5
        app.game_started = True
        #when       
        val = app.place_ships(x,y)
        #then
        self.assertEqual(val,-2)
    #6          
    def test_shoot_same_tile(self):
        #given
        root = Tk()
        app = player.Ships_app(1,root,True)
        x = 3
        y = 2
        app.game_started = True
        app.enemy = ai.Enemy(app.button_grid_player,app.button_grid_enemy,app.taken_tiles)
        #when       
        val = app.player_attack(x,y)
        val = app.player_attack(x,y)
        #then
        self.assertEqual(val,-1)
    #7 
    def test_shoot_enemy_again(self):
        #given
        root = Tk()
        app = player.Ships_app(1,root,True)
        x = 4
        y = 5
        enemy = ai.Enemy(app.button_grid_player,app.button_grid_enemy,app.taken_tiles)
        enemy.taken_tiles.add(enemy.button_grid_enemy[x][y])
        app.game_started = True
        app.enemy = enemy
        #when       
        val = app.player_attack(x,y)
        val = app.player_attack(x,y)
        #then
        self.assertEqual(val,-1)       
    #8 
    def test_place_and_reset(self):
        #given
        root = Tk()
        app = player.Ships_app(1,root,True)
        x1 = 4
        y1 = 4
        x2 = 4
        y2 = 6
        #when 
        val1 = app.place_ships(x1,y1)
        val2 = app.place_ships(x2,y2)
        app.reset_game()
        val1 = app.place_ships(x1,y1)
        val2 = app.place_ships(x2,y2)
        #then
        self.assertEqual(val1,1)
        self.assertEqual(val2,1)
    #9
    def test_shoot_and_reset(self):
        #given
        root = Tk()
        app = player.Ships_app(1,root,True)
        x2 = 4
        y2 = 5
        x1 = 6
        y1 = 7
        enemy = ai.Enemy(app.button_grid_player,app.button_grid_enemy,app.taken_tiles)
        app.game_started = True
        app.enemy = enemy
        #when 
        val1 = app.player_attack(x1,y1)
        val2 = app.player_attack(x2,y2)
        app.reset_game()
        app.game_started = True
        val1 = app.player_attack(x1,y1)
        val2 = app.player_attack(x2,y2)    
        #then
        self.assertEqual(val1,1)
        self.assertEqual(val2,1)
    #11
    def test_shoot_before_placement(self):
        #given
        root = Tk()
        app = player.Ships_app(1,root,True)
        x = 4
        y = 5
        enemy = ai.Enemy(app.button_grid_player,app.button_grid_enemy,app.taken_tiles)
        app.game_started = False
        app.enemy = enemy
        #when 
        val1 = app.attack_enemy(x,y)  
        #then
        self.assertEqual(val1,-1)
        
        
a = TestApp()
a.test_wrong_ship_placement_diagonal()
a.test_wrong_ship_placement_tooclose()
a.test_shoot_empty_tile()
a.test_shoot_enemy_ship()
a.test_shoot_own_ship()
a.test_shoot_same_tile()
a.test_shoot_enemy_again()
a.test_place_and_reset()
a.test_shoot_and_reset()
a.test_shoot_before_placement()