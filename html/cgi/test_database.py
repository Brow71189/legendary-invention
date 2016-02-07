# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 11:47:48 2016

@author: Andi
"""
from numpy.random import rand
import database_manager

usernames = ['Giacomo', 'Andreas', 'Ursula', 'Christian', 'Tim']

manager = database_manager.BetBase()
manager.load_database(writeable=True)

for user in usernames:
    manager.add_usernode(user)

manager.read_games_list()
manager.update_games()

root = manager.database_tree.getroot()

for game in root.find('games'):
    for user in usernames:
        manager.add_tip(user, game.tag, int(rand()*5), int(rand()*5))
        
manager.update_points()