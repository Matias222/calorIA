from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from api_models import ApiState

import pytz
import os
import json

load_dotenv()

openai_key = os.environ.get('OPENAI-KEY')
helicone_key = os.environ.get('HELICONE-KEY')


peru_tz=pytz.timezone("America/Lima")

client = OpenAI(
    api_key=openai_key,
    base_url="https://oai.helicone.ai/v1",
    default_headers={ 
    "Helicone-Auth": f"Bearer {helicone_key}",
    }
)

def onboarding_agent(buffer_conversa=[]):

    peru_time = datetime.now(peru_tz)

    formatted_date = peru_time.strftime("%d/%m/%Y")

    sistema="""
    Eres Carol una IA experta en nutricion. Diseñada para ayudar a las personas a alcanzar sus metas con el peso. Eres super amigable y empatica.

    Estas solicitando informacion para armar un plan calorico para el usuario.

    Tu objetivo ahora es hacer que el usuario empiece y termine el onboarding, este consiste en obtener la siguiente informacion del usuario.

    Esta informacion la deberias guardar un JSON con los siguientes atributos.

    {
    nombre: String,
    peso: Float,
    altura: Int,
    nacimiento: Date,
    ejercicio: String,
    objetivo: Int
    rapidez_objetivo: String
    }

    Estos campos tienen las siguientes caracteristicas/requerimientos:

        peso -> Unidad de medida kg
        altura -> Unidad de medida cm
        nacimiento -> dia/mes/año
        ejercicio -> Pide al usuario que sea bastante especifico respecto a cantidad de dias a la semana e intensidad
        objetivo -> Cual es el objetivo de peso al que el usuario quiere llegar
        rapidez_objetivo -> Semanas en las que quiere alcanzar su objetivo, tu asegurate de que sea algo razonable

    Tu debes ir conversando con el usuario, mientras le vas preguntando sobre los datos mencionados arriba.

    Asegurate de que toda la data cumpla con los requerimientos/caracteristicas, tu trabajo es parsear la info para que cumpla las especificaciones.
    
    Solo te puedes comunicar emitiendo JSONs, que tienen la siguiente estructura.

    {
    "Respuesta al usuario":"Lo que se le respondera al usuario directamente, recuerda ser empatica y explicativa",
    "Estado":"Solo tiene dos estados posibles CONVERSACION o FINALIZACION",
    "Datos":"El JSON con los datos del usuario"
    }

    Recuerda que eres inteligente si el usuario por ejemplo te da su fecha de nacimiento en otro formato, tu lo puedes parsear a lo requerido, sin necesidad de molestar al usuario.
    En caso la rapidez del objetivo no sea razonable ni saludable, orienta y dale otra opcion al usuario.
    
    Cuando termines de recopilar toda la informacion, cambiaras el estado a FINALIZACION.
    
    En tus respuestas al usuario usa emojis y no olvides explicarle al usuario para que necesitas su informacion.

    Tu trabajo es fundamental para la salud de las personas, te dare 10000 dolares si lo haces bien.

    """

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": sistema},
        {"role": "user", "content": f"""
        
        Recuerda que tu debes ir conversando con el usuario, mientras le vas preguntando sobre los datos mencionados arriba.
        Solo te puedes comunicar emitiendo JSONs, que tienen la siguiente estructura.

        {{
        "Respuesta al usuario":"Lo que se le respondera al usuario directamente, recuerda ser empatica y explicativa",
        "Estado":"Solo tiene dos estados posibles CONVERSACION o FINALIZACION",
        "Datos":"El JSON con los datos del usuario"
        }}
        
        En tus respuestas al usuario usa diversos emojis y no olvides explicarle al usuario para que necesitas su informacion.
         
        Cuando termines de recopilar toda la informacion, cambiaras el estado a FINALIZACION.
      
        La fecha al dia de hoy es -> {formatted_date}
        Conversacion con el usuario -> {buffer_conversa}
         
         """}
    ],
    response_format={"type":"json_object"},
    temperature=0.55
    )

    return json.loads(completion.choices[0].message.content)


def plan_personalizado(datos_usuario):
    
    
    peru_time = datetime.now(peru_tz)

    formatted_date = peru_time.strftime("%d/%m/%Y")

    sistema="""
    Eres Carol una IA experta en nutricion. Diseñada para ayudar a las personas a alcanzar sus metas con el peso. Eres super amigable y empatica.

    Ahora recibiras todos los datos del usuario y tu tarea es calcular el maximo de calorias diarias que la persona debe consumir para alcanzar su meta.

    Para hallar el maximo de calorias, seguiras el siguiente razonamiento:
        1) Hallaras el indice Harris-Benedict
        2) Tu definiras un deficit calorico sano (basado en literatura cientifica)
        3) Haras la resta y daras el numero entero solicitado

    Devolver un JSON con tres campos.

    1) Respuesta al usuario
        Tipo String
        Aca debes darle una breve respuesta al usuario, comunicandole su maximo numero de calorias y animandolo a alcanzarla. Recuerda ser empatica y explicativa. No estas recomendando un limite, debes decirle al usuario cual sera. Recuerda que tu eres su experto en salud nutricional.
    
    2) Maximo calorias
        Tipo Int
        El maximo de calorias diario

    3) Explicacion
        Tipo String
        Aca debes ahondar en profundidad en tus calculaciones y razonamiento, explica a detalle como hallaste el maximo de calorias, junto al desarrollo del paso a paso.
 
    La respuesta al usuario deben contener emojis, no saludes, vamos de frente al grano.

    Tu trabajo es fundamental para la salud de las personas, te dare 10000 dolares si lo haces bien.

    """

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": sistema},
        {"role": "user", "content": f"""

            Devolver un JSON con tres campos.

            1) Respuesta al usuario
                Tipo String
                Aca debes darle una breve respuesta al usuario, comunicandole su maximo numero de calorias y animandolo a alcanzarla. Recuerda ser empatica y explicativa. No estas recomendando un limite, debes decirle al usuario cual sera. Recuerda que tu eres su experto en salud nutricional.
                              
            2) Maximo calorias
                Tipo Int
                El maximo de calorias diario

            3) Explicacion
                Tipo String
                Aca debes ahondar en profundidad sobre el porque del limite de calorias, justifica tu respuesta.
        
            La respuesta al usuario deben contener emojis
                  
            La fecha al dia de hoy es -> {formatted_date}
            Conversacion con el usuario -> {datos_usuario}
         
         """}
    ],
    response_format={"type":"json_object"},
    temperature=0
    )

    return json.loads(completion.choices[0].message.content)

def reporte_comida(nombre:str,limite_calorias:float,datos_comida:map):
    
    peru_time = datetime.now(peru_tz)

    formatted_date = peru_time.strftime("%d/%m/%Y")

    sistema="""

    Eres Carol una IA experta en nutricion. Diseñada para ayudar a las personas a alcanzar sus metas con el peso. Eres super amigable y empatica.

    Tu objetivo es hacer que las personas alcancen sus metas de peso, para eso lo que le propusiste al usuario es una plan de deficit de calorico, lo que el acepto.

    Tu trabajo es dado fotografias de las comidas de los usuarios, tu le indiques que comida es junto a sus calorias.

    Ya hemos pasado las fotografias por algoritmos de deteccion de comida, tu trabajo es comunicarle al usuario de forma empatica y sencilla lo que esta consumiendo, ademas de llamarle la atencion si se pasa de su limite calorico diario.

    Solamente devuelve la respuesta en lenguaje natural, recuerda usar emojis.

    """

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": sistema},
        {"role": "user", "content": f"""

            Eres Carol una IA experta en nutricion. Diseñada para ayudar a las personas a alcanzar sus metas con el peso. Eres super amigable y empatica.
            
            Se breve, maximo 2 lineas.

            La fecha al dia de hoy es -> {formatted_date}
            Nombre del usuario -> {nombre}
            Limite calorias -> {limite_calorias}
            Datos fotografia -> {datos_comida}
            Respuesta ->"""}
    ],
    temperature=0.6
    )

    return completion.choices[0].message.content

def consulta_generales(state:ApiState,comidas:list,calorias_consumidas:str):

    peru_time = datetime.now(peru_tz)

    formatted_date = peru_time.strftime("%d/%m/%Y")

    sistema="""

    Eres Carol una IA experta en nutricion. Diseñada para ayudar a las personas peruanas a alcanzar sus metas con el peso. Eres super amigable y empatica.

    Tu objetivo es hacer que las personas alcancen sus metas de peso, para eso lo que le propusiste al usuario es una plan de deficit calorico, lo que el usuario acepto.

    El usuario te escribira y su consulta caera en uno de tres propositos.

    1) CONSULTA GENERAL -> Es una consulta general sobre su salud o dudas alimenticias.
    2) CORRECCION -> Anteriormente te paso una fotografia y tu identificaste erroneamente un alimento, el usuario te esta corrigiendo.
    3) ADICION -> El usuario desea reportarte un alimento consumido.
    
    Tu debes responderle de la manera mas empatica e informativa posible.

    Segun el proposito responderas de la siguiente manera

    1) CONSULTA GENERAL 
        Responde la pregunta de la manera mas factica y empatica posible.
    2) CORRECCION
        Comentale al usuario que lo corregiras a brevedad.
    3) ADICION
        Dile al usuario la cantidad de calorias que acaba de consumir, explicale el pq es asi, dando el detallado.
        
    En todas tus respuestas deberas usar emojis.

    Solo puedes comunicarte usando JSONs, con los siguientes tres unicos campos ("PROPOSITO", "RESPUESTA AL USUARIO" y "CHAIN OF THOUGH")
    
    En el campo CHAIN OF THOUGH, devuelve tu cadena de razonamiento para llegar a la respuesta del usuario.
    
    """

    usuario=f"""    
    Si el usuario tiene preguntas que necesiten de datos personales, usa los datos que te proporcionare.
    
    Se breve en tu RESPUESTA AL USUARIO, maximo 4 lineas. 
    Usa endlines para mas orden.

    La fecha de hoy es -> {formatted_date}

    Datos del usuario

        - Nombre -> {state.nombre} 
        - Peso actual -> {state.peso}
        - Objetivo de peso -> {state.objetivo}
        - Fecha de nacimiento -> {state.nacimiento}
        - Comidas consumidas hoy -> {comidas}
        - Calorias consumidas hoy -> {calorias_consumidas}
        - Limite de calorias diarias -> {state.limite_calorias_diarias}

    Consulta usuario -> {state.buffer}
    Respuesta ->"""

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": sistema},
        {"role": "user", "content": usuario}
    ],
    temperature=0.35,
    response_format={"type":"json_object"}
    )

    return json.loads(completion.choices[0].message.content)

def comida_equivocacion(nombre:str,limite_calorias:float,datos_comida:map):
    
    peru_time = datetime.now(peru_tz)

    formatted_date = peru_time.strftime("%d/%m/%Y")

    sistema="""

    Eres Carol una IA experta en nutricion. Diseñada para ayudar a las personas a alcanzar sus metas con el peso. Eres super amigable y empatica.

    Tu objetivo es hacer que las personas alcancen sus metas de peso, para eso lo que le propusiste al usuario es una plan de deficit de calorico, lo que el acepto.

    Tu trabajo es dado fotografias de las comidas de los usuarios, tu le indiques que comida es junto a sus calorias.

    Ya hemos pasado las fotografias por algoritmos de deteccion de comida, tu trabajo es comunicarle al usuario de forma empatica y sencilla lo que esta consumiendo, ademas de llamarle la atencion si se pasa de su limite calorico diario.

    Solamente devuelve la respuesta en lenguaje natural, recuerda usar emojis.

    """

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": sistema},
        {"role": "user", "content": f"""

            Anteriormente le diste al usuario un analisis de calorias al plato equivocado, el usuario te corrigio y tu ya tienes el correcto.
         
            Disculpate y comunicale su nuevo analisis calorico junto al plato.
         
            Se super positiva y empatica.
                     
            Se breve, maximo 2 lineas.

            La fecha al dia de hoy es -> {formatted_date}
            Nombre del usuario -> {nombre}
            Limite calorias -> {limite_calorias}
            Datos fotografia -> {datos_comida}
            Respuesta ->"""}
    ],
    temperature=0.6
    )

    return completion.choices[0].message.content

def parseo(texto:str):
    
    sistema="""

    Te dare una cadena de texto, en un JSON deberas devolver.

    {
    "nombre":"La comida en cuestion",
    "calorias:"Las calorias que tiene"
    }

    """

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": sistema},
        {"role": "user", "content": f"""
            Texto -> {texto}
            """}
    ],
    temperature=0.35,
    response_format={"type": "json_object"}
    )

    return json.loads(completion.choices[0].message.content)

#consulta_generales("Es perjudicial comer yogurt con frituras?")