<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <title>Account</title>
    <!-- <link rel="stylesheet" href="styles.css"> -->
    <link rel="lazy css" href="https://some shit.css">
</head> 
<body>

   <div class="wrapper">
       <h2>Please fill this form to change your account info</h2>

       <form id="change" method="post" action="change_acc_info.php" enctype="multipart/form-data">
        <input class="entry1" name="username" id="username" type="text" placeholder="username" required>
        <input class="entry1" name="password" id="password" type="password" placeholder="password" required>
        Select your profile picture:
        <input type="file" name="fileToUpload" id="fileToUpload">

        <br>
        <input class="send styled" type="submit" id="formchange" value="Change">
       </form> 
       <p>Already have an account ? <a href="login.php">Login</a></p>

       <div class="test">
           <a href=#>link1</a>
           <a href=#>link2</a>
           <a href=#>link3</a>
       </div>

    </div>   
</body>

</html>

<?php

    session_start();
    require('database.php');
    require('gen_uid.php');
    require('auth_checker.php');
    checkAuth($redirect=False);
    require('navbar.php');
    if (isset($_POST['username'], $_POST['password'])){  
        $tmp = $db->prepare('SELECT * FROM accounts WHERE id=:id');
        $tmp->execute([
            ':id'=>$_SESSION['id']
        ]);
        $result = $tmp->fetch();
        if ($result==TRUE){
            if (password_verify($_POST['password'], $result['password'])) {
            $target_dir = "pp/";
            $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
            echo $target_file;
            $uploadOk = 1;
            $imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
            $im_name = basename($_FILES["fileToUpload"]["name"]);

            // Check if image file is a actual image or fake image
            if(isset($_POST["submit"])) {
                $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
                if($check !== false) {
                    echo "File is an image - " . $check["mime"] . ".";
                    $uploadOk = 1;
                } else {
                    echo "File is not an image.";
                    $uploadOk = 0;
                }
            }
            // Check if file already exists
            if (file_exists($target_file)) {
                echo "Sorry, file already exists.";
                $uploadOk = 0;
            }
            // Check file size
            if ($_FILES["fileToUpload"]["size"] > 500000) {
                echo "Sorry, your file is too large.";
                $uploadOk = 0;
            }
            // Allow certain file formats
            if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
                && $imageFileType != "gif" ) {
                echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
                $uploadOk = 0;
            }
            // Check if $uploadOk is set to 0 by an error
            if ($uploadOk == 0) {
                echo "Sorry, your file was not uploaded.";
            // if everything is ok, try to upload file
            } else {
                if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
                    echo "The file ". htmlspecialchars( basename( $_FILES["fileToUpload"]["name"])). " has been uploaded.";
                } else {
                    echo "Sorry, there was an error uploading your file.";
                }
            }
            print("<p> type :".gettype($im_name)."</p>");
            $tmp = $db->prepare("UPDATE accounts SET username=:username, pp_name=:pp_name WHERE id=:id");
            $tmp->execute([
                'username' => $_POST['username'],
                'id' => $_SESSION['id'],
                'pp_name' => $im_name
            ]);
            print("<p class='info'>your change are now gud</p>");
            //header("Location: login.php"); //too lazy to do this the right way
            }else{print("<p class='error'>Password does not match</p>");}
        }else{print("<p class='error'>your id bugged</p>");}
    }    
              
?>