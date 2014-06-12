#!/usr/bin/env python
#-*- mode: python; coding: utf-8 -*-

import noticias.obtenerNoticias

FRECUENCIA = 15

class Noticias:
  def __init__(self, configuracion):
    self.configuracion = configuracion

  def procesar(self, instante):
    if instante[1] % FRECUENCIA != 0:
      return None

    n = obtenerNoticias(self.configuracion.fuentes)
