from config.db import get_connection
from modelo.taller import Taller

class TallerDao:
    def __init__(self):
        self.connection4 = get_connection()

    def crear_taller(self, taller):
        cursor = self.connection4.cursor()
        sql = '''INSERT INTO taller (nombre, direccion, telefono) VALUES (%s, %s, %s)'''
        cursor.execute(sql, (taller.nombre, taller.direccion, taller.telefono))
        self.connection4.commit()
        id_taller = cursor.lastrowid
        return id_taller
    
    def actualizar_taller(self, id_taller, nombre, direccion, telefono):
        cursor = self.connection4.cursor()
        sql = '''UPDATE taller SET nombre = %s, direccion = %s, telefono = %s 
                WHERE id_taller = %s'''
        cursor.execute(sql, (nombre, direccion, telefono, id_taller))
        self.connection4.commit()
    
    def borrar_taller(self, id_taller):
        cursor = self.connection4.cursor()
        sql = '''DELETE FROM taller WHERE id_taller = %s'''
        cursor.execute(sql, (id_taller,))
        self.connection4.commit()
    
    def obtener_todos(self):
        cursor = self.connection4.cursor()
        sql = "SELECT id_taller, nombre, direccion, telefono FROM taller"
        cursor.execute(sql)
        talleres = cursor.fetchall()
        cursor.close()
        return talleres