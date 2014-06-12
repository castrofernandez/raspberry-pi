#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-

from tts import obtenerMP3
from log import auditarPeticion
import cola

LOG = './log/acciones.txt'

################################################################################
#                                 CLASE ACCION
################################################################################

class Accion:
  __colores = ['AMBER', 'GREEN', 'RED', 'TEAL','VIOLET', 'YELLOW']

  def __init__(self, serie):
    self.serie = serie

  def decir(self, texto):
    accion = obtenerMP3('ES', texto, './audio/mensaje.mp3')
    return accion

  def luz(self, led, color):
    if color not in self.__colores:
      color = self.__colores[0]

    led = int(led)
    if led not in [1, 2, 3]:
      led = 1

    accion = "LED%i %s" % (led, color)
    return accion

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

  def __giro(self, sentido):
    sentido = int(sentido)
    return sentido if sentido in [0, 1] else 0

  @classmethod
  def encolarAccion(cls, serie, accion):
    cola.encolarComando(serie, accion)
    auditarPeticion(LOG, serie, None, None, accion)

################################################################################
#                                     MAIN
################################################################################

if __name__=="__main__":
  import sys, argparse

  ejemplo = "%s [--decir hola] [--luz 1-AMBER] [--apagar] [--esperar 1000] [--gizda 0] [--gizda 1]" % sys.argv[0]

  parser  = argparse.ArgumentParser(description = ejemplo)
  parser.add_argument('--decir',  "-d", help = 'Texto para decir.', default = None)
  parser.add_argument('--luz',  "-l", help = 'Led 1-AMBER.', default = None)
  parser.add_argument('--apagar',  "-a", help = 'Apagar luces.', default = None)
  parser.add_argument('--esperar',  "-e", help = 'Esperar X milisegundos.', default = None)
  parser.add_argument('--gizda',  "-i", help = 'Giro izquierda.', default = None)
  parser.add_argument('--gdcha',  "-c", help = 'Giro izquierda.', default = None)
  args = parser.parse_args()

  accion = Accion("num_serie")

  if not args.decir == None:
    resultado = accion.decir(args.decir)
    encolarAccion(accion.serie, resultado)
  elif not args.luz == None:
    params = args.luz.split("-")

    if len(params) == 2:
      resultado = accion.luz(params[0], params[1])
      Accion.encolarAccion(accion.serie, resultado)
    else:
      print "Ej: --luz 1-AMBER"
  elif not args.apagar == None:
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
  else:
    print "Introduza una acción."
