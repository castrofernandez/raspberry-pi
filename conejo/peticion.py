#!/usr/bin/env python
#-*- mode: python; coding: utf-8 -*-
import sys
import datetime
import lib

LOG = './log/peticiones.txt'

def procesarAccion(serie, boton, rfid):
  resultado = lib.comando.procesarComando(serie, boton, rfid)
  lib.log.auditarPeticion(LOG, serie, boton, rfid, resultado)

  print resultado
if __name__=="__main__":
  import sys, argparse

  ejemplo = "%s --serie 0019db9e9367 --boton 1 --rfid d0021a0353063b72" % sys.argv[0]

  parser  = argparse.ArgumentParser( description=ejemplo )
  parser.add_argument('--serie',   "-s", help = 'Número de serie.', required = True )
  parser.add_argument('--boton',   "-b", help = 'Botón pulsado. Sí o no.', default = None )
  parser.add_argument('--rfid',  "-r", help = 'RFID posicionado sobre nariz.', default = None )
  args = parser.parse_args()

  if not args.serie == None:
    procesarAccion(args.serie, args.boton, args.rfid)
  else:
      print "Introduza número de serie."
