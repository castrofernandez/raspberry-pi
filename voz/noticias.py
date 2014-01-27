import feedparser
import random
import nltk
import json

# Fuentes RSS obtenidas de fuentes.json
fuentes_json = open('fuentes.json')
fuentes = json.load(fuentes_json)['fuentes']

class Noticias:
    def __init__(self, titulo):
        self.titulo = titulo
        self.noticias = []
        
    def insertar(self, titulo, resumen):
        self.noticias.append((titulo, resumen))

def obtenerNoticias():
    # Seleccionamos una al azar
    fuente_seleccionada = fuentes[random.randint(0, len(fuentes) - 1)]
    # Descargamos la fuente
    noticias = feedparser.parse(fuente_seleccionada)
    # Se seleccionan 3 noticias al azar
    seleccionables = min(3, len(noticias['entries']))
    seleccionadas = []
    # Seleccionamos
    while len(seleccionadas) < seleccionables:
        seleccionada = random.randint(0, len(noticias['entries']) - 1)
        if (seleccionada not in seleccionadas):
            seleccionadas.append(seleccionada)
    # Creamos retorno
    # Encabezado de la fuente
    titulo = noticias['feed']['title']	
    retorno = Noticias(titulo)	
    
    for i in seleccionadas:
        retorno.insertar(noticias['entries'][i]['title'], nltk.clean_html(noticias['entries'][i]['summary']))
    
    return retorno
    
if __name__ == "__main__":
    print obtenerNoticias()
