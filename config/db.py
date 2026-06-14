import os
from supabase import create_client, Client

SUPABASE_URL = "https://esaghoyruqyqqjvvfzeu.supabase.co"
# Pega aquí tu clave anon public real (la que empieza con eyJ...)
SUPABASE_KEY = "TU_CLAVE_LARGA_ANON_PUBLIC_DE_SUPABASE_AQUÍ" 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_connection():
    return supabase
