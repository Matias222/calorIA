import supabase
import os
import pytz
import requests

from dotenv import load_dotenv
from datetime import datetime

peru_tz=pytz.timezone("America/Lima")


load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")


cliente = supabase.create_client(url, key)

def crear_bucket(name):

    res = cliente.storage.create_bucket(name)

    print(res)

def subir_imagen(name,link,id_imagen):

    imagen=requests.get(link)

    cliente.storage.from_(name).upload(file=imagen.content, path=f"/{id_imagen}.jpg",file_options={"content-type": "image/jpeg"})

def link_publico(name,imagen):
    res = cliente.storage.from_(name).create_signed_url(f"/{imagen}.jpg",60)

    return res["signedURL"]


#def subir_imagen(name):
#crear_bucket("matias")
#subir_imagen("matias","https://api.twilio.com/2010-04-01/Accounts/ACbc907395ab6024e769e826dfe74b3fe5/Messages/MM0473fd27332aabf420e7e165c25a32b7/Media/ME8c054bd4c9cfc97318cf8e58f3746944")
