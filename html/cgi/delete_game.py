# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 18:21:58 2016

@author: Andi
"""

import database_manager
import cgitb
cgitb.enable()
import cgi

def print_response(gameid):
    print("""\
Content-type:text/html\r\n\r\n
<!DOCTYPE html>
<html>
    <head>
        <title>Legendary Invention</title>
        <link rel="stylesheet" href="/legend.css" type="text/css">
    </head>
    <body>
        Logged in as <?php echo $_SERVER['PHP_AUTH_USER'];?>
    
        <h1>GAME """ + gameid + """ HAS BEEN SUCCESSFULLY UPDATED!</h1>
        <a href="/" title="Home">Home</a>
        <a href="/users/admin/" title="Admin Area">Admin Area</a>
    </body>
</html>""")


if __name__ == '__main__':
    form = cgi.FieldStorage()
    gameid = form.getvalue('gameid')
    manager = database_manager.BetBase()
    manager.read_config()
    manager.delete_game(gameid)
    manager.update_points()
    manager.save_database()
    print_response(gameid)