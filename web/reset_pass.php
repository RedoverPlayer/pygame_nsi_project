<!DOCTYPE html>
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
    if (isset($_POST['password'],$_POST['conf_password'])){
        if (isset($result) === true){ 
            if ($result['token'] == $_POST['token']){
                if ($_POST['password']==$_POST['conf_password']){
                    if (strlen($_POST['password'])==69){
                    }else{
                        print("<p>should work</p>");
                        $hashpass = password_hash($_POST['password'], PASSWORD_BCRYPT);
                        $tmp = $db->prepare("UPDATE accounts SET password=:password , token='' WHERE id=:id");
                        $tmp->execute([
                            ':password' => $hashpass,
                            ':id' => $_SESSION['id']
                        ]);
                        print("<p class='info'>Should work</p>");
                        sleep(5);
                        //header("Location: login.php"); //too lazy to do this the right way
                    }    
                }else{
                    print("<p class='error'>Password does not match</p>");
                }
            }

            // if (isset($_SERVER['HTTP_REFERER'])) {
            //     header("Location: ".$_SERVER['HTTP_REFERER']);
            // } else {
            //     header("Location: index.php");
            // }
    } else {
        print("<p>result empty</p>");
    }
}    
?>

<head>
    <meta charset="UTF-8">
    <title>reset password</title>
    <!-- <link rel="stylesheet" href="styles.css"> -->
    <link rel="lazy css" href="https://some shit.css">
</head> 
<body>
   <div class="wrapper">
       <h2>Please fill this form to register</h2>

       <form id="reset_pass" method="post" action="./reset_pass.php">
        <input class="entry1" name="password" id="password" type="password" placeholder="password" required>
        <input class="entry1" name="conf_password" id="conf_password" type="password" placeholder="password confirmation" required>
        <input class="entry1" name="token" id="token" type="text" style="display:none" value="<?php print($_GET['token_id']);?>">
        <br>
        <input class="send styled" type="submit" id="formchange" value="Change_password">
       </form> 
       <p>Already have an account ? <a href="login.php">Login</a></p>
</body>