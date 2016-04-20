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
    create_file = False
    manager = database_manager.BetBase()
    manager.read_config()
    
    user_path = os.path.normpath(manager.user_path)    
    htpassword_file = os.path.normpath(manager.htpassword_file)

    form=cgi.FieldStorage()    
    user = form.getfirst('user')
    password = form.getfirst('password')
    confirm = form.getfirst('confirm')
    
    if user.lower().startswith('xml'):
        print_error('Username must not start with "xml"!')
        return

    if user[0] in '0123456789':
        print_error('Username must not start with a number!')
        return
        
    for char in user:
        if not char in 'qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM1234567890':
            print_error('Invalid character in username. Valid characters are only letters and numbers.')
            return
            
    if not os.path.isdir(user_path):
        print_error('Path to users folder ' + user_path + ' was not found. New user was not created.')
        return
        
    if not password == confirm:
        print_error('Passwords do not match. Please try again.')
        return
        
    if not os.path.isfile(htpassword_file):
        create_file = True
    
    manager.add_usernode(user)
    manager.save_database()
    
    userpath = os.path.join(user_path, user)
    if not os.path.exists(userpath):
        os.makedirs(userpath)
    
    shutil.os.symlink(os.path.join(user_path, 'personal_betting_table.php'), os.path.join(userpath, 'index.php'))
    with open(os.path.join(userpath, '.htacess'), 'w') as userfile:
        userfile.write('Require user ' + user)
    
    if create_file:
        subprocess.call(['htpasswd', '-bc', htpassword_file, user, password])
    else:
        subprocess.call(['htpasswd', '-b', htpassword_file, user, password])
        
    print_response(user)

if __name__ == '__main__':
    main()
