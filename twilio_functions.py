from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
numero_twilio = os.getenv('NUMERO')


def enviar_mensaje(numero_enviar,mensaje):

  client = Client(account_sid, auth_token)

  message = client.messages.create(
    from_=numero_twilio,
    to=numero_enviar,
    body=mensaje,
  )

  return message.sid