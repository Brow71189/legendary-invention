<!DOCTYPE html>
<html>
<head>
  <title>Legendary Invention</title>
  <link rel="stylesheet" href="legend.css" type="text/css">
  <script type="text/javascript" src="js/jquery-1.10.2.min.js"></script>
  <script type="text/javascript" src="js/jquery.tablesorter.min.js"></script>
</head>
<body>
  <img width="34em" src="/images/lock.png" alt="lock.png">
  <a href="/users/" title="Log in">Log in to bet!</a>

  <h1>RANKING TABLE</h1>
  
  <?php system(dirname(__FILE__).'/cgi/cgi_response.py '.'-f create_ranking_table'); ?>

  <h1>DETAILED BETTING TABLE</h1>
  
  <?php system(dirname(__FILE__).'/cgi/cgi_response.py '.'-f create_detailed_table'); ?>


</body>
</html>
