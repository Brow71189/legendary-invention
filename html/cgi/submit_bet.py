#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 15:40:36 2016

@author: Andi
"""

import cgi
import cgitb
import database_manager
import cgi_response

cgitb.enable()

def process_input(form):
    manager = database_manager.BetBase()
    manager.read_config()
    user = form['name'].value
   
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
                score2 = int(score1)
            except:
                score2 = None
        if not (score1 and score2):
            continue
        
        manager.add_or_update_tip(user, game, score1, score2)
    
    manager.save_database()
            

def print_response(form):
    print("""\
Content-type:text/html\r\n\r\n
<!DOCTYPE html>
<html>
    <head>
        <title>Legendary Invention</title>
        <link rel="stylesheet" href="/legend.css" type="text/css">
    </head>
    <body>
        Logged in as """ + #form['name'].value + """
    
        """<h1>YOUR BETS HAVE BEEN SUCCESSFULLY UPDATED!</h1>""")
    
    #cgi_response.create_betting_table(form['name'].value)
    print(form.list)
    
    print("""\
    </body>
</html>"""
        )
      

if __name__ == '__main__':
    form = cgi.FieldStorage()
#    process_input(form)
    print_response(form)
