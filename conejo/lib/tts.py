#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-
import urllib, urllib2
from os import path
#from pydub import AudioSegment

def obtenerMP3(idioma, mensaje, nombre = None):
    base  = "http://translate.google.com/translate_tts"
    valores   = { 'q': mensaje, 'tl': idioma }
    data     = urllib.urlencode(valores)
    peticion  = urllib2.Request(base, data)
    peticion.add_header("User-Agent", "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11" )
    respuesta = urllib2.urlopen(peticion)

    if (nombre == None):
        nombre = "_".join(mensaje.split())

    aux = nombre + ".aux.mp3"
    ofp = open(aux, "wb")
    ofp.write(respuesta.read())

    # Aumentar volumen
    #cancion = AudioSegment.from_mp3(aux)

    # Aumentar decibelios
    #cancion = cancion + 10

    #cancion.export(nombre, "mp3")

    return "PLAY %s" % nombre

def procesarLista(idioma, fichero):
    ifp = open(fichero)
    for linea in ifp:
        linea = linea.strip()
        obtenerMP3(idioma, linea, nombre = linea + ".mp3")
    ifp.close()
    return

#if __name__=="__main__":
#    import sys, argparse

#    ejemplo = "%s --idioma ES --mensaje 'HOLA' --nombre fichero.mp3" % sys.argv[0]

#    parser  = argparse.ArgumentParser( description=ejemplo )
#    parser.add_argument('--idioma',   "-i", help = 'Idioma: Japonés = ja, Inglés = en, etc.', required = True )
#    parser.add_argument('--mensaje',   "-m", help = 'Texto a sintetizar.', default = None )
#    parser.add_argument('--lista',  "-l", help = 'Fichero a procesar, una frase por línea.', default = None )
#    parser.add_argument('--nombre',  "-n", help = 'Fichero de salida .mp3', default = None )
#    args = parser.parse_args()

#    if not args.mensaje==None:
#        obtenerMP3(args.idioma, args.mensaje, args.nombre)
#    elif not args.lista==None:
#        procesarLista(args.idioma, args.lista)
#    else:
#        print "Introduza un mensaje (--mensaje) o una lista (--lista)."
