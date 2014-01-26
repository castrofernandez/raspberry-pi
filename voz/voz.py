from subprocess import call
from time import sleep
import datetime

INICIO = 8
FIN = 21

def hablar(texto):
    print texto
    url = "http://translate.google.com/translate_tts?tl=es&q=" + texto
    try:
        call(["mpg123", "-q", url])
    except:
        pass
        
def esperar(tiempo):
   minutos = tiempo / 60
   segundos = tiempo % 60
   print "Esperando " + str(minutos) + " minutos y " + str(segundos) + " segundos"
   sleep(tiempo)
   
def hora(h):
    if h > 12:
        h -= 12
    if h == 1:
        hablar("Es la una")
    elif h == 2:
        hablar("Son las dos")
    elif h == 3:
        hablar("Son las tres")
    elif h == 4:
        hablar("Son las cuatro")
    elif h == 5:
        hablar("Son las cinco")
    elif h == 6:
        hablar("Son las seis")
    elif h == 7:
        hablar("Son las siete")
    elif h == 8:
        hablar("Son las ocho")
    elif h == 9:
        hablar("Son las nueve")
    elif h == 10:
        hablar("Son las diez")
    elif h == 11:
        hablar("Son las once")
    else:
        hablar("Son las doce")
     
hablar("hola")
ahora = datetime.datetime.now().time()
# Esperamos a la siguiente hora
espera = (60 - ahora.minute) * 60 - ahora.second
esperar(espera)
while(True):
    ahora = datetime.datetime.now().time()
    if ahora.hour >= INICIO and ahora.hour <= FIN:
        hora(ahora.hour)
    esperar(3600) # Se espera a la siguiente hora