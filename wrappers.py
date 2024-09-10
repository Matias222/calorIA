import db_functions
import pytz

from datetime import datetime

peru_tz=pytz.timezone("America/Lima")


def escribir_actualizar_reportes(numero,calorias_consumidas,json_comidas):

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

    


#escribir_actualizar_reportes("whatsapp:+51927144823",100)   