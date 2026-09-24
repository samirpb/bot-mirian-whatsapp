from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT
from gesden import get_horarios, agendar_cita

load_dotenv()
app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "hola" in incoming_msg or "cita" in incoming_msg:
        msg.body("Hola! Soy tu asistente virtual. ¿Qué servicio necesitas y qué día?")
    elif "cancelar" in incoming_msg:
        msg.body("Claro, dime tu nombre y la fecha para cancelar.")
    else:
        # Aquí luego conectamos OpenAI
        msg.body(f"Recibí: {incoming_msg}. {SYSTEM_PROMPT[:50]}...")
    
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)