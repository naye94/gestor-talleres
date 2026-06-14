from config.db import get_connection
from modelo.servicio import Servicio

class ServicioDao:
    def __init__(self):
        self.connection3 = get_connection()

    def crear_servicio(self, servicio):
        cursor = self.connection3.cursor()
        sql = '''INSERT INTO servicio (nombre, descripcion, costo, id_taller)
                VALUES (%s, %s, %s, %s)'''
        cursor.execute(sql, (servicio.nombre, servicio.descripcion, servicio.costo, servicio.id_taller))
        self.connection3.commit()
        id_servicio = cursor.lastrowid
        return id_servicio
    
    def actualizar_servicio(self, id_servicio, nombre, descripcion, costo):
        cursor = self.connection3.cursor()
        sql = '''UPDATE servicio SET nombre = %s, descripcion = %s, costo = %s
                WHERE id_servicio = %s'''
        cursor.execute(sql, (nombre, descripcion, costo, id_servicio))
        self.connection3.commit()
        cursor.close()

    def borrar_servicio(self, id_servicio):
        cursor = self.connection3.cursor()
        sql = '''DELETE FROM servicio WHERE id_servicio = %s'''
        cursor.execute(sql, (id_servicio,))
        self.connection3.commit()
        cursor.close()
    def obtener_todos(self):
        cursor = self.connection3.cursor()
        sql = "SELECT id_servicio, nombre, descripcion, costo, id_taller FROM servicio"
        cursor.execute(sql)
        servicios = cursor.fetchall()
        cursor.close()
        return servicios 