<?php
    session_start();
    require('database.php');
    require('gen_uid.php');
    require('email.php');
    require('auth_checker.php');
    checkAuth();

    print("<p>start create toke</p>");
    $token_id = gen_uid();
    $tmp = $db->prepare("UPDATE accounts SET token= :token_id WHERE id=:id");
    $tmp ->execute([
        'token_id'=>$token_id,
        'id'=>$_SESSION['id'],
    ]);
    //idk why there's a ' after the "HOST"]." but it works so i'll keep it
    //0 for email verif and 1 for rest password
    if ($_SESSION['email_type']==0){
        SendMail($_SESSION['email'], "Verify your email", "<h1>Jeu en cours de développement, nom sujet à modifications </h1><h2>Please verify your email by clicking this link : <a href='http://" . $_SERVER['HTTP_HOST'] . "/projectNSI/verif_email.php?token_id=" . $token_id . "'>Verify your email</a></h2>");
    } elseif ($_SESSION['email_type']==1){
        SendMail($_SESSION['email'], "Verify your email", "<h1>Jeu en cours de développement, nom sujet à modifications </h1><h2>you can change your password by clicking this link : <a href='http://" . $_SERVER['HTTP_HOST'] . "/projectNSI/reset_pass.php?token_id=" . $token_id . "'>Reset your password</a></h2>");
    }

    if (isset($_SERVER['HTTP_REFERER'])) {
        header("Location: ".$_SERVER['HTTP_REFERER']);
    } else {
        header("Location: index.php");
    }
?>    
