from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_PROMPT
from gesden import get_horarios, agendar_cita

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Memoria simple Mirian (en memoria, para no pagar base de datos aún)
conversaciones = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    numero = request.values.get('From', '')
    incoming_msg = request.values.get('Body', '').strip()

    print(f"Mirian recibió de {numero}: {incoming_msg}")

    # Inicializar historial si es primera vez
    if numero not in conversaciones:
        conversaciones[numero] = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Guardar mensaje del usuario
    conversaciones[numero].append({"role": "user", "content": incoming_msg})

    # Lógica rápida para no gastar tokens
    texto_lower = incoming_msg.lower()
    respuesta_final = None

    if "horario" in texto_lower or "disponible" in texto_lower:
        horarios = get_horarios()
        respuesta_final = f"Claro, estos son los horarios disponibles:\n{horarios}\n\n¿Que día te sirve?"

    elif "agendar" in texto_lower or ("cita" in texto_lower and "mañana" in texto_lower):
        resultado = agendar_cita(numero, incoming_msg)
        respuesta_final = f"¡Listo! {resultado}"

    # Si no es horario ni agendar, usamos a OpenAI
    if not respuesta_final:
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversaciones[numero],
                temperature=0.7
            )
            respuesta_final = completion.choices[0].message.content
            conversaciones[numero].append({"role": "assistant", "content": respuesta_final})

        except Exception as e:
            print(f"Error con OpenAI: {e}")
            respuesta_final = "Uy, se me fue la señal un segundito. ¿Me repites porfa?"

    resp = MessagingResponse()
    resp.message(respuesta_final)
    return str(resp)

# Para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
