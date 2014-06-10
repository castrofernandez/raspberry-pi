from subprocess import call
from time import sleep
import datetime
import noticias
import hora
import urllib

INICIO = 8
FIN = 21

def hablar(texto):
    print texto
    texto = urllib.quote(texto.encode('utf8'))
    url = "http://translate.google.com/translate_tts?tl=es&q=" + texto
    print url
    try:
        call(["mpg123", "-q", url])
    except:
        pass
        
def esperar(tiempo):
    minutos = tiempo / 60
    segundos = tiempo % 60
    print "Esperando " + str(minutos) + " minutos y " + str(segundos) + " segundos"
    sleep(tiempo)
   
def contarNoticias():
    # Obtenemos noticias
    n = noticias.obtenerNoticias()
    # Encabezado y noticias
    titulo = n.titulo
    n = n.noticias
    # Se dice encabezado
    hablar(titulo)
    for noticia in n:
        # Se dice encabezado
        hablar(noticia[0])
        # Se dice resumen
        hablar(noticia[1])
     
hablar("hola")

while(True):
    # Obtener hora
    ahora = datetime.datetime.now().time()
    print str(ahora.hour) + " horas y " + str(ahora.minute) + " minutos"
    if ahora.minute == 0:
        if ahora.hour >= INICIO and ahora.hour <= FIN:
            hablar(hora.queHoraEs(ahora.hour))
    elif ahora.minute % 5 == 0:
        contarNoticias() 
    esperar(60) # Se espera un minuto