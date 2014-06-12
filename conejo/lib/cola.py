#!/usr/bin/python
#-*- mode: python; coding: utf-8 -*-

import sqlite3

BASE = "./bd/conejo.db"

class Comando:
  def __init__(self, id, serie, comando, fecha):
    self.id = id
    self.serie = serie
    self.comando = comando
    self.fecha = fecha

  def __str__(self):
    return "[id: %s, serie: %s, comando: %s, fecha: %s]" % (self.id, self.serie, self.comando, self.fecha)

def obtenerComando():
  conexion = sqlite3.connect(BASE)
  cursor = conexion.cursor()

  cursor.execute("SELECT * FROM cola ORDER BY id LIMIT 1")

  comando = None

  for fila in cursor:
    comando = Comando(fila[0], fila[1], fila[2], fila[3])
    break

  # Borrar comando
  if comando != None:
    cursor.execute("DELETE FROM cola WHERE id = %s" % comando.id)

  conexion.commit()
  conexion.close()

  return comando

def encolarComando(serie, comando):
  conexion = sqlite3.connect(BASE)
  cursor = conexion.cursor()

  cursor.execute('''INSERT INTO cola(serie, comando)
                  VALUES(?,?)''', (serie, comando))
  conexion.commit()
  conexion.close()
