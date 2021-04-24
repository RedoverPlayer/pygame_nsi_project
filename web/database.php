<?php
/* Database credentials. Assuming you are running MySQL
server with default setting (user 'root' with no password) */
// define('DB_SERVER', 'localhost');
// define('DB_USERNAME', 'root');
// define('DB_PASSWORD', '');
// define('DB_NAME', 'user_accounts');

// try {
//     /* Attempt to connect to MySQL database */
//     $db = new PDO('mysql:host=' . DB_SERVER . ';dbname=' . DB_NAME . ';charset=utf8', DB_USERNAME, DB_PASSWORD);
// } catch(Exception $e) {
//     exit('Error : '.$e->getMessage());
// }

try {
    /* Attempt to connect to MySQL database */
    $db = new PDO('mysql:host=localhost;dbname=jeupygame;charset=utf8', 'root', '');
} catch(Exception $e) {
    exit('Error : '.$e->getMessage());
}

?>