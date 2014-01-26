from subprocess import call
from time import sleep
from datetime import date

def hablar(texto):
    print texto
    url = "http://translate.google.com/translate_tts?tl=es&q=" + texto
    call(["mpg123", "-q", url])
     
hablar("hola")
print date.now()
sleep(60)
print data.now()