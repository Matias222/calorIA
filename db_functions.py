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

def leer_comidas(dic):

    response = (
    cliente.table("comidas")
    .select("*")
    .eq("reporte",dic["reporte"])
    .execute()
    )

    if(len(response.data)==0): return []
    return response.data

def leer_detallado(dic):

    response = (
    cliente.table("detallado")
    .select("*")
    .eq("comida",dic["comida"])
    .execute()
    )

    if(len(response.data)==0): return []
    return response.data

def upsertar_reportes(reporte):
    
    try:

        response=cliente.table("reportes").upsert(reporte).execute()

        return response.data[0]

    except Exception as e:

        print(f"Error en Upsertar reportes -> {e}")

        return 0

def upsertar_comidas(comidas):
    
    try:

        response=cliente.table("comidas").upsert(comidas).execute()

        return response.data[0]

    except Exception as e:

        print(f"Error en Upsertar comidas -> {e}")

        return 0
    
def upsertar_detallado(comidas):
    
    try:

        response=cliente.table("detallado").upsert(comidas).execute()

        return response.data[0]

    except Exception as e:

        print(f"Error en Upsertar usuario -> {e}")

        return 0

def ultima_comida(id_reporte):

    response = (
    cliente.table("comidas")
    .select("*")
    .eq("reporte",id_reporte)
    .order("hora", desc=True)
    .limit(1)
    .execute()
    )

    if(len(response.data)==0): return []
    return response.data[0]


def delete_row(tabla,columna,id):
    cliente.table(tabla).delete().eq(columna,id).execute()

def borrar_data_matias():

    reporte=leer_reportes({"usuario":"whatsapp:+51927144823","dia":"2024-09-12"})

    print(reporte)

    id=reporte["id"]

    comidas=leer_comidas({"reporte":id})

    print(comidas)

    for i in comidas:

        detallados=leer_detallado({"comida":i["id"]})
        
        for j in detallados: delete_row("detallado","id",j["id"])
        
        delete_row("comidas","id",i["id"])

    delete_row("reportes","id",reporte["id"])

#upsertar_reportes({"usuario":"whatsapp:+51927144823","calorias":"3860","dia":"2024-09-12"})
#upsertar_usuario({'numero':'whatsapp:+51927144823','nombre': 'Matias', 'peso': 92.0, 'altura': 177, 'nacimiento': '02-22-2003', 'ejercicio': 'No hace ejercicio', 'objetivo': 85, 'rapidez_objetivo': '8 semanas'})
#borrar_data_matias()