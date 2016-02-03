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
    _fields = {'month': 'Month', 'day': 'Day', 'time': 'Time', 'team1': 'Team1', 'team2': 'Team2', 'name1': 'FullName1',
               'name2': 'FullName2', 'timeformat': '%H:%M'}
    
    def __init__(self, **kwargs):
        self.gameslist_path = 'gameslist.txt'
        self.database_path = 'betbase.xml'
        self.user = kwargs.get('user', {})
        self.database_tree = None
        self.lock_timeout = 5
        self.filelock = Lock()
        self.games = []
        self._is_readonly = True

    def read_config(self):
        try:
            configfile = open(os.path.join(os.path.dirname(sys.argv[0]), 'manager.conf'))
        except (IOError, OSError):
            raise IOError('Could not find config file. Make sure it is in the same folder as the script and is ' + 
                  'called "manager.conf"!')
        
        for line in configfile:
            line = line.strip()
            if line.startswith('#'):
                continue
            
            splitline = line.split(':', 1)
            if len(splitline) == 2:
                try:
                    setattr(self, splitline[0].strip(), ast.literal_eval(splitline[1].strip()))
                except AttributeError:
                    print('Parameter ' + splitline[0].strip() + ' is not known. It will be ignored.')
                    
        configfile.close()
                    
    def read_games_list(self, separator='\t'):
        try:
            gameslist_file = open(os.path.abspath(self.gameslist_path))
        except (IOError, OSError):
            raise IOError('Could not find gameslist file. Make sure the path you entered is correct (' +
                          self.gameslist_path + ')!')
        fieldnames = []
        for line in gameslist_file:
            line = line.strip()
            if line.startswith('#'):
                continue
            elif line.startswith(';'):
                line = line[1:].strip()
                splitline = line.split(separator)
                for element in splitline:
                    element = element.strip()
                    fieldnames.append(element)
            else:
                splitline = line.split(separator)
                if len(fieldnames) > 0 and len(splitline) == len(fieldnames):
                    game = {}
                    for i in range(len(splitline)):
                        game[fieldnames[i]] = splitline(i).strip()
                    game['id'] = self.create_game_id(game)
                    self.games.append(game)
        
        gameslist_file.close()
    
    def create_game_id(self, game):
        team1 = min(game[self._fields['team1']], game[self._fields['team2']])
        team2 = max(game[self._fields['team1']], game[self._fields['team2']])
        return game[self._fields['month']] + game[self._fields['day']] + team1 + team2
    
    def delete_game(self, *args):
        if len(args) != 1 and len(args) != 4:
            raise ValueError('At least 1 argument is required. A single argument is interpreted as game id. ' + 
                             'Multiple argument must be Month, Day, Team1, Team2.')
        if self.database_tree is None:
            self.read_config()
            self.load_database(writeable=True)
        if len(args) == 4:
            game = {self._fields['month']: args[0], self._fields['day']: args[1], self.fields['team1']: args[2]}
            gameid = self.create_game_id(game)
        else:
            gameid = args[0]
        
        games = self.database_tree.getroot().find('games')
        try:
            games.remove(games.find(gameid))
        except TypeError:
            raise RuntimeError('A game with this identificator could not be found in the database '  + str(args) + '.')
        
        self.save_database()
            
    
    def delete_user(self, name):
        if self.database_tree is None:
            self.read_config()
            self.load_database(writeable=True)
        
        users = self.database_tree.getroot().find('users')
        try:        
            users.remove(users.find(name))
        except TypeError:
            raise RuntimeError('A user ' + name + 'could not be found in the database.')
            
        self.save_database()
    
    def update_points(self):
        pass
    
    def update_ranks(self):
        pass
    
    def add_game_result(self, *args):
        pass
    
    def add_tipp(self, tipp, user):
        pass
    
    def get_user_info(self, name):
        if self.database_tree is None:
            self.read_config()
            self.load_database()
        
        user = self.database_tree.getroot().find('users').find(name)
        if user is None:
            raise RuntimeError('A user ' + name + 'could not be found in the database.')
            
            
    
    def get_game_info(self, *game):
        pass
    
    def load_database(self, readonly=True, writeable=False):
        self._is_readonly = readonly
        if writeable:
            self._is_readonly = False
            
        self.database_path = os.path.normpath(self.database_path)
        if os.path.isfile(self.database_path) and not self._is_readonly:
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
        if not self._is_readonly:
            self.database_tree.getroot().set('last_updated', time.strftime('%Y_%m_%d_%H_%M'))
            self.database_tree.write(self.database_path)
            try:            
                self.filelock.release()
            except:
                print('Could not release the lock on the database file.')
        else:
            raise IOError('Cannot save database because it was opened readonly.')