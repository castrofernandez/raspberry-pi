#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-

from tts import obtenerMP3
from log import auditarPeticion
import cola

LOG = './log/acciones.txt'

class Accion:
  def __init__(self, serie):
    self.serie = serie

  def decir(self, texto):
    accion = obtenerMP3('ES', texto, './audio/mensaje.mp3')
    cola.encolarComando(self.serie, accion)
    auditarPeticion(LOG, self.serie, None, None, accion)

if __name__=="__main__":
  import sys, argparse

  ejemplo = "%s [--decir hola]" % sys.argv[0]

  parser  = argparse.ArgumentParser(description = ejemplo)
  parser.add_argument('--decir',  "-d", help = 'Texto para decir.', default = None)
  args = parser.parse_args()

  accion = Accion("num_serie")

  if not args.decir == None:
    accion.decir(args.decir)
  else:
    print "Introduza una acción."
