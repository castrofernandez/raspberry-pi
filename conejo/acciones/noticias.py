#!/usr/bin/env python
#-*- mode: python; coding: utf-8 -*-
import sys
import datetime
import lib
import json

LOG = './log/peticiones.txt'
CONFIGURACION = json.load(open('./configuracion.json'))

dormir = lib.accion.Accion("serie").dormir()

def estaDespierto(instante):
  hora = instante[0]

  return hora >= CONFIGURACION["despertar"] and hora < CONFIGURACION["dormir"]

def procesarAccion(serie, boton, rfid):
  ahora = datetime.datetime.now().time()
  instante = (ahora.hour, ahora.minute)

  if not estaDespierto(instante):
    print dormir
    return

  resultado = lib.comando.Comando(CONFIGURACION).procesarComando(instante, serie, boton, rfid)
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
