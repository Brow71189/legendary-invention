#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 09:34:34 2016

@author: mittelberger
"""

import database_manager
import argparse
import os
import shutil
import subprocess


default_path = '/home/pi/legendary-invention/html/users'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('user', help='Username that should be added to the BetBase Database')
    parser.add_argument('-p', '--path', help='Path to user folder. Default: ' + default_path,
                        default=default_path)
    
    args = parser.parse_args()
    user = args.user
    path = os.path.normpath(args.path)

    if not os.path.isdir(path):
        raise OSError(path + ' Does not exist. Please enter a valid path.')
    
    manager = database_manager.BetBase()
    manager.add_usernode(user)
    manager.save_database()
    
    userpath = os.path.join(path, user)
    if not os.path.exists(userpath):
        os.makedirs(userpath)
    else:
        print('User folder already exists')
    
    shutil.os.symlink(os.path.join(path, 'personal_betting_table.php'), os.path.join(userpath, 'index.php'))
    shutil.os.symlink(os.path.join(path, 'submit_bet.php'), os.path.join(userpath, 'submit_bet.php'))
    with open(os.path.join(userpath, '.htacess'), 'w') as userfile:
        userfile.write('Require user ' + user)
        
    subprocess.call(['htpasswd', '/home/pi/legendary.pass', user])
