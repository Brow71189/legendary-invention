#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Feb  7 10:40:41 2016

@author: Andi
"""

import database_manager
import argparse
import time

def create_ranking_table():
    manager = database_manager.BetBase()
    manager.read_config()
    userlist = manager.get_all_users_info()
    print("""
    <table border="1" id="keywords" cellspacing="0" cellpadding="0">
    <script type="text/javascript">
	$(function(){
  	$('#keywords').tablesorter(); 
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

def create_detailed_table():
    manager = database_manager.BetBase()
    manager.read_config()
    userlist = manager.get_all_users_info()
    userlist = sorted(userlist, key=lambda user: user.get('name', 'z'))
    gameslist = manager.get_all_games_info()
    gameslist = sorted(gameslist, key=lambda game: game.get('date', 'z'))
    print("""
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
              
    print("""
            </tr>
        </thead>
        <tbody>""")
    for i in range(len(gameslist)):
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
                """<img width="25em" src="images/flags/""" + gameslist[i].get('team1', '') + """.png" title=\"""" + 
                gameslist[i].get('name1', '') + """\">""" + gameslist[i].get('team1', '') + """-""" +
                gameslist[i].get('team2', '') +
                """<img width="25em" src="../images/flags/""" + gameslist[i].get('team2', '') + """.png" title=\"""" + 
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

if __name__ == '__main__':
    _functions = {'create_ranking_table': create_ranking_table, 'create_detailed_table': create_detailed_table}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user')
    parser.add_argument('-f', '--function')
    args = parser.parse_args()
    function = _functions.get(args.function)
    if function is not None:
        function()
        
