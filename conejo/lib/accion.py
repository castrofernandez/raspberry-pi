#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-

import os
from tts import obtenerMP3
#from log import auditarPeticion
import cola
from random import randint

import datetime
import logging

MENSAJE = os.path.join(os.path.dirname(__file__), "../audio/mensaje.mp3")
MENSAJE_RUTA = './audio/mensaje.mp3'

################################################################################
#                              CLASE COREOGRAFIA
################################################################################

class Coreografia(object):
  def procesar(self, acciones):
    return "\n".join(acciones)

class CoreografiaBasica(Coreografia):
  def __colores(self):
    colores = [Accion.color()]

    color = Accion.color()

    while color in colores:
      color = Accion.color()

    colores.append(color)

    color = Accion.color()

    while color in colores:
      color = Accion.color()

    colores.append(color)

    return colores

  def procesar(self):
    accion = Accion("serie")

    colores = self.__colores()

    acciones = [
                accion.luz(1, colores[0]),
                accion.esperar(1000),
                accion.luz(2, colores[1]),
                accion.esperar(1000),
                accion.luz(3, colores[2]),
                accion.esperar(1000),
                accion.apagar()
              ]

    c = super(CoreografiaBasica, self).procesar(acciones)
    coreografia = super(CoreografiaBasica, self).procesar([c, c, c, c, c, c, c, c, accion.panza(Accion.colorPanza())])

    return coreografia

################################################################################
#                                 CLASE ACCION
################################################################################

class Accion:
  colores = ['AMBER', 'GREEN', 'RED', 'TEAL','VIOLET', 'YELLOW']

  coloresPanza = ['Red', 'Green', 'Yellow', 'Violet',
                  'Teal', 'White', 'Orange']

  def __init__(self, serie):
    self.serie = serie

  def decir(self, texto):
    accion = obtenerMP3('ES', texto, MENSAJE, MENSAJE_RUTA)
    return accion

  def panza(self, color):
    if color not in Accion.coloresPanza:
      color = Accion.coloresPanza[0]

    return "BOTTOMCOLOR %s" % color

  def luz(self, led, color):
    if color not in Accion.colores:
      color = Accion.colores[0]

    led = int(led)
    if led not in [1, 2, 3]:
      led = 1

    return "LED%i %s" % (led, color)

  def apagar(self):
    return "LEDOFF"

  def esperar(self, tiempo):
    return "WAIT %i" % tiempo

  def giroIzquierda(self, sentido):
    sentido = self.__giro(sentido)
    return "LEFTTWITCH %i" % sentido

  def giroDerecha(self, sentido):
    sentido = self.__giro(sentido)
    return "RIGHTTWITCH %i" % sentido

  def arriba(self):
    return "EARSUP"

  def abajo(self):
    return "EARSDOWN"

  def dormir(self):
    return "SLEEP"

  def encolar(self, texto):
    cola.encolarComando(self.serie, texto)
    Accion.log(texto)
    #auditarPeticion(LOG, self.serie, None, None, texto)

  def __giro(self, sentido):
    sentido = int(sentido)
    return sentido if sentido in [0, 1] else 0

  @classmethod
  def color(cls):
    indice = randint(0, len(Accion.colores) - 1)
    return Accion.colores[indice]

  @classmethod
  def colorPanza(cls):
    indice = randint(0, len(Accion.coloresPanza) - 1)
    return Accion.coloresPanza[indice]

  @classmethod
  def encolarAccion(cls, serie, accion):
    cola.encolarComando(serie, accion)
    Accion.log(accion)
    #auditarPeticion(LOG, serie, None, None, accion)

  @classmethod
  def log(accion):
    fecha = str(datetime.date.today())
    LOG = os.path.join(os.path.dirname(__file__), "log/acciones_%s.log" % fecha)

    logging.basicConfig(filename = LOG, level = logging.ERROR)
    logging.info('%s %s' % (datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), accion))

################################################################################
#                                     MAIN
################################################################################

if __name__=="__main__":
  import sys, argparse

  ejemplo = "%s [--decir hola] [--luz 1-AMBER] [--apagar] [--esperar 1000] [--gizda 0] [--gizda 1] [--arriba] [--abajo] [--dormir] [--panza BOTTOMYELLOW]" % sys.argv[0]

  parser  = argparse.ArgumentParser(description = ejemplo)
  parser.add_argument('--decir',  "-d", help = 'Texto para decir.', default = None)
  parser.add_argument('--luz',  "-l", help = 'Led 1-AMBER.', default = None)
  parser.add_argument('--apagar',  "-a", help = 'Apagar luces.', action = 'store_true')
  parser.add_argument('--esperar',  "-e", help = 'Esperar X milisegundos.', default = None)
  parser.add_argument('--gizda',  "-i", help = 'Giro izquierda.', default = None)
  parser.add_argument('--gdcha',  "-c", help = 'Giro izquierda.', default = None)
  parser.add_argument('--arriba',  "-r", help = 'Orejas arriba.', action = 'store_true')
  parser.add_argument('--abajo',  "-b", help = 'Orejas abajo.', action = 'store_true')
  parser.add_argument('--dormir',  "-o", help = 'Orejas abajo.', action = 'store_true')
  parser.add_argument('--panza',  "-p", help = 'Color de panza.', default = None)
  args = parser.parse_args()

  accion = Accion("num_serie")

  if not args.decir == None:
    resultado = accion.decir(args.decir)
    Accion.encolarAccion(accion.serie, resultado)
  elif not args.luz == None:
    params = args.luz.split("-")

    if len(params) == 2:
      resultado = accion.luz(params[0], params[1])
      Accion.encolarAccion(accion.serie, resultado)
    else:
      print "Ej: --luz 1-AMBER"
  elif args.apagar == True:
    resultado = accion.apagar()
    Accion.encolarAccion(accion.serie, resultado)
  elif not args.esperar == None:
    resultado = accion.esperar(args.esperar)
    Accion.encolarAccion(accion.serie, resultado)
  elif not args.gizda == None:
    resultado = accion.giroIzquierda(args.gizda)
    Accion.encolarAccion(accion.serie, resultado)
  elif not args.gdcha == None:
    resultado = accion.giroDerecha(args.gdcha)
    Accion.encolarAccion(accion.serie, resultado)
  elif args.arriba == True:
    resultado = accion.arriba()
    Accion.encolarAccion(accion.serie, resultado)
  elif args.abajo == True:
    resultado = accion.abajo()
    Accion.encolarAccion(accion.serie, resultado)
  elif args.dormir == True:
    resultado = accion.dormir()
    Accion.encolarAccion(accion.serie, resultado)
  elif not args.panza == None:
    resultado = accion.panza(args.panza)
    Accion.encolarAccion(accion.serie, resultado)
  else:
    print "Introduza una acción."
