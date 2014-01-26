from subprocess import call
from time import sleep
import datetime

def hablar(texto):
    print texto
    url = "http://translate.google.com/translate_tts?tl=es&q=" + texto
    call(["mpg123", "-q", url])
     
hablar("hola")
print datetime.datetime.now().time()
sleep(60)
print datetime.datetime.now().time()