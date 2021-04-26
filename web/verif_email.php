<?php
    session_start();
    require('database.php');
    // if (isset($_SESSION['id']) == false and isset($_GET['token_id'])){
    //     if (isset($_SERVER['HTTP_REFERER'])) {
    //         header("Location: ".$_SERVER['HTTP_REFERER']);
    //     } else {
    //         header("Location: index.php");
    //     } 
    // }
    $tmp = $db->prepare("SELECT * FROM accounts WHERE id=:id");
    $tmp ->execute([
        ':id' => $_SESSION['id']
    ]);
    $result = $tmp->fetch();
    if (isset($result) === true){
        if ($result['token'] == $_GET['token_id']){
            $tmp = $db->prepare("UPDATE accounts SET verif_email=1, token='' WHERE id=:id");
            $tmp -> execute([
                ':id'=> $_SESSION['id']
            ]);
            if (isset($_SERVER['HTTP_REFERER'])) {
                header("Location: ".$_SERVER['HTTP_REFERER']);
            } else {
                header("Location: index.php");
            }
        } else {
            print("<p>Invalid email verification hash</p>");
        }    
    } else {
        print("<p>wrong id (idk why)</p>");
    }
?>