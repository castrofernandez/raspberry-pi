<?php
  echo 1;
  $command = escapeshellcmd('/Users/castrofernandez/Desarrollo/raspberry-pi/peticion.py');
  //$output = shell_exec($command);
  //echo $output;

  //echo 2;

$python = `python peticion.py`;
echo $python;
