#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-

from hora import decirHora
from tts import obtenerMP3

def procesarComando(serie, boton, rfid):
  #if boton == "3":
  #  return procesarAccionBoton()
  #elif rfid != None and rfid != "":
  #  return procesarRFID(rfid)
  #else:
  #  return ejecutarAccionProgramada()
  boton = "si" if boton == "3" else "no"
  nariz = "si" if rfid != None and rfid != "" else "no"
  return obtenerMP3('ES', "Boton %s y Nariz %s" % (boton, nariz), './audio/aux.mp3')

def procesarAccionBoton():
  return obtenerMP3('ES', "Me has tocado la cabeza", './audio/boton.mp3')

def procesarRFID(rfid):
  return obtenerMP3('ES', "Me has tocado la nariz", './audio/rfid.mp3')

def ejecutarAccionProgramada():
  return decirHora('./audio/hora.mp3')
