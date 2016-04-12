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
    
        <h3>USER """ + user + """ HAS BEEN SUCCESSFULLY DELETED!</h3>
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
    delete_from_htpasswd = True
    manager = database_manager.BetBase()
    manager.read_config()
    
    user_path = os.path.normpath(manager.user_path)    
    htpassword_file = os.path.normpath(manager.htpassword_file)

    form=cgi.FieldStorage()    
    user = form.getfirst('user')

    if not os.path.isdir(user_path):
        print_error('Path to users folder ' + user_path + ' was not found. User was not deleted.')
        return
        
    if not os.path.isfile(htpassword_file):
        delete_from_htpasswd = False
    
    userpath = os.path.join(user_path, user)
    if os.path.exists(userpath):
        shutil.rmtree(userpath)	
   
    if delete_from_htpasswd:
        subprocess.call(['htpasswd', '-D', htpassword_file, user])
        
    try:
        manager.delete_user(user)
    except RuntimeError:
        print_error('A user ' + user + ' was not found in the database.')
    else:
        print_response(user)
    finally:
        manager.save_database()

if __name__ == '__main__':
    main()
