import supabase
import os
import pytz

from dotenv import load_dotenv
from datetime import datetime

peru_tz=pytz.timezone("America/Lima")


load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")


cliente = supabase.create_client(url, key)

def upsertar_usuario(usuario):

    try:

        response=cliente.table("usuario").upsert(usuario).execute()

        return response.data[0]

    except Exception as e:

        print(f"Error en Upsertar usuario -> {e}")

        return 0
    
def leer_usuario(numero):
    
    response = (
    cliente.table("usuario")
    .select("*")
    .eq("numero",numero)
    .execute()
    )

    if(len(response.data)==0): return []
    return response.data[0]

def leer_reportes(dic):

    response = (
    cliente.table("reportes")
    .select("*")
    .eq("usuario",dic["usuario"])
    .eq("dia",dic["dia"])
    .execute()
    )

    if(len(response.data)==0): return []
    return response.data[0]

def upsertar_reportes(reporte):
    
    try:

        response=cliente.table("reportes").upsert(reporte).execute()

        return response.data[0]

    except Exception as e:

        print(f"Error en Upsertar usuario -> {e}")

        return 0

def upsertar_comidas(comidas):
    
    try:

        response=cliente.table("comidas").upsert(comidas).execute()

        return response.data[0]

    except Exception as e:

        print(f"Error en Upsertar usuario -> {e}")

        return 0
    
def upsertar_detallado(comidas):
    
    try:

        response=cliente.table("detallado").upsert(comidas).execute()

        return response.data[0]

    except Exception as e:

        print(f"Error en Upsertar usuario -> {e}")

        return 0

#upsertar_usuario({'numero':'whatsapp:+51927144823','nombre': 'Matias', 'peso': 92.0, 'altura': 177, 'nacimiento': '02-22-2003', 'ejercicio': 'No hace ejercicio', 'objetivo': 85, 'rapidez_objetivo': '8 semanas'})