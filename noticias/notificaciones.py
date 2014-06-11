from time import sleep
import datetime
import noticias
import hora
import httplib
import urllib

# Horas de funcionamiento
INICIO = 8
FIN = 21
# Numero maximo de notificaciones simultaneas
MAX_NOTICIAS_SIMULTANEAS = 1
MINUTOS_ENTRE_NOTICIAS = 20

# Noticias ya enviadas
noticias_enviadas = []
# Pushover
pushover_user = "uZKUiXbKvtqHHLbkNtSBtTn9Fr4h42"
pushover_token = "anUDKCVeHT1gSg3Yh1kHyYJogG12iL"

def notificar(titulo, descripcion, enlace):
    print titulo

    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
        "token": pushover_token,
        "user": pushover_user,
        "message": descripcion,
        "title": titulo,
        "url": enlace,
        "url_title": "Ver noticia"
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

def esperar(tiempo):
    minutos = tiempo / 60
    segundos = tiempo % 60
    print "Esperando " + str(minutos) + " minutos y " + str(segundos) + " segundos"
    sleep(tiempo)

def contarNoticias():
    # Obtenemos noticias
    ns = noticias.obtenerNoticias()
    # Encabezado y noticias
    ns = ns.noticias

    enviadas = 0

    for noticia in ns:
        if enviadas == MAX_NOTICIAS_SIMULTANEAS:
          break;

        titulo = noticia[0]
        descripcion = noticia[1]
        enlace = noticia[2]

        if enlace not in noticias_enviadas:
          noticias_enviadas.append(enlace)
          notificar(titulo, descripcion, enlace)
          enviadas += 1

minutos = MINUTOS_ENTRE_NOTICIAS;

while(True):
    # Obtener hora
    ahora = datetime.datetime.now().time()

    print str(ahora.hour) + " horas y " + str(ahora.minute) + " minutos"

    if ahora.hour >= INICIO and ahora.hour <= FIN and minutos == MINUTOS_ENTRE_NOTICIAS:
        contarNoticias()

    esperar(60) # Se espera un minuto

    minutos += 1

    if minutos > MINUTOS_ENTRE_NOTICIAS:
      minutos = 0
