<!DOCTYPE html>
<html>
<head>
  <title>Legendary Invention</title>
  <link rel="stylesheet" href="/legend.css" type="text/css">
</head>
<div id="header">
  <table id=headertable width=100%>
 <tr>
  <td align="left"><a href="/"><img width="100em" src="/images/logo.png" alt="logo.png" title="Home"></a></td>
  <td align="center"><a href="/" id="home" title="Home"><h1>PNM UEFA betting system</h1></a></td>
  <td align="right"><a href="/"><img width="100em" src="/images/logo.png" alt="logo.png" title="Home"></a></td>
 </tr>
</table>
</div>
<div align="right">Logged in as <?php echo $_SERVER['PHP_AUTH_USER'];?></div>

	<h3>Admin Area</h3>  
	<?php system(dirname(__FILE__).'/../../cgi/cgi_response.py '.'-f create_admin_table'); ?> 
	<form action="/cgi/update_gameslist.py" method="post">
		<input type="submit" value="Update Gameslist from Textfile"/>
	</form>	
	<form action="/cgi/delete_game.py" method="post">
		<input type="submit" value="Delete this game"/>
		<input type="text" name="gameid" maxlength="10" style="width: 10em" placeholder="Game ID"/>
	</form>
 
</body>
</html>
