FRECUENCIA = 60 # Cada 60 minutos

################################################################################
#                                     HORA
################################################################################

class Hora:
  def __init__(self, configuracion, accion):
    self.configuracion = configuracion
    self.accion = accion

  def ejecutar(self, instante):
    if instante[1] % FRECUENCIA != 0:
      return

    hora = self.__obtenerTiempo(instante)

    accion = self.accion.decir(hora)
    self.accion.encolar(accion)

  def __obtenerTiempo(self, instante):
      hora = instante[0]

      if hora > 12:
          hora -= 12

      minutos = instante[1]

      if minutos == 0:
          minutos = "en punto"
      else:
          minutos = "y %i minuto%s" % (minutos, "" if minutos == 1 else "s")

      hora = self.__horaEnTexto(hora)

      return "%s %s" % (hora, minutos)

  def __horaEnTexto(self, hora):
    if hora == 0 or hora == 12:
      return "Son las doce"
    elif hora == 1:
      return "Es la una"
    elif hora == 2:
      return "Son las dos"
    elif hora == 3:
      return "Son las tres"
    elif hora == 4:
      return "Son las cuatro"
    elif hora == 5:
      return "Son las cinco"
    elif hora == 6:
      return "Son las seis"
    elif hora == 7:
      return "Son las siete"
    elif hora == 8:
      return "Son las ocho"
    elif hora == 9:
      return "Son las nueve"
    elif hora == 10:
      return "Son las diez"
    elif hora == 11:
      return "Son las once"
