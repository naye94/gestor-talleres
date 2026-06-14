# -*- coding: utf-8 -*-
from config.db import supabase

class TallerDao:
    def __init__(self):
        self.supabase = supabase

    def crear_taller(self, taller):
        # Insertamos los datos y solicitamos que devuelva la fila creada para capturar el ID
        response = self.supabase.table("taller").insert({
            "nombre": taller.nombre,
            "direccion": taller.direccion,
            "telefono": taller.telefono
        }).execute()
        
        if response.data:
            return response.data[0].get("id_taller")
        return None
    
    def actualizar_taller(self, id_taller, nombre, direccion, telefono):
        self.supabase.table("taller").update({
            "nombre": nombre,
            "direccion": direccion,
            "telefono": telefono
        }).eq("id_taller", id_taller).execute()
    
    def borrar_taller(self, id_taller):
        self.supabase.table("taller").delete().eq("id_taller", id_taller).execute()
    
    def obtener_todos(self):
        response = self.supabase.table("taller").select("id_taller, nombre, direccion, telefono").execute()
        
        # Convertimos la lista de diccionarios JSON en una lista de tuplas para mantener la estructura original
        talleres_tuplas = []
        if response.data:
            for t in response.data:
                talleres_tuplas.append((
                    t.get("id_taller"),
                    t.get("nombre"),
                    t.get("direccion"),
                    t.get("telefono")
                ))
        return talleres_tuplas
