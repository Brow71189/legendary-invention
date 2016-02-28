<!DOCTYPE html>
<html>
<head>
  <title>Legendary Invention</title>
  <link rel="stylesheet" href="/legend.css" type="text/css">
</head>
<body>
 Logged in as <?php echo $_SERVER['PHP_AUTH_USER'];?>

	<h1>Admin Area</h1>
	<a href="/" title="Home">Home</a>
  
	<?php system(dirname(__FILE__).'/../cgi/cgi_response.py '.'-f create_admin_table'); ?>
 
	<form action="/cgi/update_gameslist.py" method="post">
		<input type="submit" value="Update Gameslist from Textfile"/>
	</form>
	
	<form action="/cgi/delete_game.py" method="post">
		<input type="submit" value="Delete this game"/>
		<input type="text" name="gameid" maxlength="10" style="width: 10em"/>
	</form>
 
</body>
</html>
