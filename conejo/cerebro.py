import time
import rpyc
import threading
import signal
import pkgutil
import sys
import os
import imp
import json
import datetime

from rpyc.utils.server import ThreadedServer
from threading import Thread
from tendo import singleton

import logging

import lib

RUTA = os.path.dirname(__file__)
RUTA_ACCIONES = os.path.join(RUTA, "acciones")
FRECUENCIA = 60 # Una iteracion cada 60 segundos
CONFIGURACION = os.path.join(RUTA, "configuracion.json")
LOG = os.path.join(RUTA, "log/errores.log")

logging.basicConfig(filename = LOG, level = logging.ERROR)

################################################################################
#                                    BUCLE
################################################################################

class Bucle():
  __iteracion = None
  __acciones = None

  def __init__(self, configuracion):
    self.configuracion = json.load(open(configuracion))

  def iteracion(self):
    ahora = datetime.datetime.now()
    instante = (ahora.hour, ahora.minute)

    if self.estaDespierto(instante):
      self.__ejecutarAcciones(instante)

    self.__iteracion = threading.Timer(FRECUENCIA, self.iteracion)
    self.__iteracion.start()

  def arrancar(self):
    print "Cerebro pensando..."

    self.__acciones = self.__obtenerAcciones()
    self.iteracion()

  def parar(self):
    if self.__iteracion != None:
      self.__iteracion.cancel()

  def interrupcion(self, signal, frame):
    self.parar()
    print 'Encefalograma plano...'

  def estaDespierto(self, instante):
    if instante == None:
      ahora = datetime.datetime.now()
      instante = (ahora.hour, ahora.minute)

    hora = instante[0]
    return hora >= self.configuracion["despertar"] and hora < self.configuracion["dormir"]

  def __ejecutarAcciones(self, instante):
    for accion in self.__acciones:
      try:
        accion.ejecutar(instante)
      except Exception:
        logging.error('Error en accion', exc_info = True)

  def __obtenerAcciones(self):
    instancias = []

    a = lib.accion.Accion("serie")
    configuracion = self.configuracion

    acciones = pkgutil.iter_modules(path = [RUTA_ACCIONES])

    for loader, mod_name, ispkg in acciones:

      # Ensure that module isn't already loaded
      if mod_name.startswith("accion_") and mod_name not in sys.modules:

        # Import module
        fichero = RUTA_ACCIONES + "/" + mod_name + ".py"
        modulo = imp.load_source(mod_name, fichero)

        # Load class from imported module
        nombre_clase = self.__obtenerNombreClase(mod_name)
        clase = getattr(modulo, nombre_clase)

        # Create an instance of the class
        instancia = clase(configuracion, a)
        instancias.append(instancia)
        #instancia.ejecutar(instante)

    return instancias

  def __obtenerNombreClase(self, modulo):
    #Return the class name from a plugin name
    output = ""

    # Split on the _ and ignore the 1st word plugin
    words = modulo.split("_")[1:]

    # Capitalise the first letter of each word and add to string
    for word in words:
        output += word.title()
    return output

# Instancia de bucle
bucle = Bucle(CONFIGURACION)

################################################################################
#                                  SERVIDOR
################################################################################

class Servicio(rpyc.Service):
  def exposed_peticion(self, serie, boton, rfid):
    try:
      if not bucle.estaDespierto(None):
        return lib.accion.Accion(serie).dormir()
      elif boton == "3":
        return self.__procesarAccionBoton(serie)
      elif rfid != None and rfid != "":
        return self.__procesarRFID(serie, rfid)
      else:
        return self.__comprobarAccionesProgramadas()
    except Exception:
      logging.error('Error en peticion', exc_info = True)

  def __procesarAccionBoton(self, serie):
    return lib.accion.Accion(serie).decir("Me has tocado la cabeza")

  # RFID se encola porque la respuesta devuelta no se procesa
  def __procesarRFID(self, serie, rfid):
    accion = lib.accion.Accion(serie).decir("Me has tocado la nariz")
    lib.cola.encolarComando(serie, accion)
    return

  def __comprobarAccionesProgramadas(self):
    comando = lib.cola.obtenerComando()

    # Primero miramos si hay alguna accion encolada
    if comando != None:
      return comando.comando
    # Si no hay accion devolvemos una coreografia
    else:
      return lib.accion.CoreografiaBasica().procesar()

################################################################################
#                                  ARRANQUE
################################################################################

servidor = ThreadedServer(Servicio, port = 12345)
t = Thread(target = servidor.start)
t.daemon = True
t.start()

# Hacemos que solo exista un proceso de este scrip
programa = singleton.SingleInstance()

# Capturamos la interrupcion por teclado
signal.signal(signal.SIGINT, bucle.interrupcion)

# Arrancar bucle
bucle.arrancar()
