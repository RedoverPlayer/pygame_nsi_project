<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require './PHPMailer/src/Exception.php';
require './PHPMailer/src/PHPMailer.php';
require './PHPMailer/src/SMTP.php';

function sendMail($remoteaddr, $subject, $body) {
    print("<p>mail sent</p>");
    $mail = new PHPMailer();
    $mail->isSMTP();
    $mail->SMTPAuth = true;
    $mail->SMTPSecure = 'ssl';
    $mail->Host = 'azerty.com';
    $mail->Port = '465';
    $mail->isHTML();
    $mail->Username = 'azerty@gmail.com';
    $mail->Password = 'azerty';
    $mail->SetFrom('azerty@gmail.com','Server Name');
    
    $mail->Subject = $subject;
    $mail->Body = $body;
    $mail->AltBody = 'I love pancakes, have a nice day. btw you can \'t login because the verification failed';


    $mail->AddAddress($remoteaddr);
    //if you copy this please incremente the number of result
    $result42 = $mail->Send();

    if($result42 != 1) {
        print("An error occured");
    }
}
?>