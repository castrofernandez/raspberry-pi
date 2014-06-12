<?php

  /* Botón superior */
  if(isset($_GET['sd']))
    $boton = $_GET['sd'];
  else
    $boton = 0;

  /* Número de serie */
  $serie = $_GET['sn'];

  /* RFID */
  if(isset($_GET['rf']))
    $rfid = "--rfid " . $_GET['rf'];
  else
    $rfid = "";

  $comando = "python peticion.py --serie $serie --boton $boton $rfid 2>&1";

  $python = `$comando`;
  echo $python;

//exec("python peticion.py 2>&1", $output);
//var_dump( $output);
