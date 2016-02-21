<!DOCTYPE html>
<html>
<head>
  <title>Legendary Invention</title>
  <link rel="stylesheet" href="/legend.css" type="text/css">
 </head>
<body>
  Logged in as <?php echo $_SERVER['PHP_AUTH_USER'];?>

  <h1>PLACE YOUR BETS!</h1>
  
 <?php system(dirname(__FILE__).'/../cgi/cgi_response.py '.'-f create_betting_table'.' -u '.$_SERVER['PHP_AUTH_USER']); ?>


 
</body>
</html>
