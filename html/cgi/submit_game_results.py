#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 15:40:36 2016

@author: Andi
"""

import cgi
import cgitb
import database_manager
#import cgi_response
import time

cgitb.enable()

def process_input(form):
    manager = database_manager.BetBase()
    manager.read_config()
   
    for tip in form.keys():
        score1 = score2 = None
        if tip.startswith('score1'):
            game = tip.split('_')[1]
            score1 = form[tip].value
            try:
                score1 = int(score1)
            except:
                score1 = None
            score2 = form.getfirst('score2_' + game)
            try:
                score2 = int(score2)
            except:
                score2 = None
        if (score1 is None or score2 is None or
            time.strftime(manager.time_format) < manager.get_game_info(game).get('date')):
            continue
        
        manager.add_game_result(score1, score2, game)
    
    manager.update_points()    
    manager.save_database()
            

def print_response(form):
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
        <h3>GAME RESULTS SUCCESSFULLY UPDATED!</h3>
        <br><br>
        <p>You will be redirected to the admin area in 5 seconds. If not, use the following link:</p>
        <a href="/users/admin/" title="Admin Area">Admin Area</a>
    </body>
</html>"""
        )
      

if __name__ == '__main__':
    form = cgi.FieldStorage()
    process_input(form)
    print_response(form)
