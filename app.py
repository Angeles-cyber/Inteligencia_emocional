from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import os
import google.generativeai as genai

# 💡 Cargamos las variables de entorno
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print("🔐 API KEY cargada:", api_key)

# 🤖 Configuramos el modelo de Gemini con nuestra API Key
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# 🌐 Creamos la app de Flask
app = Flask(__name__)

# 🧠 Historial de la conversación (inicio con un mensaje guía)
chat_history = [
    {
        "role": "user",
        "parts": [
            "Eres un psicólogo empático. Escucha con atención, responde con amabilidad, validando emociones y ofreciendo apoyo emocional, no consejos médicos."
        ]
    }
]

@app.route("/")
def index():
    # 🏠 Mostramos la interfaz principal (chat.html)
    return send_from_directory('.', 'chat.html')

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history
    data = request.get_json()
    prompt = data.get("message", "")

    try:
        # 📩 Añadimos el mensaje del usuario al historial
        chat_history.append({"role": "user", "parts": [prompt]})

        # 🧑‍⚕️ Iniciamos una sesión de chat con historial
        chat_session = model.start_chat(history=chat_history)

        # ✉️ Enviamos el mensaje al modelo
        response = chat_session.send_message(prompt)
        reply = response.text

        # 🗣️ Guardamos la respuesta del modelo
        chat_history.append({"role": "model", "parts": [reply]})

        # ✅ Devolvemos la respuesta al frontend
        return jsonify({"reply": reply})
    except Exception as e:
        import traceback
        traceback.print_exc()
        # ⚠️ En caso de error, enviamos una respuesta amigable
        return jsonify({"reply": f"❌ Ups... algo salió mal: {str(e)}"}), 500

# 🚀 Ejecutamos la app en modo debug
if __name__ == "__main__":
    app.run(debug=True)
