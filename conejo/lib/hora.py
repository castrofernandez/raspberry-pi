#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-
import sys
import datetime

from tts import obtenerMP3

def obtenerTiempo():
    ahora = datetime.datetime.now()
    
    hora = ahora.hour
    
    if hora > 12:
        hora -= 12
    
    minutos = ahora.minute
    
    if minutos == 0:
        minutos = "en punto"
    else:
        minutos = "y %i minuto%s" % (minutos, "" if minutos == 1 else "s")
    
    return "Son las %i %s" % (hora, minutos)

def decirHora(fichero):
    #obtenerMP3('ES', obtenerTiempo(), fichero)
    
    return "STREAM 192.168.1.192/vl/audio/hora.wav"
    #return "STREAM %s" % fichero

#if __name__=="__main__":
#    decirHora('./audio/hora.mp3')