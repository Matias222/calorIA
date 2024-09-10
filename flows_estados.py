from api_models import ApiState
from fastapi import BackgroundTasks

import aux_functions
import agents
import twilio_functions
import calorias_pipeline
import random
import wrappers

def onboarding(state:ApiState):

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
        state.respuesta_usuario="Tu data fue registrada correctamente, estoy generando un plan personalizado, dame un minuto! 😎😎😎"

        #CALL PARA OBTENER EL PLAN PERSONALIZADO

        twilio_functions.enviar_mensaje(state.numero_enviar,state.respuesta_usuario)

        json_plan=agents.plan_personalizado(state.json_onboarding)

        state.json_onboarding["limite_calorias_diarias"]=json_plan["Maximo calorias"]

        state.respuesta_usuario=json_plan["Respuesta al usuario"]

def imagen(state:ApiState,imagen_url:str,background_tasks: BackgroundTasks):

    loaders=[
        f"Perfecto {state.nombre}, estoy analizando la imagen dame unos segundos 😁😁😁",
        f"Genial {state.nombre}, dejame que le doy un vistazo dame unos segundos 🔎🔎🔎"
    ]

    twilio_functions.enviar_mensaje(state.numero_enviar,loaders[random.randint(0,1)])

    dic,total_calorias=calorias_pipeline.get_image_info(imagen_url)

    respuesta_reporte=agents.reporte_comida(state.nombre,state.limite_calorias_diarias,dic)

    state.respuesta_usuario=respuesta_reporte

    background_tasks.add_task(wrappers.escribir_actualizar_reportes,state.numero_enviar,total_calorias,dic)

    #print(dic)

def base(state:ApiState):
    
    pass
    