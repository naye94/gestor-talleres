# -*- coding: utf-8 -*-
from config.db import supabase

class ServicioDao:
    def __init__(self):
        self.supabase = supabase

    def crear_servicio(self, servicio):
        response = self.supabase.table("servicio").insert({
            "nombre": servicio.nombre,
            "descripcion": servicio.descripcion,
            "costo": servicio.costo,
            "id_taller": servicio.id_taller
        }).execute()
        
        if response.data:
            return response.data[0].get("id_servicio")
        return None
    
    def actualizar_servicio(self, id_servicio, nombre, descripcion, costo, id_taller=None):
        datos_actualizar = {
            "nombre": nombre,
            "descripcion": descripcion,
            "costo": costo
        }
        # Si el controlador envía el id_taller, lo actualizamos también
        if id_taller is not None:
            datos_actualizar["id_taller"] = id_taller

        self.supabase.table("servicio").update(datos_actualizar).eq("id_servicio", id_servicio).execute()
    
    def borrar_servicio(self, id_servicio):
        self.supabase.table("servicio").delete().eq("id_servicio", id_servicio).execute()

    def obtener_todos(self):
        response = self.supabase.table("servicio").select("id_servicio, nombre, descripcion, costo, id_taller").execute()
        
        # Convertimos los diccionarios a tuplas con el orden exacto de tu antiguo mapeo MySQL
        servicios_tuplas = []
        if response.data:
            for s in response.data:
                servicios_tuplas.append((
                    s.get("id_servicio"),
                    s.get("nombre"),
                    s.get("descripcion"),
                    s.get("costo"),
                    s.get("id_taller")
                ))
        return servicios_tuplas
