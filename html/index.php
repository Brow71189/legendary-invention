<!DOCTYPE html>
<html>
<head>
  <title>Legendary Invention</title>
  <link rel="stylesheet" href="/legend.css" type="text/css">
  <script type="text/javascript" src="js/jquery-1.10.2.min.js"></script>
  <script type="text/javascript" src="js/jquery.tablesorter.min.js"></script>  
</head>
<body>
<div id="header">
  <table id=headertable width=100%>
 <tr>
  <td align="left"><a href="/"><img width="100em" src="/images/logo.png" alt="logo.png" title="Home"></a></td>
  <td align="center"><h1>PNM UEFA betting system</h1></td>
  <td align="right"><a href="/"><img width="100em" src="/images/logo.png" alt="logo.png" title="Home"></a></td>
 </tr>
</table>
</div>
<br>
<div align="right">
<a href="/users/"><img width="34em" src="/images/lock.png" alt="lock.png" title="Log in"></a>
<a href="/users/" title="Log in">start betting!</a>
</div>
  <h3>RANKING TABLE</h3>
  <?php system(dirname(__FILE__).'/cgi/cgi_response.py '.'-f create_ranking_table'); ?>
  <h3>DETAILED BETTING TABLE</h3>
  <?php system(dirname(__FILE__).'/cgi/cgi_response.py '.'-f create_detailed_table'); ?>
  <a href="/users/admin/" title="Admin Area">Admin Area</a>
</body>
</html>
