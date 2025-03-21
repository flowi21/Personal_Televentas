from flask import Flask, request, jsonify
import requests
import openai
import os

app = Flask(__name__)

# Configuración
BITRIX24_WEBHOOK = "https://personal.bitrix24.es/rest/40/oy1texfcn8pxcses/"  # 🔹 Reemplazar con tu webhook de Bitrix24
OPENAI_API_KEY = "proj_wCWFSkDmDXxA8PeQtVvb93JN"  # 🔹 Reemplazar con tu API Key de OpenAI

openai.api_key = OPENAI_API_KEY

# Endpoint para recibir mensajes de Bitrix24
@app.route("/webhook", methods=["POST"])
def bitrix_webhook():
    data = request.json
    
    if not data or "data" not in data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    # Extraer mensaje y usuario
    message = data["data"].get("TEXT", "")
    chat_id = data["data"].get("DIALOG_ID", "")

    if not message or not chat_id:
        return jsonify({"error": "Faltan datos"}), 400

    # Enviar mensaje a OpenAI
    ai_response = get_ai_response(message)

    # Enviar la respuesta de vuelta a Bitrix24
    send_message_to_bitrix(chat_id, ai_response)

    return jsonify({"status": "ok"}), 200

# Función para obtener respuesta de OpenAI
def get_ai_response(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-4",  
        messages=[{"role": "user", "content": user_message}]
    )
    return response["choices"][0]["message"]["content"].strip()

# Función para enviar mensaje a Bitrix24
def send_message_to_bitrix(chat_id, message):
    url = f"{BITRIX24_WEBHOOK}/im.message.add"
    payload = {
        "DIALOG_ID": chat_id,
        "MESSAGE": message
    }
    requests.post(url, json=payload)

# Ejecutar servidor en Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



