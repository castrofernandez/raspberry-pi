#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-

from hora import decirHora
from tts import obtenerMP3
import cola

def procesarComando(serie, boton, rfid):
  if boton == "3":
    return procesarAccionBoton()
  elif rfid != None and rfid != "":
    return procesarRFID(serie, rfid)
  else:
    return ejecutarAccionProgramada()

def procesarAccionBoton():
  return obtenerMP3('ES', "Me has tocado la cabeza", './audio/boton.mp3')

# RFID se encola porque la respuesta devuelta no se procesa
def procesarRFID(serie, rfid):
  accion = obtenerMP3('ES', "Me has tocado la nariz", './audio/rfid.mp3')
  cola.encolarComando(serie, accion)
  return accion

def ejecutarAccionProgramada():
  comando = cola.obtenerComando()

  if comando != None:
    return comando.comando
  else:
    return decirHora('./audio/hora.mp3')
