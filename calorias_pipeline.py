from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

openai_key = os.environ.get('OPENAI-KEY')

client = OpenAI(api_key=openai_key)

def get_image_info(url: str):

    total_calories = 0
    message = """ 
    Eres un experto de comida peruana.
    Dime cada una de las comidas que ves en la imagen y sus respectivas calorías en un JSON con el formato:
    {
        comidas_individuales:{
            "arroz":"100",
            "crema de aji amarillo":"200",
            ....
        }
        "nombre": "aji de gallina con papa a la huancaina y arroz",
        "explicacion": "Se observa un guiso cremoso de pollo desmenuzado con una salsa hecha a base de ají amarillo, leche, pan o galletas molidas, y especias.
        También veo rodajas de papa cocida cubiertas con una salsa cremosa de ají amarillo, queso fresco, leche, y galletas o pan."
    }

    Cuando calcules cuantas calorias hay en cada comida o ingrediente. Explicame porque cada uno contiene esas calorias.
    Por cada explicación correcta te daré $100 dólares.
    """   

    response = client.chat.completions.create(
        model="gpt-4o-mini",
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