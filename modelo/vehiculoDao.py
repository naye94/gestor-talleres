from config.db import get_connection

class VehiculoDao:
    def __init__(self):
        self.connection5 = get_connection()
    
    def crear_vehiculo(self, vehiculo):
        cursor = self.connection5.cursor()
        sql = '''INSERT INTO vehiculo (placa, marca, modelo, color, id_cliente, id_taller)
                VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(sql, (vehiculo.placa, vehiculo.marca, vehiculo.modelo, vehiculo.color, vehiculo.id_cliente, vehiculo.id_taller))
        self.connection5.commit()
        id_vehiculo = cursor.lastrowid
        return id_vehiculo
        
    def actualizar_vehiculo(self, id_vehiculo, placa, marca, modelo, color, id_cliente, id_taller):
        cursor = self.connection5.cursor()
        sql = '''UPDATE vehiculo SET placa = %s, marca = %s, modelo = %s, color = %s, id_cliente = %s, id_taller = %s
                WHERE id_vehiculo = %s'''
        cursor.execute(sql, (placa, marca, modelo, color, id_cliente, id_taller, id_vehiculo))
        self.connection5.commit()
        cursor.close()
    def borrar_vehiculo(self, id_vehiculo):
        cursor = self.connection5.cursor()
        sql = '''DELETE FROM vehiculo WHERE id_vehiculo = %s'''
        cursor.execute(sql, (id_vehiculo,))
        self.connection5.commit()
    def obtener_todos(self):
        cursor = self.connection5.cursor()
        sql = "SELECT id_vehiculo, placa, marca, modelo, color, id_cliente, id_taller FROM vehiculo"
        cursor.execute(sql)
        vehiculos = cursor.fetchall()
        cursor.close()
        return vehiculos