import os
from supabase import create_client, Client

SUPABASE_URL = "https://esaghoyruqyqqjvvfzeu.supabase.co"
# Pega aquí tu clave anon public real (la que empieza con eyJ...)
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzYWdob3lydXF5cXFqdnZmemV1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEzODU1MTcsImV4cCI6MjA5Njk2MTUxN30.AQTmAy3EaBPdHfev8298mPakbFa06fF5d_lIqKQ2MCQ" 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_connection():
    return supabase
