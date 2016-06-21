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
import time

cgitb.enable()

def process_input(form):
    manager = database_manager.BetBase()
    manager.read_config()
    user = form.getvalue('user')
   
    for tip in form.keys():
        score1 = score2 = None
        if tip.startswith('score1'):
            game = tip.split('_')[1]
            score1 = form[tip].value
            try:
                score1 = int(score1)
                assert score1 >= 0
            except:
                score1 = None
            score2 = form.getfirst('score2_' + game)
            try:
                score2 = int(score2)
                assert score2 >= 0
            except:
                score2 = None
        if (score1 is None or score2 is None or
            time.strftime(manager.time_format) > manager.get_game_info(game).get('date')):
            continue
        
        manager.add_or_update_tip(user, game, score1, score2)
    
    manager.save_database()
            

def print_response(form):
    print("""\
Content-type:text/html\r\n\r\n
<!DOCTYPE html>
<html>
    <head>
        <title>PNM Betting</title>
        <link rel="stylesheet" href="/legend.css" type="text/css">
    </head>
    <body>
         <div id="header">
      	 <table id=headertable width=100%>
                 <tr>
                     <td align="left"><a href="/"><img width="100em" src="/images/logo.png" alt="logo.png" title="Home"></a></td>
                     <td align="center"><a href="/" id="home" title="Home"><h1>PNM UEFA betting system</h1></a></td>
                     <td align="right"><a href="/"><img width="100em" src="/images/logo.png" alt="logo.png" title="Home"></a></td>
                </tr>
            </table>
	</div>
	<div align="right">Logged in as """ + form.getvalue('user') + """</div>
            
        <h3>BETS SUCCESSFULLY UPDATED!</h3>""")
    
    cgi_response.create_betting_table(form.getvalue('user'))
    
    print("""\
    </body>
</html>"""
        )
      

if __name__ == '__main__':
    form = cgi.FieldStorage()
    process_input(form)
    print_response(form)
