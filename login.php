<?php

require 'connect.php';
require 'sample.php';
// echo "h1";


if(isset($_POST['submitbtn'])){
    
// echo "h2";
  $username = mysqli_real_escape_string($connection,$_POST['username']);
  $password = mysqli_real_escape_string($connection,$_POST['password']);

  

  $sql =  "SELECT `username`,`password` FROM users WHERE `username`='".$username."'and `password`='".$password."'limit 1";                                    
                
  $result = mysqli_query($connection,$sql);    

  
  if(empty($username) || empty($password))
  {
    echo "
    <script>
        alert('No user exist');
        window.location.href='./login.php' ;
    </script>
    ";
  }
  elseif (mysqli_num_rows($result)==1)
  {
  
    echo "<script>
    alert('successful');
    window.location.href='./login.php' ;
</script>";
     
  }
  else
  {
    echo "
    <script>
        alert('Invalid credentials');
        window.location.href='./login.php' ;
    </script>
    ";
    
  }
  

}  
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action="login.php" method="post">
        <div class="imgcontainer">
          <img src="img_avatar2.png" alt="Avatar" class="avatar">
        </div>
      
        <div class="container">
          <label for="uname"><b>Username</b></label>
          <input type="text" placeholder="Enter Username" name="username" required>
      
          <label for="psw"><b>Password</b></label>
          <input type="password" name="password" placeholder="Enter Password" name="psw" required>
      
          <button type="submit" name= "submitbtn">Login</button>
          <label>
            <input type="checkbox" checked="checked" name="remember"> Remember me
          </label>
        </div>
      
        <div class="container" style="background-color:#f1f1f1">
          <button type="button" class="cancelbtn">Cancel</button>
          <span class="psw">Forgot <a href="#">password?</a></span>
        </div>
      </form>
</body>
</html>