import openai
from flask import Flask, request, jsonify

# Inicia Flask
app = Flask(__name__)

# Coloca aquí tu API Key de OpenAI
openai.api_key = 'proj_wCWFSkDmDXxA8PeQtVvb93JN'

# Definir el comportamiento del bot
@app.route('/', methods=['POST'])
def webhook():
    # Obtener datos del mensaje desde Bitrix24
    data = request.json
    mensaje_cliente = data.get('data', {}).get('PARAMS', {}).get('MESSAGE', '')
    
    # Realizar consulta a OpenAI para generar respuesta
    response = openai.Completion.create(
        engine="text-davinci-003",  # Puedes elegir el modelo de OpenAI que prefieras
        prompt=mensaje_cliente,
        max_tokens=150,
        temperature=0.7
    )
    
    # Responder con el texto generado por OpenAI
    respuesta = response.choices[0].text.strip()
    
    return jsonify({"MESSAGE": respuesta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
