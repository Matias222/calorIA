import agents
import db_functions

a=db_functions.upsertar_usuario({"numero":"whatsapp:+51927144823"})

z=agents.plan_personalizado(a)

print(z["Respuesta al usuario"])
print("*"*60)
print(z["Explicacion"])