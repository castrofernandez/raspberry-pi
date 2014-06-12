#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-
import time
import locale

def auditarPeticion(fichero, serie, boton, rfid):
  #locale.setlocale(locale.LC_TIME, "es_ES")
  hora = time.strftime("%a, %d %b %Y %H:%M:%S")

  linea = "%s - serie: %s botón: %s RFID: %s \n" % (hora, serie, boton, rfid)

  ofp = open(fichero, "a")
  ofp.write(linea)
