#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-

import pkgutil
import sys
import os
import imp

from hora import decirHora
from tts import obtenerMP3
import cola
import accion

RUTA = os.path.join(os.path.dirname(__file__), "../acciones")
ACCIONES = pkgutil.iter_modules(path = [RUTA])

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
      self.recorrerAcciones(instante) # Se encolan
      return accion.CoreografiaBasica().procesar()

################################################################################
#                               EJECUTAR ACCIONES
################################################################################

  def recorrerAcciones(self, instante):

    a = accion.Accion("serie")
    configuracion = self.configuracion

    for loader, mod_name, ispkg in ACCIONES:

      # Ensure that module isn't already loaded
      if mod_name.startswith("accion_") and mod_name not in sys.modules:

        # Import module
        fichero = RUTA + "/" + mod_name + ".py"
        modulo = imp.load_source(mod_name, fichero)

        # Load class from imported module
        nombre_clase = self.get_class_name(mod_name)
        clase = getattr(modulo, nombre_clase)

        # Create an instance of the class
        instancia = clase(configuracion, a)

        instancia.ejecutar(instante)

################################################################################
#                                       AUX
################################################################################

  def get_class_name(self, mod_name):
    #Return the class name from a plugin name
    output = ""

    # Split on the _ and ignore the 1st word plugin
    words = mod_name.split("_")[1:]

    # Capitalise the first letter of each word and add to string
    for word in words:
        output += word.title()
    return output
