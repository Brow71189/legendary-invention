#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Feb  7 10:40:41 2016

@author: Andi
"""

import database_manager
import argparse
import time
#import os
#import sys

def create_ranking_table(*args):
    manager = database_manager.BetBase()
    manager.read_config()
    try:
        userlist = manager.get_all_users_info()
    except TypeError:
        userlist = []
    print("""
    <table border="1" id="keywords" cellspacing="0" cellpadding="0">
    <script type="text/javascript">
	$(function(){
  	$('#keywords').tablesorter({sortList:[[2,0]]}); 
	});
    </script>
            <thead>
                <tr>
                    <th><span>Name</span></th>
                    <th><span>Points</span></th>
                    <th><span>Ranking</span></th>
                </tr>
            </thead>
        <tbody>""")
    for user in userlist:
        print("""\
                <tr>
                    <td>""" + user.get('name', 'unknown') + """</td>
                    <td>""" + user.get('points', '0') + """</td>
                    <td>""" + user.get('rank', str(len(userlist))) + """</td>
                </tr>""")
    
    print("""
        </tbody>
    </table>""")

def create_detailed_table(*args):
    manager = database_manager.BetBase()
    manager.read_config()
    try:
        userlist = manager.get_all_users_info()
    except TypeError:
        userlist = []
    else:
        userlist = sorted(userlist, key=lambda user: user.get('name', 'z'))
    gameslist = manager.get_all_games_info()
    gameslist = sorted(gameslist, key=lambda game: game.get('date', 'z'))
    now = time.strftime(manager.time_format)
    next_game = None
    for i in range(len(gameslist)):
        next_game = gameslist[i].get('date')
        if now < next_game:
            break

    print("""
    <a href="#""" + next_game + """\">Go to next game</a>
    <table border="1" id="detailed" cellspacing="0" cellpadding="0">
        <thead>
            <tr>
                <th>Day</th>
                <th>Time</th>
                <th>Match</th>
                <th>Result</th>""")
    for user in userlist:
        print("""\
                <th>""" + user.get('name', 'unknown') + """</th>"""
              )      
    
    print("""\
          </tr>
          </thead>
          <tbody>""")
    for i in range(len(gameslist)):
        print("""\
            <tr id=\"""" + gameslist[i].get('date') + """\">""")
            
        if not (i > 0 and gameslist[i].get('date')[:5] == gameslist[i-1].get('date')[:5]):
            rowspan=1
            while i+rowspan < len(gameslist) and gameslist[i+rowspan].get('date')[:5] == gameslist[i].get('date')[:5]:
                rowspan += 1
            print("""\
                <td rowspan=""" + str(rowspan) + """>""" +
                time.strftime('%B %d', time.strptime(gameslist[i].get('date'), manager.time_format)) +
                """</td>"""
                )
                
        print("""\
                <td>""" + 
                time.strftime('%H:%M', time.strptime(gameslist[i].get('date'), manager.time_format)) +
                """</td>
                <td>""" + 
                """<img width="25em" src="/images/flags/""" + gameslist[i].get('team1', '') + """.png" title=\"""" + 
                gameslist[i].get('name1', '') + """\">""" + gameslist[i].get('team1', '') + """-""" +
                gameslist[i].get('team2', '') +
                """<img width="25em" src="/images/flags/""" + gameslist[i].get('team2', '') + """.png" title=\"""" + 
                gameslist[i].get('name2', '') + """\">""" + 
                """</td>
                <td>""" + 
                gameslist[i].get('score1', '') + """-""" + gameslist[i].get('score2', '') +
                """</td>"""
                    )
        for user in userlist:
            if not user.get('tips') or not user['tips'].get(gameslist[i]['id']):
                print("""\
                <td> - </td>""")
            else:
                print("""\
                <td>""" + user['tips'][gameslist[i]['id']].get('score1', '') + """-""" +
                          user['tips'][gameslist[i]['id']].get('score2', '') + """</td>"""
                    )
        print("""\
            </tr>""")
    print("""\
            </tbody>
        </table>"""
        )

def create_betting_table(*args):
    manager = database_manager.BetBase()
    manager.read_config()
    gameslist = manager.get_all_games_info()
    gameslist = sorted(gameslist, key=lambda game: game.get('date', 'z'))
    userinfo = None
    if len(args) > 0:
        try:
            userinfo = manager.get_user_info(args[0])
        except AttributeError:
            pass
        
    print("""
    <form action="/cgi/submit_bet.py" method="post">
     <div align="center"><input id="submit" type="image" src="/images/submit.png" value="Submit"/></div>
     <input type="hidden" name="user" value=\"""" + args[0] + """\">
      <table border="1" id="betting" cellspacing="0" cellpadding="0">
        <thead>
            <tr>
                <th>Day</th>
                <th>Time</th>
                <th>Match</th>
                <th>Result</th>
                <th>Your bet</th>
           </tr>
        </thead>
        <tbody>""")
    for i in range(len(gameslist)):
        score1 = score2 = ''
        if userinfo and userinfo.get('tips'):
            tip = userinfo['tips'].get(gameslist[i].get('id'))
            if tip:
                score1 = tip.get('score1', '')
                score2 = tip.get('score2', '')
        
        disabled = ''
        if time.strftime(manager.time_format) > gameslist[i].get('date'):
            disabled = 'disabled'
                
        print("""\
            <tr>""")
            
        if not (i > 0 and gameslist[i].get('date')[:5] == gameslist[i-1].get('date')[:5]):
            rowspan=1
            while i+rowspan < len(gameslist) and gameslist[i+rowspan].get('date')[:5] == gameslist[i].get('date')[:5]:
                rowspan += 1
            print("""\
                <td rowspan=""" + str(rowspan) + """>""" +
                time.strftime('%B %d', time.strptime(gameslist[i].get('date'), manager.time_format)) +
                """</td>"""
                )
                
        print("""\
                <td>""" + 
                time.strftime('%H:%M', time.strptime(gameslist[i].get('date'), manager.time_format)) +
                """</td>
                <td>""" + 
                """<img width="25em" src="/images/flags/""" + gameslist[i].get('team1', '') + """.png" title=\"""" + 
                gameslist[i].get('name1', '') + """\">""" + gameslist[i].get('team1', '') + """-""" +
                gameslist[i].get('team2', '') +
                """<img width="25em" src="/images/flags/""" + gameslist[i].get('team2', '') + """.png" title=\"""" + 
                gameslist[i].get('name2', '') + """\">""" + 
                """</td>
                <td>""" + 
                gameslist[i].get('score1', '') + """-""" + gameslist[i].get('score2', '') + """</td>
                <td><input type="text" name="score1_""" + gameslist[i].get('id') +
                """" value=\"""" + score1 + """\" maxlength="2" style="width: 2em" """ + disabled + 
                """/>-<input type="text" name="score2_""" + gameslist[i].get('id') + """" value=\"""" + score2 +
                """\" maxlength="2" style="width: 2em" """ + disabled + """/></td>"""
                )

        print("""\
            </tr>""")
    print("""\
            </tbody>
        </table>
    </form>"""
      )
      
def create_admin_table(*args):
    manager = database_manager.BetBase()
    manager.read_config()
    gameslist = manager.get_all_games_info()
    gameslist = sorted(gameslist, key=lambda game: game.get('date', 'z'))
#    userinfo = None
#    if len(args) > 0:
#        userinfo = manager.get_user_info(args[0])
        
    print("""
    <form action="/cgi/submit_game_results.py" method="post">
     <input type="submit" value="Submit"/>
      <table border="1" id="betting" cellspacing="0" cellpadding="0">
        <thead>
            <tr>
                <th>Day</th>
                <th>Time</th>
                <th>Match</th>
                <th>ID</th>
                <th>Result</th>
           </tr>
        </thead>
        <tbody>""")
    for i in range(len(gameslist)):
#        score1 = score2 = ''
#        if userinfo and userinfo.get('tips'):
#            tip = userinfo['tips'].get(gameslist[i].get('id'))
#            if tip:
#                score1 = tip.get('score1', '')
#                score2 = tip.get('score2', '')
        
#        disabled = ''
#        if time.strftime(manager.time_format) > gameslist[i].get('date'):
#            disabled = 'disabled'
                
        print("""\
            <tr>""")
            
        if not (i > 0 and gameslist[i].get('date')[:5] == gameslist[i-1].get('date')[:5]):
            rowspan=1
            while i+rowspan < len(gameslist) and gameslist[i+rowspan].get('date')[:5] == gameslist[i].get('date')[:5]:
                rowspan += 1
            print("""\
                <td rowspan=""" + str(rowspan) + """>""" +
                time.strftime('%B %d', time.strptime(gameslist[i].get('date'), manager.time_format)) +
                """</td>"""
                )
                
        print("""\
                <td>""" + 
                time.strftime('%H:%M', time.strptime(gameslist[i].get('date'), manager.time_format)) +
                """</td>
                <td>""" + 
                """<img width="25em" src="/images/flags/""" + gameslist[i].get('team1', '') + """.png" title=\"""" + 
                gameslist[i].get('name1', '') + """\">""" + gameslist[i].get('team1', '') + """-""" +
                gameslist[i].get('team2', '') +
                """<img width="25em" src="/images/flags/""" + gameslist[i].get('team2', '') + """.png" title=\"""" + 
                gameslist[i].get('name2', '') + """\">""" + """</td>
                <td>""" + gameslist[i].get('id', '') + """</td>
                <td><input type="text" name="score1_""" + gameslist[i].get('id') +
                """" value=\"""" + gameslist[i].get('score1', '') +
                """\" maxlength="2" style="width: 2em"/>-<input type="text" name="score2_""" + gameslist[i].get('id') +
                """" value=\"""" + gameslist[i].get('score2', '') +
                """\" maxlength="2" style="width: 2em"/></td>"""
                )

        print("""\
            </tr>""")
    print("""\
            </tbody>
        </table>
  </form>"""
      )


if __name__ == '__main__':
    _functions = {'create_ranking_table': create_ranking_table, 'create_detailed_table': create_detailed_table,
                  'create_betting_table': create_betting_table, 'create_admin_table': create_admin_table}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user')
    parser.add_argument('-f', '--function')
    args = parser.parse_args()
    function = _functions.get(args.function)
    user = args.user
    if function is not None:
        function(user)
        
