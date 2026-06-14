# -*- coding: utf-8 -*-
import sys
import os
from config.db import supabase

class ClienteDao:
    def __init__(self):
        self.supabase = supabase
    
    def crear_cliente(self, cliente):
        response = self.supabase.table("cliente").insert({
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "telefono": cliente.telefono,
            "correo": cliente.correo
        }).execute()
        
        if response.data:
            return response.data[0].get("id_cliente")
        return None
    
    def obtener_clientes_por_taller(self, id_taller):
        # En Supabase hacemos el equivalente al JOIN consultando la tabla vehículo filtrada por taller
        response = self.supabase.table("vehiculo") \
            .select("id_taller, cliente(id_cliente, nombre, apellido, telefono, correo)") \
            .eq("id_taller", id_taller).execute()
        
        clientes_tuplas = set()  # Usamos un conjunto para emular el DISTINCT de SQL
        if response.data:
            for item in response.data:
                c = item.get("cliente")
                if c:
                    clientes_tuplas.add((
                        c.get("id_cliente"),
                        c.get("nombre"),
                        c.get("apellido"),
                        c.get("telefono"),
                        c.get("correo")
                    ))
        return list(clientes_tuplas)
    
    def obtener_cliente(self, id_cliente):
        response = self.supabase.table("cliente") \
            .select("nombre, apellido, telefono, correo") \
            .eq("id_cliente", id_cliente).execute()
        
        if response.data:
            c = response.data[0]
            return (c.get("nombre"), c.get("apellido"), c.get("telefono"), c.get("correo"))
        return None

    def actualizar_cliente(self, id_cliente, nombre, apellido, telefono, correo):
        self.supabase.table("cliente").update({
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono,
            "correo": correo
        }).eq("id_cliente", id_cliente).execute()

    def borrar_cliente_taller(self, id_cliente, id_taller):
        try:
            # 1. Eliminar vehículos del cliente en el taller específico
            self.supabase.table("vehiculo") \
                .delete() \
                .eq("id_cliente", id_cliente) \
                .eq("id_taller", id_taller).execute()
            
            # 2. Verificar si al cliente aún le quedan vehículos en otros talleres
            check_vehiculos = self.supabase.table("vehiculo") \
                .select("id_vehiculo") \
                .eq("id_cliente", id_cliente).execute()
            
            # 3. Si ya no tiene ningún vehículo registrado, se elimina el cliente por completo
            if not check_vehiculos.data:
                self.supabase.table("cliente").delete().eq("id_cliente", id_cliente).execute()
                
        except Exception as e:
            raise e

    def obtener_todos(self):
        response = self.supabase.table("cliente") \
            .select("id_cliente, nombre, apellido, telefono, correo").execute()
        
        clientes_tuplas = []
        if response.data:
            for c in response.data:
                clientes_tuplas.append((
                    c.get("id_cliente"),
                    c.get("nombre"),
                    c.get("apellido"),
                    c.get("telefono"),
                    c.get("correo")
                ))
        return clientes_tuplas

    def borrar_cliente(self, id_cliente):
        self.supabase.table("cliente").delete().eq("id_cliente", id_cliente).execute()
