from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Home route to check if the app is running
@app.route('/')
def home():
    return "Flask is running on Render!"

# Chatbot endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400
    
    user_message = data["message"]

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{"parts": [{"text": user_message}]}],
        "generationConfig": {"temperature": 0.7}
    }

    # Use the correct Gemini API model and key
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"
    API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

    response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", json=payload, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "error": "Failed to get response from Gemini API",
            "status_code": response.status_code,
            "details": response.text
        }), response.status_code

# Ensure it listens on the correct port for Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Render expects an open 0.0.0.0 host
