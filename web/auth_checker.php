<?php
    function checkAuth($redirect=True) {
        require('database.php');
        if (isset($_SESSION['id'], $_SESSION['email'], $_SESSION['username'], $_SESSION['verified_email']) == False AND isset($_COOKIE['authentication_hash'])) {
            $sth = $db->prepare('SELECT * FROM users_accounts WHERE authentication_hash=:authentication_hash');
            $sth->execute([
                ':authentication_hash' => $result['authentication_hash'],
            ]);
            $result = $sth->fetch();
    
            if ($result == True AND isset($result['id'], $result['email'], $result['username'], $result['verified_email'])) {
                $_SESSION['id'] = $result['id'];
                $_SESSION['email'] = $result['email'];
                $_SESSION['username'] = $result['username'];
                $_SESSION['verified_email'] = $result['verified_email'];
            } else {
                header("Location: login.php");
            }
        } else if (isset($_SESSION['id'], $_SESSION['email'], $_SESSION['username'], $_SESSION['verified_email']) == False AND $redirect) {
            header("Location: login.php");
        }
    }

    function loginCookieAuthHash() {
        require('database.php');
        $sth = $db->prepare('SELECT * FROM users_accounts WHERE id=:id');
        $sth->execute([
            ':id' => $result['id'],
        ]);
        $result = $sth->fetch();

        if ($result == True) {
            if ($result['authentication_hash'] != "") {
                return($result['authentication_hash']);
            } else {
                $id = gen_uid(64);
                $sth = $db->prepare("UPDATE users_accounts SET password_verification_hash = :password_verification_hash WHERE id = :id");
                $sth->execute([
                    ':id' => $id,
                ]);
                return($id);
            }
        } else {
            print('<p class="info">An error occured</p>');
        }
    }
?>