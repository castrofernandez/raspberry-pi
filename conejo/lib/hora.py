#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-
import sys
import datetime

sys.path.append('./lib')
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

def decirHora():
    fichero = './audio/hora.mp3'
    obtenerMP3('ES', obtenerTiempo(), fichero)
    
    return "PLAY %s" % fichero

if __name__=="__main__":
    decirHora()