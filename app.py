from flask import Flask, request, jsonify
import requests
import os
import markdown
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Get your Gemini API Key from environment variables
API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

# Gemini API URL
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"

@app.route('/')
def home():
    return '✅ Chatbot backend is running! Use the /chat endpoint to POST messages.'

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data["message"]

    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [{"parts": [{"text": user_message}]}],
        "generationConfig": {"temperature": 0.7}
    }

    # Make API request to Gemini
    response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()

        # Extract text safely
        bot_reply = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "I'm not sure how to respond to that.")

        # Convert Markdown reply from Gemini to clean HTML
        html_response = markdown.markdown(bot_reply)

        return jsonify({ "response": html_response })

    else:
        return jsonify({
            "error": "Failed to get response from Gemini API",
            "status_code": response.status_code,
            "details": response.text
        }), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
