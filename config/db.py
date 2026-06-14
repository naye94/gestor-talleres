import os
from supabase import create_client, Client

# Pon tus credenciales reales aquí
SUPABASE_URL = "https://esaghoyruqyqqjvvfzeu.supabase.co" 
SUPABASE_KEY = "sb_publishable__y5-GG7L89wspXsi8dj_TA_ShyxFQ29" # Tu llave completa

# Creamos la instancia global del cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
import mysql.connector
from mysql.connector import errorcode
import re


def get_connection():
   return mysql.connector.connect(
        host="localhost",
        port=3306, 
        user="root",
        password="1234",
        database="prueba",

    )