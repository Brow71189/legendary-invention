<!DOCTYPE html>
<html>
<head>
  <title>Legendary Invention</title>
  <link rel="stylesheet" href="/legend.css" type="text/css">
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
<div align="right">Logged in as <?php echo $_SERVER['PHP_AUTH_USER'];?></div>
  <h3>PLACE YOUR BETS!</h3>
 <?php system(dirname(__FILE__).'/../cgi/cgi_response.py '.'-f create_betting_table'.' -u '.$_SERVER['PHP_AUTH_USER']); ?>
</body>
</html>
