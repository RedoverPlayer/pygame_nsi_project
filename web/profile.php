<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <title>Account</title>
    <!-- <link rel="stylesheet" href="styles.css"> -->
    <link rel="lazy css" href="https://some shit.css">
</head> 
<body>
    <h1>Profile page</h1>
    <a class="menu_button1" href="change_acc_info.php"> modify account </a>
</body>
</html>

<?php
    session_start();
    require('database.php');
    require('auth_checker.php');
    checkAuth($redirect=False);

    $tmp = $db->prepare('SELECT * FROM accounts WHERE id=:id');
    $tmp->execute([
        ':id' => $_SESSION['id'],
    ]);
    $result = $tmp->fetch();

    $seconds = $result['time_wasted'] % 60;
    $result['time_wasted'] = ($result['time_wasted'] - $seconds) / 60;
    $minutes = $result['time_wasted'] % 60;
    $hours = ($result['time_wasted'] - $minutes) / 60;

    print("<p class='p_info' class='rank'> your rank : " . $result['rank'] . " </p>");
    print("<p class='p_info' class='kd'> your kd : " . $result['kills']/$result['deaths'] . "1 if <1 then you suck otherwise your good </p>");
    print("<p class='p_info' class='time'> time you wasted : " . $hours. "h " . $minutes . "min " . $seconds ."sec </p>");
    print("<p class='p_info' class='kd'> your win rate : " . $result['win_game']/$result['tot_game'] . "1 if <1 then you suck otherwise your good </p>");
    print("<p class='p_info' class='kd'> the number of game you played : " . $result['tot_game'] . "</p>");

?>