from subprocess import call
from time import sleep
import datetime

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
     
hablar("hola")
ahora = datetime.datetime.now().time()
# Esperamos a la siguiente hora
espera = (60 - ahora.minute) * 60 - ahora.second
esperar(espera)
hablar("es la hora")