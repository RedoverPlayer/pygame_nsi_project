<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <title>leader board</title>
    <!-- <link rel="stylesheet" href="styles.css"> -->
    <link rel="lazy css" href="https://some shit.css">
</head> 
<body>
   <h1>Ladder page</h1>
   <table>

   </table>
</body>
<?php 
     session_start();
     require('database.php');
     require('gen_uid.php');
     require('auth_checker.php');
     require('navbar.php');
     checkAuth($redirect=False);
 
    $tmp = $db->prepare('SELECT username, rank, win_game FROM accounts ORDER BY rank DESC');
    $tmp->execute([
    ]);
    $result = $tmp->fetchAll();
    echo "<table>";
    for ($i = 0; $i <= sizeof($result)-1; $i++) {
        print("<div class='leader_line'><tr><td>".$result[$i][0]."</td><td>".$result[$i][1]."</td><td> ".$result[$i][2]."</td></tr>");
    }
    echo "</table>";
?>
