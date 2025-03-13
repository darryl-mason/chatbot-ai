from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS  # Import CORS

@app.route('/')
def home():
    return "Flask is running on Render!"
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Get API Key from Environment Variables
API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_GEMINI_API_KEY is not set. Please set it in your environment.")

# Correct API Endpoint with updated model name
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"

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

    response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return jsonify(response_data)  
    else:
        return jsonify({
            "error": "Failed to get response from Gemini API",
            "status_code": response.status_code,
            "details": response.text  
        }), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
