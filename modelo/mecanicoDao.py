# -*- coding: utf-8 -*-
from config.db import supabase

class MecanicoDao:
    def __init__(self):
        self.supabase = supabase
    
    def crear_mecanico(self, mecanico):
        response = self.supabase.table("mecanico").insert({
            "nombre": mecanico.nombre,
            "apellido": mecanico.apellido,
            "especialidad": mecanico.especialidad,
            "telefono": mecanico.telefono,
            "id_taller": mecanico.id_taller
        }).execute()
        
        if response.data:
            return response.data[0].get("id_mecanico")
        return None
    
    def actualizar_mecanico(self, id_mecanico, nombre, apellido, especialidad, telefono):
        self.supabase.table("mecanico").update({
            "nombre": nombre,
            "apellido": apellido,
            "especialidad": especialidad,
            "telefono": telefono
        }).eq("id_mecanico", id_mecanico).execute()
    
    def eliminar_mecanico(self, id_mecanico):
        self.supabase.table("mecanico").delete().eq("id_mecanico", id_mecanico).execute()

    def obtener_todos(self):
        response = self.supabase.table("mecanico").select("id_mecanico, nombre, apellido, especialidad, telefono, id_taller").execute()
        
        # Convertimos a tuplas respetando el orden exacto que utilizaba tu consulta MySQL
        mecanicos_tuplas = []
        if response.data:
            for m in response.data:
                mecanicos_tuplas.append((
                    m.get("id_mecanico"),
                    m.get("nombre"),
                    m.get("apellido"),
                    m.get("especialidad"),
                    m.get("telefono"),
                    m.get("id_taller")
                ))
        return mecanicos_tuplas
