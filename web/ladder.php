<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <title>Sign Up</title>
    <!-- <link rel="stylesheet" href="styles.css"> -->
    <link rel="lazy css" href="https://some shit.css">
</head> 
<body>
   <h1>Ladder page page</h1>
</body>

<?php
    session_start();
    require('database.php');
    require('gen_uid.php');
    require('email.php');
    require('auth_checker.php');
    checkAuth();
?>    