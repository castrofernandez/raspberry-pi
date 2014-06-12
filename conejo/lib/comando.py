#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-

from hora import decirHora
from tts import obtenerMP3
import cola
import accion

################################################################################
#                               PROCESAR COMANDO
################################################################################
class Comando:
  def __init__(self, configuracion):
    self.configuracion = configuracion

  def procesarComando(self, instante, serie, boton, rfid):
    if boton == "3":
      return self.procesarAccionBoton()
    elif rfid != None and rfid != "":
      return self.procesarRFID(serie, rfid)
    else:
      return self.ejecutarAccionProgramada(instante)

################################################################################
#                               BOTON PULSADO
################################################################################

  def procesarAccionBoton(self):
    return obtenerMP3('ES', "Me has tocado la cabeza", './audio/boton.mp3')

################################################################################
#                               TARJETA RFID
################################################################################

  # RFID se encola porque la respuesta devuelta no se procesa
  def procesarRFID(self, serie, rfid):
    accion = obtenerMP3('ES', "Me has tocado la nariz", './audio/rfid.mp3')
    cola.encolarComando(serie, accion)
    return accion

################################################################################
#                               ACCION PROGRAMADA
################################################################################

  def ejecutarAccionProgramada(self, instante):
    comando = cola.obtenerComando()

    # Primero miramos si hay alguna accion encolada
    if comando != None:
      return comando.comando
    # Comprobamos si toca decir la hora
    elif self.configuracion["reloj"] == True and instante[1] == 0:
      return decirHora('./audio/hora.mp3')
    # Si no hay accion encolada miramos las acciones programadas
    else:
      return accion.CoreografiaBasica().procesar()
