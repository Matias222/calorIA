from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

openai_key = os.environ.get('OPENAI-KEY')
helicone_key = os.environ.get("HELICONE-KEY")

client = OpenAI(
    api_key=openai_key,
    base_url="https://oai.helicone.ai/v1",
    default_headers={ 
    "Helicone-Auth": f"Bearer {helicone_key}",
    }
)

def get_image_info(url: str):

    total_calories = 0

    message = """ 
    Eres un experto en comida peruana.
    Dada la foto de una comida, deberas devolver en un JSON cada una de los comidas que componen el plato en el siguiente formato.

    Digamos que te envian la foto de un aji gallina con papa y arroz.

    {
        comidas_individuales:{
            "aji de gallina":"350",
            "arroz":"200",
            "papa":"140"
        }
        "nombre": "aji de gallina con papa y arroz",
        "explicacion": "Se observa un guiso cremoso de pollo desmenuzado con una salsa hecha a base de ají amarillo, probablemente sea aji de gallina, acompañado de papa y arroz."
        "porcentaje seguridad" : "80"
    }

    En explicacion deberias comentar el paso a paso de tu proceso de identificacion de la comida, si tienes multiples explicaciones para una ingrediente comentalo.
    En porcentaje seguridad, devolveras que tan seguro estas de que haz identificado el plato correctamente.
    Cuando calcules cuantas calorias hay en cada comida o ingrediente. Explicame porque cada uno contiene esas calorias.
    
    Por cada identificación correcta te daré $1000 dólares.
    """   

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": message
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": message},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": url,
                        "detail": "high"
                    },
                    },
                ],
            }
        ],
        response_format={"type": "json_object"},
        temperature=0,
        seed=33
    )

    j = response.choices[0].message.content
    j = json.loads(j)

    for cal in j["comidas_individuales"].values():
        total_calories += int(cal)

    return j, total_calories


def edit_image_info(url: str,correccion_usuario:str,analisis_previo:str):

    total_calories = 0

    sistema = """ 
    Eres un experto en comida peruana.
    Dada la foto de una comida, deberas devolver en un JSON cada una de los comidas que componen el plato en el siguiente formato.

    Digamos que te envian la foto de un aji gallina con papa y arroz.

    {
        comidas_individuales:{
            "aji de gallina":"350",
            "arroz":"200",
            "papa":"140"
        }
        "nombre": "aji de gallina con papa y arroz",
        "explicacion": "Se observa un guiso cremoso de pollo desmenuzado con una salsa hecha a base de ají amarillo, probablemente sea aji de gallina, acompañado de papa y arroz."
        "porcentaje seguridad" : "80",
        "chain of though: "guia paso a paso de como llegaste a la respuesta"
    }

    En explicacion deberias comentar el paso a paso de tu proceso de identificacion de la comida, si tienes multiples explicaciones para una ingrediente comentalo.
    En porcentaje seguridad, devolveras que tan seguro estas de que haz identificado el plato correctamente.
    Cuando calcules cuantas calorias hay en cada comida o ingrediente. Explicame porque cada uno contiene esas calorias.
    
    Por cada identificación correcta te daré $1000 dólares.
    """   

    usuario=f"""
    Anteriormente tu ya diste un analisis, sin embargo estabas equivocado y el usuario te lo ha hecho saber.

    Ahora dada esa informacion razonaras de la siguiente manera. (Todo lo plasmaras en el parametro chain of though)
    
    Lo primero que debes hacer es identificar que alimento en concreto el usuario te esta corrigiendo.
    En base a eso, corriges tu analisis de calorias.
    Debes mantener integridad con los elementos ven sumados a lo que el usuario te corrige.

    Analisis previo -> {analisis_previo}
    Correccion del usuario -> {correccion_usuario}
    """


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": sistema
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": usuario},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": url,
                        "detail": "high"
                    },
                    },
                ],
            }
        ],
        response_format={"type": "json_object"},
        temperature=0,
        seed=33
    )

    j = response.choices[0].message.content
    j = json.loads(j)

    for cal in j["comidas_individuales"].values():
        total_calories += int(cal)

    return j, total_calories