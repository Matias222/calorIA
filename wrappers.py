import db_functions
import storage_functions
import pytz

from datetime import datetime

peru_tz=pytz.timezone("America/Lima")


def escribir_actualizar_reportes(numero,calorias_consumidas,json_comidas,imagen_url):

    print(json_comidas)

    peru_time = datetime.now(peru_tz)
    formatted_date = peru_time.strftime("%m/%d/%Y")    
    
    temp_dic={"usuario":numero,"dia":formatted_date}

    reporte_dic=db_functions.leer_reportes(temp_dic)

    if(reporte_dic==[]): reporte_dic=db_functions.upsertar_reportes(temp_dic)

    total_calorias_consumidas=reporte_dic["calorias"]+calorias_consumidas

    temp_dic={"id":reporte_dic["id"],"calorias":total_calorias_consumidas}

    reporte_dic=db_functions.upsertar_reportes(temp_dic)

    #Ahora falta registrar las comidas

    comidas_dic=db_functions.upsertar_comidas({"reporte":reporte_dic["id"],"comida":json_comidas["nombre"],"calorias":calorias_consumidas})

    for i in json_comidas["comidas_individuales"]:
        db_functions.upsertar_detallado({"comida":comidas_dic["id"],"alimento":i,"calorias":int(json_comidas["comidas_individuales"][i])})

    #Ahora falta subir la imagen al s3, con ese muere el flujo de reporte

    storage_functions.subir_imagen(numero,imagen_url,comidas_dic["id"])


def equivocacion_correccion(nuevo_comida,ultima_comida,total_calorias_antes,calorias_nuevas):

    print("Ultima comida ->",ultima_comida)
    print()
    print("Nueva comida",nuevo_comida)

    peru_time = datetime.now(peru_tz)
    formatted_date = peru_time.strftime("%m/%d/%Y")    

    db_functions.delete_row("detallado","comida",ultima_comida["id"])

    total_calorias_despues=total_calorias_antes-ultima_comida["calorias"]+calorias_nuevas

    db_functions.upsertar_reportes({"id":ultima_comida["reporte"],"dia":formatted_date,"calorias":total_calorias_despues})

    db_functions.upsertar_comidas({"id":ultima_comida["id"],"reporte":ultima_comida["reporte"],"calorias":calorias_nuevas,"comida":nuevo_comida["nombre"]})

    for i in nuevo_comida["comidas_individuales"]:
        db_functions.upsertar_detallado({"comida":ultima_comida["id"],"alimento":i,"calorias":int(nuevo_comida["comidas_individuales"][i])})

def escribir_actualizar_reportes_simplificado(numero,json_comidas):

    print(json_comidas)

    peru_time = datetime.now(peru_tz)
    formatted_date = peru_time.strftime("%m/%d/%Y")    
    
    temp_dic={"usuario":numero,"dia":formatted_date}

    reporte_dic=db_functions.leer_reportes(temp_dic)

    if(reporte_dic==[]): reporte_dic=db_functions.upsertar_reportes(temp_dic)

    print("LLEGUE ACA")

    total_calorias_consumidas=reporte_dic["calorias"]+json_comidas["calorias"]

    temp_dic={"id":reporte_dic["id"],"calorias":int(total_calorias_consumidas)}

    reporte_dic=db_functions.upsertar_reportes(temp_dic)

    #Ahora falta registrar las comidas

    print("POR UPSERTAR ->",{"reporte":reporte_dic["id"],"comida":json_comidas["nombre"],"calorias":json_comidas["calorias"]})

    comidas_dic=db_functions.upsertar_comidas({"reporte":reporte_dic["id"],"comida":json_comidas["nombre"],"calorias":json_comidas["calorias"]})

    db_functions.upsertar_detallado({"comida":comidas_dic["id"],"alimento":json_comidas["nombre"],"calorias":json_comidas["calorias"]})


#escribir_actualizar_reportes("whatsapp:+51927144823",100)   