from api_models import ApiState
from fastapi import BackgroundTasks
from datetime import datetime

import aux_functions
import agents
import twilio_functions
import calorias_pipeline
import random
import wrappers
import storage_functions
import db_functions
import pytz
import cadenas

peru_tz=pytz.timezone("America/Lima")


def onboarding(state:ApiState):

    if(len(state.buffer)==1): state.background_tasks.add_task(storage_functions.crear_bucket,state.numero_enviar)

    json_rpta=agents.onboarding_agent(state.buffer)
    
    state.respuesta_usuario=json_rpta["Respuesta al usuario"]
    estado_agente=json_rpta["Estado"]

    print(estado_agente)

    if(estado_agente=="FINALIZACION"):

        state.json_onboarding=json_rpta["Datos"]
        state.json_onboarding["nacimiento"]=aux_functions.convertir(state.json_onboarding["nacimiento"])

        #Aca tengo que generar el plan y guardarlo en la bd

        state.buffer=[]
        state.estado_conversa="BASE"


        state.respuesta_usuario=cadenas.onboarding_bajar

        try:
            if(int(state.json_onboarding["peso"])<int(state.json_onboarding["objetivo"])): state.respuesta_usuario=cadenas.onboarding_subir
        except:
            state.respuesta_usuario=cadenas.onboarding_subir

        #CALL PARA OBTENER EL PLAN PERSONALIZADO

        twilio_functions.enviar_mensaje(state.numero_enviar,state.respuesta_usuario)

        json_plan=agents.plan_personalizado(state.json_onboarding)

        state.json_onboarding["limite_calorias_diarias"]=json_plan["Maximo calorias"]

        state.respuesta_usuario=json_plan["Respuesta al usuario"]+"\n\nQuedo atento a las fotos de tus comidas! 📷"

def imagen(state:ApiState,imagen_url:str):

    loaders=[
        f"Perfecto {state.nombre}, estoy analizando la imagen dame unos segundos 😁😁😁",
        f"Genial {state.nombre}, dejame que le doy un vistazo dame unos segundos 🔎🔎🔎"
    ]

    twilio_functions.enviar_mensaje(state.numero_enviar,loaders[random.randint(0,1)])

    dic,total_calorias=calorias_pipeline.get_image_info(imagen_url)

    respuesta_reporte=agents.reporte_comida(state.nombre,state.limite_calorias_diarias,dic)

    state.respuesta_usuario=respuesta_reporte

    state.background_tasks.add_task(wrappers.escribir_actualizar_reportes,state.numero_enviar,total_calorias,dic,imagen_url)

    #print(dic)

def base(state:ApiState):
    
    peru_time = datetime.now(peru_tz)
    formatted_date = peru_time.strftime("%m/%d/%Y")   
    
    dic_reportes=db_functions.leer_reportes({"usuario":state.numero_enviar,"dia":formatted_date})
    
    try:
        calorias_consumidas=dic_reportes["calorias"]
        comidas=db_functions.leer_comidas({"reporte":dic_reportes["id"]})
    except:
        calorias_consumidas=0
        comidas=[]

    comidas_filtrado=[]

    for i in comidas: comidas_filtrado.append({"comida":i["comida"],"calorias":i["calorias"]})

    rpta=agents.consulta_generales(state,comidas_filtrado,calorias_consumidas)

    state.respuesta_usuario=rpta