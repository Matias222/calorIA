from fastapi import FastAPI, Request, Form, Depends, BackgroundTasks
from typing import Optional
from api_models import ApiState, Recordatorio


import db_functions
import twilio_functions
import flows_estados

app = FastAPI()

async def extraer_json(request:Request):
    return await request.form()

@app.post("/whatsapp-webhook")
def whatsapp_webhook(background_tasks: BackgroundTasks, request: bytes=Depends(extraer_json)):

    from_number = request["From"]
    message_body = request["Body"]
    message_type = request["MessageType"]

    if(from_number=="whatsapp:+51996568784"): return

    data_usuario=db_functions.upsertar_usuario({"numero":from_number})

    state=ApiState(buffer=data_usuario["buffer"],estado_conversa=data_usuario["estado_conversa"],numero_enviar=from_number,limite_calorias_diarias=data_usuario["limite_calorias_diarias"],nombre=data_usuario["nombre"],background_tasks=background_tasks,nacimiento=data_usuario["nacimiento"],objetivo=data_usuario["objetivo"],peso=data_usuario["peso"],is_pay=data_usuario["is_pay"],num_fotos=data_usuario["num_fotos"])

    #print(state.is_pay,state.num_fotos)

    if(state.is_pay==False and state.num_fotos>3):
        twilio_functions.enviar_mensaje(state.numero_enviar,f"Estimad@ {state.nombre}, haz agotado tu prueba gratuita 🥺.\n\nEl costo de la subscripción es de 20 soles al mes, puedes comunicarte al *+51927144823* para adquirirla.\n\nCada dia estas mas cerca de alcanzar tu meta. \n\nHemos hecho progreso juntos, pero solo es el inicio.\n\nNo te rindas 💪")
        return 

    state.buffer.append(f"Usuario: {message_body}")

    if(state.estado_conversa=="ONBOARDING"):
        flows_estados.onboarding(state)

    elif(state.estado_conversa=="BASE"):

        if(message_type=="image"): flows_estados.imagen(state,request["MediaUrl0"])
        else: flows_estados.base(state)

    state.buffer.append(f"IA: {state.respuesta_usuario}")

    data_usuario=db_functions.upsertar_usuario({"numero":state.numero_enviar,"buffer":state.buffer,"estado_conversa":state.estado_conversa,"num_fotos":state.num_fotos}|state.json_onboarding)

    #Envia la respuesta
    twilio_functions.enviar_mensaje(state.numero_enviar,state.respuesta_usuario)

@app.post("/recordatorio")
def recordatorio(recordatorio: Recordatorio):
    twilio_functions.enviar_mensaje(recordatorio.numero,recordatorio.mensaje)
