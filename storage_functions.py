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

def crear_bucket():
    pass