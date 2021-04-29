<!DOCTYPE html>
<?php
    session_start();
    require('database.php');
    require('gen_uid.php');
    require('auth_checker.php');
    checkAuth($redirect=False);
    
    if (isset($_POST['email'])==true){
        $tmp = $db->prepare('SELECT * FROM accounts WHERE email=:email');
        $tmp->execute([
            ':email'=>$_POST['email']
        ]);
        $result = $tmp->fetch();
        if ($result==TRUE){
            $_SESSION['email_type']=1;
            header("http://" .$_SERVER['HTTP_HOST']. "/projectNSI/create_token.php");
            print("<a href='http://" .$_SERVER['HTTP_HOST']. "/projectNSI/create_token.php'>reset</a>");
        }else{
            print("<p class='error'>Email not found</p>");
        }
    }             
?>


<head>
    <meta charset="UTF-8">
    <title>login</title>
    <!-- <link rel="stylesheet" href="styles.css"> -->
    <link rel="lazy css" href="https://some shit.css">
</head> 
<body>
   <div class="wrapper">
       <h2>Please fill this form to send a email to reset your password </h2>

       <form id="reset1" method="post" action="./forgotten_pass.php">
        <input class="entry1" name="email" id="email" type="text" placeholder="email" required>
        <br>
        <input class="send styled" type="submit" id="formreset" value="send">
       </form> 
       <p>Don't have an account ? <a href="register.php">Sign Up</a></p>
       <p>Remembered your password ? <a href="login.php">Login</a></p>
</body>

