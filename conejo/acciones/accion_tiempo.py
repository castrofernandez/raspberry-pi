import urllib2
import xml.etree.ElementTree as ElementTree

FRECUENCIA = 2 # Cada 2 horas
HOY = 0
MANANA = 1

################################################################################
#                                  TIEMPO
################################################################################

class Tiempo:
  def __init__(self, configuracion, accion):
    self.configuracion = configuracion
    self.accion = accion

  def ejecutar(self, instante):
    if instante[0] % FRECUENCIA != 0 and minuto == 30:
      return

    tiempo = self.__obtenerTiempo(HOY)

    accion = self.accion.decir(tiempo)
    self.accion.encolar(accion)

  def __obtenerTiempo(self, dia):
    ciudad = 278

    url = "http://api.tiempo.com/index.php?api_lang=es&localidad=%i&affiliate_id=jyh5d619qtwg" % ciudad

    xml = urllib2.urlopen(url).read()
    raiz = ElementTree.fromstring(xml)

    pronostico = raiz.find('location').findall('var')

    minima = pronostico[0].find('data').findall('forecast')[dia].attrib['value']
    maxima = pronostico[1].find('data').findall('forecast')[dia].attrib['value']
    descripcion = pronostico[5].find('data').findall('forecast')[dia].attrib['value']

    descripcion = descripcion.encode('utf8')

    pronostico = ""

    if dia == HOY:
      pronostico = "Tiempo para hoy"
    else:
      pronostico = "Tiempo para mañana"

    pronostico = "%s %s. Minima: %s grados y maxima: %s grados" %(pronostico, descripcion, minima, maxima)

    return pronostico
