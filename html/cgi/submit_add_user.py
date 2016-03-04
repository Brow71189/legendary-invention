#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 09:34:34 2016

@author: mittelberger
"""

import database_manager
import os
import shutil
import cgi
import cgitb
cgitb.enable()
import subprocess


user_path = '/home/pi/legendary-invention/html/users'
htpassword_file = '/home/pi/legendary.pass'

def print_response(user):
    print("""\
Content-type:text/html\r\n\r\n
<!DOCTYPE html>
<html>
    <head>
        <title>Legendary Invention</title>
        <link rel="stylesheet" href="/legend.css" type="text/css">
        <meta http-equiv="Refresh" content="5;url=/users/admin/">
    </head>
    <body>
        Logged in as <?php echo $_SERVER['PHP_AUTH_USER'];?>
    
        <h3>USER """ + user + """ HAS BEEN SUCCESSFULLY ADDED!</h3>
        <br><br>
        <p>You will be redirected to the admin area in 5 seconds. If not, use the following link:</p>
        <a href="/users/admin/" title="Admin Area">Admin Area</a>
    </body>
</html>""")

def print_error(message):
    print("""\
Content-type:text/html\r\n\r\n
<!DOCTYPE html>
<html>
    <head>
        <title>Legendary Invention</title>
        <link rel="stylesheet" href="/legend.css" type="text/css">
        <meta http-equiv="Refresh" content="5;url=/users/admin/">
    </head>
    <body>
        Logged in as <?php echo $_SERVER['PHP_AUTH_USER'];?>
        <h1>COULD NOT ADD NEW USER! REASON:<h1>
        <h3>""" + message + """</h3>
        <br><br>
        <p>You will be redirected to the admin area in 5 seconds. If not, use the following link:</p>
        <a href="/users/admin/" title="Admin Area">Admin Area</a>
    </body>
</html>""")

def main():
    global htpassword_file
    global user_path
    user_path = os.path.normpath(user_path)    
    htpassword_file = os.path.normpath(htpassword_file)

    form=cgi.FieldStorage()    
    user = form.getfirst('user')
    password = form.getfirst('password')
    confirm = form.getfirst('confirm')

    if not os.path.isdir(user_path):
        print_error('Path to users folder ' + user_path + ' was not found. New user was not created.')
        return
        
    if not password == confirm:
        print_error('Passwords do not match. Please try again.')
        return
        
    if not os.path.isfile(htpassword_file):
        print_error('Htpassword file does not exist. New user was not created.')
        return
    
    manager = database_manager.BetBase()
    manager.add_usernode(user)
    manager.save_database()
    
    userpath = os.path.join(user_path, user)
    if not os.path.exists(userpath):
        os.makedirs(userpath)
    
    shutil.os.symlink(os.path.join(user_path, 'personal_betting_table.php'), os.path.join(userpath, 'index.php'))
    shutil.os.symlink(os.path.join(user_path, 'submit_bet.php'), os.path.join(userpath, 'submit_bet.php'))
    with open(os.path.join(userpath, '.htacess'), 'w') as userfile:
        userfile.write('Require user ' + user)
    
    subprocess.call(['htpasswd', '-b', htpassword_file, user, password])
        
    print_response(user)

if __name__ == '__main__':
    main()
