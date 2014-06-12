import os
import feedparser
import random
import nltk
import json

class Noticias:
    def __init__(self):
        self.noticias = []

    def insertar(self, titulo, resumen, enlace):
        self.noticias.append((titulo, resumen, enlace))

    def obtener(self, indice):
        return self.noticias[indice]

    def longitud(self):
        return len(self.noticias)

def obtenerNoticias(fuentes):
    # Retorno
    todas_noticias = []

    # Procesamos fuentes
    for fuente in fuentes:
        resultado = Noticias()
        todas_noticias.append(resultado)
        # Descargamos la fuente
        noticias = feedparser.parse(fuente)
        titulo_fuente = noticias['feed']['title']

        # Recorremos noticias
        for noticia in noticias['entries']:
            noticia_titulo =  noticia['title'].encode('UTF-8', 'replace')
            noticia_resumen = nltk.clean_html(noticia['summary']).encode('UTF-8', 'replace')
            noticia_enlace = noticia['link'].encode('UTF-8', 'replace')

            resultado.insertar(noticia_titulo, noticia_resumen, noticia_enlace)

    resultado = Noticias()

    longitud = 0

    for fuente in todas_noticias:
      longitud = max(longitud, fuente.longitud())

    for i in range(longitud):
      for fuente in todas_noticias:
        if (i >= fuente.longitud()):
          continue

        resultado.insertar(fuente.obtener(i)[0], fuente.obtener(i)[1], fuente.obtener(i)[2])

    return resultado

if __name__ == "__main__":
    print obtenerNoticias()
