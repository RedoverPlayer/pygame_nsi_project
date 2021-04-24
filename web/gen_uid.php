<?php
    function gen_uid($l=28) {
        $str = "";
        for ($x=0;$x<$l;$x++) $str .= substr(str_shuffle("0123456789abcdefghijklmnopqrstuvwxyz"), 0, 1);    
        return $str;
    }
?>