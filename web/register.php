<!DOCTYPE html>
<?php
    session_start();
    require('database.php');
    require('gen_uid.php');
    require('auth_checker.php');
    checkAuth($redirect=False);

    if (isset($_POST['username'],$_POST['email'],$_POST['password'],$_POST['conf_password'])){
        if ($_POST['password']==$_POST['conf_password']){
            $tmp = $db->prepare('SELECT * FROM accounts WHERE EMAIL=:email');
            $tmp->execute([
                ':email'=>$_POST['email']
            ]);
            $result = $tmp->rowCount();

            if ($result==0){
                if (strlen($_POST['password'])==69){
                    echo 'nice';
                }
                else{
                    $hashpass = password_hash($_POST['password'], PASSWORD_BCRYPT);
                    while (true) {
                        $id = gen_uid();
                        $tmp = $db->prepare('SELECT * FROM users_accounts WHERE ID=:id');
                        $tmp->execute([
                            ':id' => $id,
                        ]);
                        $result = $tmp->fetch();
        
                        if ($result == False) {
                            break;
                        }
                    }
                    $tmp = $db->prepare('INSERT INTO accounts (EMAIL, PASSWORD, USERNAME, ID) VALUES (:email, :password, :username, :id)');
                    $tmp->execute([
                        'email' => $_POST['email'],
                        'password' => $hashpass,
                        'username' => $_POST['username'],
                        'id' => $id
                    ]);
                    print("<p class='info'>Signup successful</p>");
                    //sleep(5);
                    //header("Location: login.php"); //too lazy to do this the right way
                    }

                }    
            }
        else{
            print("<p class='error'>Password does not match</p>");
        }
    }
?>



<head>
    <meta charset="UTF-8">
    <title>register</title>
    <!-- <link rel="stylesheet" href="styles.css"> -->
    <link rel="lazy css" href="https://some shit.css">
</head> 
<body>
   <div class="wrapper">
       <h2>Please fill this form to register</h2>

       <form id="login" method="post" action="./something.php">
        <input class="entry1" name="email" id="email" type="text" placeholder="email" required>
        <input class="entry1" name="username" id="username" type="text" placeholder="username" required>
        <input class="entry1" name="password" id="password" type="password" placeholder="password" required>
        <input class="entry1" name="conf_password" id="conf_password" type="password" placeholder="password confirmation" required>
        <br>
        <input class="send styled" type="submit" id="formregister" value="Register">
       </form> 
       <p>Already have an account ? <a href="login.php">Login</a></p>
</body>