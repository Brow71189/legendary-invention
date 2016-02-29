#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 18:21:58 2016

@author: Andi
"""

import database_manager
import cgi
import cgitb
cgitb.enable()

def print_response(gameid):
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
    
        <h3>GAME """ + gameid + """ HAS BEEN SUCCESSFULLY DELETED!</h3>
        <br><br>
        <p>You will be redirected to the admin area in 5 seconds. If not, use the following link:</p>
        <a href="/users/admin/" title="Admin Area">Admin Area</a>
    </body>
</html>""")


if __name__ == '__main__':
    form = cgi.FieldStorage()
    gameid = form.getvalue('gameid')
    manager = database_manager.BetBase()
    manager.delete_game(gameid)
    manager.update_points()
    print_response(gameid)