import twilio_functions

respuesta_usuario="""
¡Genial! Ya tengo todo listo para crear tu plan personalizado de calorías 🎉✨

No hay secretos ni fórmulas mágicas para bajar de peso, solo un principio básico: 

*Comer menos calorías de las que tu cuerpo quema* 🔥

Con toda tu información, te voy a generar exactamente lo que necesitas comer cada día para alcanzar tus metas 💪🍽️

Lo único que tienes que hacer es enviarme fotos de tus comidas, y yo me encargaré de contar las calorías por ti 📸📊. ¡Así de fácil!
"""

twilio_functions.enviar_mensaje("whatsapp:+51927144823",respuesta_usuario)