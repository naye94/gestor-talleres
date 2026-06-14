# -*- coding: utf-8 -*-
from config.db import supabase

class VehiculoDao:
    def __init__(self):
        self.supabase = supabase
    
    def crear_vehiculo(self, vehiculo):
        response = self.supabase.table("vehiculo").insert({
            "placa": vehiculo.placa,
            "marca": vehiculo.marca,
            "modelo": vehiculo.modelo,
            "color": vehiculo.color,
            "id_cliente": vehiculo.id_cliente,
            "id_taller": vehiculo.id_taller
        }).execute()
        
        if response.data:
            return response.data[0].get("id_vehiculo")
        return None
        
    def actualizar_vehiculo(self, id_vehiculo, placa, marca, modelo, color, id_cliente, id_taller):
        self.supabase.table("vehiculo").update({
            "placa": placa,
            "marca": marca,
            "modelo": modelo,
            "color": color,
            "id_cliente": id_cliente,
            "id_taller": id_taller
        }).eq("id_vehiculo", id_vehiculo).execute()
        
    def borrar_vehiculo(self, id_vehiculo):
        self.supabase.table("vehiculo").delete().eq("id_vehiculo", id_vehiculo).execute()

    def obtener_todos(self):
        response = self.supabase.table("vehiculo").select("id_vehiculo, placa, marca, modelo, color, id_cliente, id_taller").execute()
        
        # Mapeamos los diccionarios a tuplas con el orden exacto de tu antiguo cursor
        vehiculos_tuplas = []
        if response.data:
            for v in response.data:
                vehiculos_tuplas.append((
                    v.get("id_vehiculo"),
                    v.get("placa"),
                    v.get("marca"),
                    v.get("modelo"),
                    v.get("color"),
                    v.get("id_cliente"),
                    v.get("id_taller")
                ))
        return vehiculos_tuplas
