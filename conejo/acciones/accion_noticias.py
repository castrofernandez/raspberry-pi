FRECUENCIA = 10

################################################################################
#                                  NOTICIAS
################################################################################

class Noticias:
  __noticiasLeidas = []

  def __init__(self, configuracion, accion):
    self.configuracion = configuracion
    self.accion = accion

  def ejecutar(self, instante):
    if instante[1] % FRECUENCIA != 0:
      return False

    n = obtenerNoticias(self.configuracion["fuentes"])

    elegida = self.comprobar(n)

    if elegida != None:
      accion = self.accion.decir(elegida)
      self.accion.encolar(accion)
      return True

    return False

  def comprobar(self, lista):
    elegida = None

    for noticia in lista.noticias:
      titulo = noticia[0]
      descripcion = noticia[1]
      enlace = noticia[2]

      if enlace not in self.__noticiasLeidas:
        self.__noticiasLeidas.append(enlace)
        elegida = titulo
        break;

    return elegida

################################################################################
#                                     AUX
################################################################################

import feedparser
import nltk

class ListaNoticias:
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
      resultado = ListaNoticias()
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

  resultado = ListaNoticias()

  longitud = 0

  for fuente in todas_noticias:
    longitud = max(longitud, fuente.longitud())

  for i in range(longitud):
    for fuente in todas_noticias:
      if (i >= fuente.longitud()):
        continue

      resultado.insertar(fuente.obtener(i)[0], fuente.obtener(i)[1], fuente.obtener(i)[2])

  return resultado
