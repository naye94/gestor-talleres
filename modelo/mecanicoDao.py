from config.db import get_connection
from modelo.mecanico import Mecanico

class MecanicoDao:
    def __init__(self):
        self.connection2 = get_connection()
    
    def crear_mecanico(self, mecanico):
        cursor = self.connection2.cursor()
        sql = '''INSERT INTO mecanico (nombre, apellido, especialidad, telefono, id_taller)
                VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(sql, (mecanico.nombre, mecanico.apellido, mecanico.especialidad, 
                             mecanico.telefono, mecanico.id_taller))
        self.connection2.commit()
        id_mecanico = cursor.lastrowid
        cursor.close()
        return id_mecanico
    
    def actualizar_mecanico(self, id_mecanico, nombre, apellido, especialidad, telefono):
        cursor = self.connection2.cursor()
        sql = '''UPDATE mecanico SET nombre = %s, apellido = %s, especialidad = %s, telefono = %s
        WHERE id_mecanico = %s'''
        cursor.execute(sql, (nombre, apellido, especialidad, telefono, id_mecanico))
        self.connection2.commit()
        cursor.close()
    
    def eliminar_mecanico(self, id_mecanico):
        cursor = self.connection2.cursor()
        sql = '''DELETE FROM mecanico WHERE id_mecanico = %s'''
        cursor.execute(sql, (id_mecanico,))
        self.connection2.commit()
        cursor.close()
    def obtener_todos(self):
        cursor = self.connection2.cursor()
        sql = "SELECT id_mecanico, nombre, apellido, especialidad, telefono, id_taller FROM mecanico"
        cursor.execute(sql)
        mecanicos = cursor.fetchall()
        cursor.close()
        return mecanicos