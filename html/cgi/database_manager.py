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
        self._lock_expire_time = 3600

    def acquire(self, file=None, timeout=5):
        if file is not None:
            self.file = os.path.normpath(file)
        if self.file is None:
            raise OSError('No File to lock.')
        starttime = time.time()
        while time.time() - starttime < timeout:
            if (not os.path.isfile(self.file + '.lock') or
                    time.time() - os.path.getmtime(self.file + '.lock') > self._lock_expire_time):
                break
        else:
            raise OSError('Could not get a lock on file before timeout because it is already locked.')

        shutil.copy2(self.file, self.file+'.lock')

        return self.file + '.lock'

    def release(self, file=None):
        if file is not None:
            if file.endswith('.lock'):
                self.file = file[:-5]
            else:
                self.file = file
        if self.file is None:
            raise OSError('No File to release the lock from.')
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
            raise OSError('No File to check if it is locked.')

        if os.path.isfile(self.file + '.lock'):
            return True
        else:
            return False

class BetBase(object):
    # Time format in gamelist. It is used to convert the string representing the time.
    time_format = '%m-%dT%H:%M'
    # Map all elements and attributes to names used in the code. It is a dictionary where each key is an element
    # or attribute from the input, the respective value is the name as used in the code
    names = {'points': 'points', 'rank': 'rank', 'tips': 'tips', 'tipps': 'tips', 'date': 'date', 'team1': 'team1',
             'team2': 'team2', 'name1': 'name1', 'name2': 'name2', 'score1': 'score1',
             'score2': 'score2'}

    def __init__(self, **kwargs):
        self.gameslist_path = 'gameslist.txt'
        self.database_path = '/var/www/html/cgi/betbase.xml'
        self.user = kwargs.get('user', {})
        self.database_tree = None
        self.lock_timeout = 5
        self.filelock = Lock()
        self.games = []
        self._is_readonly = True
        self.quiet = kwargs.get('quiet', False)

    def read_config(self):
        try:
            configfile = open(os.path.join(os.path.dirname(sys.argv[0]), 'manager.conf'))
        except (IOError, OSError):
            raise OSError('Could not find config file. Make sure it is in the same folder as the script and is ' +
                          'called "manager.conf"!')

        for line in configfile:
            line = line.strip()
            if line.startswith('#') or line.startswith(';'):
                continue

            splitline = line.split(':', 1)
            if len(splitline) == 2:
                try:
                    setattr(self, splitline[0].strip(), ast.literal_eval(splitline[1].strip()))
                except AttributeError:
                    if not self.quiet:
                        print('Parameter ' + splitline[0].strip() + ' is not known. It will be ignored.')

        configfile.close()

    def read_games_list(self, separator=None):
        try:
            gameslist_file = open(os.path.abspath(self.gameslist_path))
        except (IOError, OSError):
            raise OSError('Could not find gameslist file. Make sure the path you entered is correct (' +
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
                        if self.names.get(fieldnames[i]):
                            game[self.names[fieldnames[i]]] = splitline[i].strip()
                    game['id'] = self.create_game_id(game)
                    self.games.append(game)

        gameslist_file.close()

    def create_game_id(self, game):
        team1 = min(game['team1'], game['team2'])
        team2 = max(game['team1'], game['team2'])
        if game.get('date'):
            date = time.strptime(game['date'], self.time_format)
            return team1 + team2 + '{:02d}{:02d}'.format(date.tm_mon, date.tm_mday)
        elif game.get('month') and game.get('day'):
            return  team1 + team2 + '{:02d}{:02d}'.format(game['month'], game['day'])

    def delete_game(self, *game):
        gamenode = self.get_gamenode(*game, writeable=True)
        games = self.database_tree.getroot().find('games')
        games.remove(gamenode)

    def delete_user(self, name):
        usernode = self.get_usernode(name, writeable=True)
        users = self.database_tree.getroot().find('users')
        users.remove(usernode)

    def update_points(self):
        if self.database_tree is None or self._is_readonly:
            self.load_database(writeable=True)

        users = self.database_tree.getroot().find('users')
        games = self.database_tree.getroot().find('games')
        currenttime = time.strftime(self.time_format)

        for user in users:
            tips = user.find('tips')
            points = 0
            if tips is None:
                continue
            for tip in tips:
                game = games.find(tip.tag)
                if (game is None or game.get('date', default='z') > currenttime or game.get('score1') is None or
                        game.get('score2') is None or tip.get('score1') is None or tip.get('score2') is None):
                    continue
                tipscore1 = int(tip.get('score1'))
                tipscore2 = int(tip.get('score2'))
                gamescore1 = int(game.get('score1'))
                gamescore2 = int(game.get('score2'))
                if tipscore1 == gamescore1 and tipscore2 == gamescore2:
                    points += 3
                elif sign(tipscore1 - tipscore2) == sign(gamescore1 - gamescore2):
                    points += 1

            pointsnode = user.find('points')
            if pointsnode is None:
                pointsnode = ElementTree.Element('points')
                user.append(pointsnode)
            pointsnode.text = str(points)

        self._update_ranks()
        self.save_database()

    def _update_ranks(self):
        users = self.database_tree.getroot().find('users')
        sortedusers = sorted(users, key=lambda usernode: int(usernode.findtext('points', default=0)), reverse=True)
        for i in range(len(sortedusers)):
            rank = sortedusers[i].find('rank')
            if rank is None:
                rank = ElementTree.Element('rank')
                sortedusers[i].append(rank)
            rank.text = str(i+1)

    def add_game_result(self, score1, score2, *game):
        gamenode = self.get_gamenode(*game, writeable=True)
        gamenode.set('score1', str(score1))
        gamenode.set('score2', str(score2))

    def add_or_update_tip(self, name, *tip):
        usernode = self.get_usernode(name, writeable=True)
        if len(tip) == 6:
            gameid = self.create_game_id({'month': tip[0], 'day': tip[1], 'team1': tip[2], 'team2': tip[3]})
        elif len(tip) == 3:
            gameid = tip[0]
        else:
            raise ValueError('Wrong number of arguments (must be 3 or 6). Three arguments are interpreted as game id,' +
                             ' score team1 and score team2. 6 arguments must be month, day, team1, team2, score team1' +
                             ' and score team2')

        tipnode = ElementTree.Element(gameid, attrib={'score1': str(tip[-2]), 'score2': str(tip[-1])})
        tips = usernode.find('tips')
        if tips is None:
            tips = ElementTree.Element('tips')
            usernode.append(tips)

        oldtip = tips.find(gameid)
        if oldtip is not None:
            tips.remove(oldtip)

        tips.append(tipnode)

    def get_usernode(self, name, **kwargs):
        if (self.database_tree is None or
                ((kwargs.get('writeable') or not kwargs.get('readonly', True)) and self._is_readonly)):
            self.load_database(**kwargs)

        usernode = self.database_tree.getroot().find('users').find(name)
        if usernode is None:
            raise RuntimeError('A user ' + name + 'could not be found in the database.')

        return usernode

    def get_user_info(self, user):
        if isinstance(user, ElementTree.Element):
            usernode = user
        else:
            usernode = self.get_usernode(user)
        return_dict = {}
        for element in usernode:
            if element.tag == 'tips':
                tips = {}
                for tip in element:
                    tips[tip.tag] = tip.attrib
                return_dict['tips'] = tips
            else:
                return_dict[element.tag] = element.text

        return return_dict

    def get_all_users_info(self):
        if self.database_tree is None:
            self.load_database()
        infolist = []
        for user in self.database_tree.getroot().find('users'):
            info = self.get_user_info(user)
            info['name'] = user.tag
            infolist.append(info)

        return infolist

    def get_gamenode(self, *game, **kwargs):
        if (self.database_tree is None or
                ((kwargs.get('writeable') or not kwargs.get('readonly', True)) and self._is_readonly)):
            self.load_database(**kwargs)
        if len(game) == 4:
            game = {'month': game[0], 'day': game[1], 'team1': game[2], 'team2': game[3]}
            game_id = self.create_game_id(game)
        elif len(game) == 1:
            game_id = game[0]
        else:
            raise ValueError('Wrong number of arguments (must be 1 or 4). A single argument is interpreted as ' +
                             'game id. Multiple argument must be Month, Day, Team1, Team2.')

        gamenode = self.database_tree.getroot().find('games').find(game_id)
        if gamenode is None:
            raise RuntimeError('A game with this identificator could not be found in the database '  + str(game) + '.')

        return gamenode

    def get_game_info(self, *game):
        if isinstance(game[0], ElementTree.Element):
            gamenode = game[0]
        else:
            gamenode = self.get_gamenode(*game)
        return gamenode.attrib

    def get_all_games_info(self):
        if self.database_tree is None:
            self.load_database()
        infolist = []
        for game in self.database_tree.getroot().find('games'):
            info = self.get_game_info(game)
            info['id'] = game.tag
            infolist.append(info)

        return infolist

    def load_database(self, readonly=True, writeable=False):
        try:
            self.read_config()
        except (IOError, OSError):
            if not self.quiet:
                print('Could not read config file. Will try to use default configuration.')

        self._is_readonly = readonly
        if writeable:
            self._is_readonly = False

        self.database_path = os.path.normpath(self.database_path)
        if os.path.isfile(self.database_path) and not self._is_readonly:
            self.database_path = self.filelock.acquire(file=self.database_path, timeout=self.lock_timeout)

        try:
            self.database_tree = ElementTree.parse(self.database_path)
        except (OSError, IOError, ElementTree.ParseError):
            if not self.quiet:
                print('Could not find a database in ' + self.database_path  + '. Creating a new empty one.')
            self.database_tree = ElementTree.ElementTree()
        finally:
            if self.database_tree.getroot() is None:
                self.database_tree._setroot(ElementTree.Element('betbase',
                                                                attrib={'created': time.strftime('%Y_%m_%d_%H_%M')}))

    def update_games(self):
        for game in self.games:
            game_id = game.pop('id')
            try:
                gamenode = self.get_gamenode(game_id, writeable=True)
            except (RuntimeError, AttributeError):
                gamenode = self.add_gamenode(game_id)

            for key, value in game.items():
                gamenode.set(key, value)

    def add_gamenode(self, *game):
        if self.database_tree is None or self._is_readonly:
            self.load_database(writeable=True)

        if len(game) == 4:
            game = {'month': game[0], 'day': game[1], 'team1': game[2], 'team2': game[3]}
            game_id = self.create_game_id(game)
        elif len(game) == 1:
            game_id = game[0]
        else:
            raise ValueError('Wrong number of arguments (must be 1 or 4). A single argument is interpreted as ' +
                             'game id. Multiple argument must be Month, Day, Team1, Team2.')

        games = self.database_tree.getroot().find('games')
        if games is None:
            games = ElementTree.Element('games')
            self.database_tree.getroot().append(games)
        gamenode = games.find(game_id)
        if gamenode is not None:
            raise RuntimeError('A game with the same id already exists (' + str(game) + ').')
        gamenode = ElementTree.Element(game_id)
        games.append(gamenode)

        return gamenode

    def add_usernode(self, name=None):
        if name is None:
            name = self.user
        if name is None:
            return

        if self.database_tree is None or self._is_readonly:
            self.load_database(writeable=True)

        users = self.database_tree.getroot().find('users')
        if users is None:
            users = ElementTree.Element('users')
            self.database_tree.getroot().append(users)
        usernode = users.find(name)
        if usernode is not None:
            raise RuntimeError('A user ' + name + 'exists already in the database.')
        usernode = ElementTree.Element(name)
        users.append(usernode)

        return usernode

    def save_database(self):
        if not self._is_readonly:
            self.database_tree.getroot().set('last_updated', time.strftime('%Y_%m_%d_%H_%M'))
            self.database_tree.write(self.database_path)
            try:
                self.filelock.release()
            except OSError:
                if not self.quiet:
                    print('Could not release lock on the database file.')
            else:
                self._is_readonly = True
        else:
            raise OSError('Cannot save database because it was opened readonly.')

def sign(x):
    """
    Signum of x. Returns -1 for negative numbers, 1 for positive numbers and 0 for 0.
    """
    if x < 0:
        return -1
    if x > 0:
        return 1
    if x == 0:
        return 0
