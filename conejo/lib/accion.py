#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-

from tts import obtenerMP3
from log import auditarPeticion
import cola

LOG = './log/acciones.txt'

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

    if led not in [1, 2, 3]:
      led = 1

    accion = "LED%i %s" % (led, color)
    return accion

  def apagar(self):
    return "LEDOFF"

  def esperar(self, tiempo):
    return "WAIT %i" % tiempo

def encolarAccion(serie, accion):
  cola.encolarComando(serie, accion)
  auditarPeticion(LOG, serie, None, None, accion)

if __name__=="__main__":
  import sys, argparse

  ejemplo = "%s [--decir hola] [--luz 1-AMBER] [--apagar] [--esperar 1000]" % sys.argv[0]

  parser  = argparse.ArgumentParser(description = ejemplo)
  parser.add_argument('--decir',  "-d", help = 'Texto para decir.', default = None)
  parser.add_argument('--luz',  "-l", help = 'Led 1-AMBER.', default = None)
  parser.add_argument('--apagar',  "-a", help = 'Apagar luces.', default = None)
  parser.add_argument('--esperar',  "-e", help = 'Esperar X milisegundos.', default = None)
  args = parser.parse_args()

  accion = Accion("num_serie")

  if not args.decir == None:
    resultado = accion.decir(args.decir)
    encolarAccion(accion.serie, resultado)
  elif not args.luz == None:
    params = args.luz.split("-")

    if len(params) == 2:
      resultado = accion.luz(params[0], params[1])
      encolarAccion(accion.serie, resultado)
    else:
      print "Ej: --luz 1-AMBER"
  elif not args.apagar == None:
    resultado = accion.apagar()
    encolarAccion(accion.serie, resultado)
  elif not args.esperar == None:
    resultado = accion.esperar(args.esperar)
    encolarAccion(accion.serie, resultado)
  else:
    print "Introduza una acción."
