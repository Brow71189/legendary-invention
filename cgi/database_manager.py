# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 15:13:07 2016

@author: mittelberger
"""
import os
import sys
import ast
import time
import shutil
from xml.etree import ElementTree

class Lock(object):
    def __init__(self, file=None):
        if file is not None:
            file = os.path.normpath(file)
        self.file = file
    
    def acquire(self, file=None):
        if file is not None:
            self.file = file
        if self.file is None:
            raise IOError('No File to lock.')
        if os.path.isfile(self.file+'.lock'):
            raise IOError('File is already locked.')
        else:
            shutil.copy2(self.file, self.file+'.lock')
        
        return self.file + '.lock'
    
    def release(self, file=None):
        if file is not None:
            if file.endswith('.lock'):
                self.file = file[:-5]
            else:
                self.file = file
        if self.file is None:
            raise IOError('No File to release the lock from.')
        if os.path.isfile(self.file+'.lock'):
            shutil.move(self.file+'.lock', self.file)
            
        return self.file
            
    def is_locked(self, file=None):
        if file is not None:
            if file.endswith('.lock'):
                self.file = file[:-5]
            else:
                self.file = file
        
        if self.file is None:
            raise IOError('No File to check if it is locked.')
        
        if os.path.isfile(self.file + '.lock'):
            return True
        else:
            return False

class BetBase(object):
    def __init__(self, **kwargs):
        self.gameslist_path = 'gameslist.txt'
        self.database_path = 'betbase.xml'
        self.user = kwargs.get('user', {})
        self.database_tree = None
        self.lock_timeout = 5
        self.filelock = Lock()
        self.games = []

    def read_config(self):
        try:
            configfile = open(os.path.join(os.path.dirname(sys.argv[0]), 'manager.conf'))
        except (IOError, OSError):
            print('Could not find config file. Make sure it is in the same folder as the script and is called ' + 
                  '"manager.conf"!')
            return
        
        for line in configfile:
            if line.startswith('#'):
                continue
            
            splitline = line.split(':', 1)
            if len(splitline) == 2:
                try:
                    setattr(self, splitline[0].strip(), ast.literal_eval(splitline[1].strip()))
                except AttributeError:
                    print('Parameter ' + splitline[0].strip() + ' is not known. It will be ignored.')
                    
    def read_games_list(self):
        pass
    
    def create_game_id(self):
        pass
    
    def delete_game(self):
        pass
    
    def delete_user(self):
        pass
    
    def load_database(self):
        self.database_path = os.path.normpath(self.database_path)
        if os.path.isfile(self.database_path):
            starttime = time.time()
            while time.time() - starttime < self.lock_timeout:
                try:
                    self.database_path = self.filelock.acquire(file=self.database_path)
                except IOError:
                    time.sleep(0.1)
                else:
                    break
            else:
                raise IOError('Could not get a lock on database file.')
                
        try:
            self.database_tree = ElementTree.parse(self.database_path)
        except (OSError, IOError, ElementTree.ParseError):
            print('Could not find a database in ' + self.database_path  + '. Creating a new empty one.')
            self.database_tree = ElementTree.ElementTree()
        finally:
            if self.database_tree.getroot() is None:
                self.database_tree._setroot(ElementTree.Element('betbase',
                                                                attrib={'created': time.strftime('%Y_%m_%d_%H_%M')}))
                                                                
    def update_games(self):
        games = self.database_tree.getroot().find('games')
        if games is None:
            games = ElementTree.Element('games')
            self.database_tree.getroot().append(games)
        
        for game in self.games:
            gamenode = games.find(game['id'])
            if gamenode is None:
                gamenode = ElementTree.Element(game['id'])
                games.append(gamenode)
            game.pop['id']
            for key, value in game.items():
                info_element = gamenode.find(key)
                if info_element is None:
                    info_element = ElementTree.Element(key)
                    gamenode.append(info_element)
                info_element.text = value

    def add_user(self, user=None):
        users = self.database_tree.getroot().find('users')
        if users is None:
            users = ElementTree.Element('users')
            self.database_tree.getroot().append(users)

        if user is None:
            user = self.user
        if user is None:
            return
        
        usernode = users.find(user)
        if usernode is None:
            usernode = ElementTree.Element(user)
            users.append(usernode)
            usernode.append(ElementTree.Element('points'))
            usernode.append(ElementTree.Element('rank'))
            usernode.append(ElementTree.Element('tips'))

    def save_database(self):
        self.database_tree.write(self.database_path)
        self.filelock.release()