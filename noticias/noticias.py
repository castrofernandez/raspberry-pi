import os
import feedparser
import random
import nltk
import json

# Fuentes RSS obtenidas de fuentes.json
os.chdir(os.path.expanduser('~') + '/Desarrollo/raspberry-pi/noticias')
fuentes_json = open('fuentes.json')
fuentes = json.load(fuentes_json)['fuentes']

class Noticias:
    def __init__(self):
        self.noticias = []

    def insertar(self, titulo, resumen, enlace):
        self.noticias.append((titulo, resumen, enlace))

def obtenerNoticias():
    # Retorno
    retorno = Noticias()

    # Procesamos fuentes
    for fuente in fuentes:
        # Descargamos la fuente
        noticias = feedparser.parse(fuente)
        titulo_fuente = noticias['feed']['title']
        # Recorremos noticias
        for noticia in noticias['entries']:
            noticia_titulo =  noticia['title'].encode('UTF-8', 'replace')
            noticia_resumen = nltk.clean_html(noticia['summary']).encode('UTF-8', 'replace')
            noticia_enlace = noticia['link'].encode('UTF-8', 'replace')

            retorno.insertar(noticia_titulo, noticia_resumen, noticia_enlace)

    return retorno

if __name__ == "__main__":
    print obtenerNoticias()
