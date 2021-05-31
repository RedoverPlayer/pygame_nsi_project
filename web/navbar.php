<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=yes" />
    <title>Account</title>
    <link rel="lazy css" href="lazy css.css">
</head> 
<body>
 <link href="lazy css.css" rel="stylesheet" id="bootstrap-css">
 <script type="text/javascript" src="maybe i'll need it.js"></script>

 <nav class="navbar navbar-inverse navbar-fixed-top">
  <div class="topnav">
    <a class="active" href="profile.php"> Profile info </a>
    <a href="index.php"> Home page / index </a>
    <a href="ladder.php"> ladder </a>
    <a href="game_hist.php"> Hisotry </a>
    <a href="game_archives.php"> Game archives </a>
    <a href="logout.php"> Log out </a>   

    <div class="dropdown">
      <button class="dropbtn" onclick="toggleDiv()">
        <img class="profile4" src="<?php print("./pp/".$_SESSION['pp_name']); ?>" alt="your pp">  
      </button>
    </div>
</div>  
      <div class="dropdown-content" id="myDropdown">
        <!-- <ul>
          <li><a href="#">Link 1</a></li>
          <li><a href="#">Link 2</a></li>
          <li><a href="#">Link 3</a></li>
        </ul> -->
        <a href="#">Link 1</a>
        <a href="#">Link 2</a>
        <a href="#">Link 3</a>
      </div> 
   
    <script>
    /* When the user clicks on the button, 
    toggle between hiding and showing the dropdown content */
    function myFunction() {
      console.log("funct called")
      document.getElementById("myDropdown").classList.toggle("show");

    }

    function toggleDiv() {
    var x = document.getElementById("myDropdown");
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    }
}
    
    // Close the dropdown if the user clicks outside of it
    window.onclick = function(e) {
      if (!e.target.matches('.dropbtn')) {
      var myDropdown = document.getElementById("myDropdown");
        if (myDropdown.classList.contains('show')) {
          myDropdown.classList.remove('show');
        }
      }
    }
    </script>
  </div>
</body>