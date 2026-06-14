# -*- coding: utf-8 -*-
from config.db import supabase  # SIEMPRE en la linea 1 y sin espacios al inicio

class UsuarioDao:
    @staticmethod
    def iniciar_sesion(email, password):
        try:
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            # Retornamos toda la respuesta de autenticacion de forma segura
            return auth_response
        except Exception as e:
            print(f"Error detectado en UsuarioDao: {e}")
            return None
