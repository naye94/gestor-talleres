import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modelo.cliente import Cliente
from config.db import get_connection

class ClienteDao:
    def __init__(self):
        self.connection = get_connection()
    
    def crear_cliente(self, cliente):
        cursor = self.connection.cursor()
        sql = "INSERT INTO cliente (nombre, apellido, telefono, correo)" \
        "VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (cliente.nombre, cliente.apellido, cliente.telefono, cliente.correo))
        self.connection.commit()
        id_cliente = cursor.lastrowid
        cursor.close()
        return id_cliente
    
    def obtener_clientes_por_taller(self, id_taller):
        cursor = self.connection.cursor()
        sql = '''SELECT DISTINCT c.id_cliente, c.nombre, c.apellido, c.telefono, c.correo
                FROM cliente c
                JOIN vehiculo v ON c.id_cliente = v.id_cliente
                JOIN taller t ON v.id_taller = t.id_taller
                WHERE t.id_taller = %s;'''
        cursor.execute(sql, (id_taller,))
        clientes = cursor.fetchall()
        cursor.close()
        return clientes
    
    def obtener_cliente(self, id_cliente):
        cursor = self.connection.cursor()
        sql = '''SELECT nombre, apellido, telefono, correo FROM cliente WHERE id_cliente = %s'''
        cursor.execute(sql, (id_cliente,))
        self.connection.commit()
        cliente = cursor.fetchone()
        cursor.close()
        return cliente

    def actualizar_cliente(self, id_cliente, nombre, apellido, telefono, correo):
        cursor = self.connection.cursor()
        sql = '''UPDATE cliente SET nombre = %s, apellido = %s, telefono = %s, correo = %s WHERE id_cliente = %s'''
        cursor.execute(sql, (nombre, apellido, telefono, correo, id_cliente))
        self.connection.commit()
        cursor.close()

    def borrar_cliente_taller(self, id_cliente, id_taller):
        cursor = self.connection.cursor()
        try:
            # Iniciar transacción explícitamente
            self.connection.start_transaction()

            # 1. Eliminar vehículos del cliente en el taller específico
            delete_vehiculo_sql = """
                DELETE FROM vehiculo 
                WHERE id_cliente = %s 
                AND id_taller = %s
            """
            cursor.execute(delete_vehiculo_sql, (id_cliente, id_taller))
            
            # 2. Eliminar cliente si ya no tiene vehículos
            delete_cliente_sql = """
                DELETE FROM cliente 
                WHERE id_cliente = %s
                AND NOT EXISTS (
                    SELECT 1 
                    FROM vehiculo 
                    WHERE id_cliente = %s
                )
            """
            cursor.execute(delete_cliente_sql, (id_cliente, id_cliente))
            
            # Confirmar transacción si todo va bien
            self.connection.commit()
            
        except Exception as e:
            # Revertir en caso de error
            self.connection.rollback()
            raise e  # Relanzar excepción para manejo externo
        finally:
            cursor.close()

    def obtener_todos(self):
        cursor = self.connection.cursor()
        sql = "SELECT id_cliente, nombre, apellido, telefono, correo FROM cliente"
        cursor.execute(sql)
        clientes = cursor.fetchall()
        cursor.close()
        return clientes
    def borrar_cliente(self, id_cliente):
        cursor = self.connection.cursor()
        sql = "DELETE FROM cliente WHERE id_cliente = %s"
        cursor.execute(sql, (id_cliente,))
        self.connection.commit()
        cursor.close()

