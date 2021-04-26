<!DOCTYPE html>
<?php
    session_start();
    require('database.php');
    require('gen_uid.php');
    require('auth_checker.php');
    checkAuth($redirect=False);

    if (isset($_POST['email'],$_POST['password'])){
        $tmp = $db->prepare('SELECT * FROM accounts WHERE email=:email');
        $tmp->execute([
            ':email'=>$_POST['email']
        ]);
        $result = $tmp->fetch();
        if ($result==TRUE){
            if (password_verify($_POST['password'], $result['password'])) {
                $_SESSION['id'] = $result['id'];
                $_SESSION['email'] = $result['email'];
                $_SESSION['username'] = $result['username'];
                $_SESSION['verif_email'] = $result['verif_email'];
                if ($result['verif_email']==1){
                    // if (isset($_POST['http_referer'])) {
                    //     header("Location: " . $_POST['http_referer']);
                    // } else {
                    header("Location: index.php");
                    // }
                }else{
                    print("<a href='http://" .$_SERVER['HTTP_HOST']. "/projectNSI/create_token.php'>Verify your email</a>");
                    }
            }else{
                print("<p class='error'>Wrong password</p>");
            }
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
       <h2>Please fill this form to login</h2>

       <form id="login" method="post" action="./login.php">
        <input class="entry1" name="email" id="email" type="text" placeholder="email" required>
        <input class="entry1" name="password" id="password" type="password" placeholder="password" required>
        <br>
        <input class="send styled" type="submit" id="formlogin" value="Login">
       </form> 
       <p>Don't have an account ? <a href="register.php">Sign Up</a></p>
</body>