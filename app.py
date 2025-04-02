from flask import Flask, request, jsonify
import requests
import os
import re
import markdown
from flask_cors import CORS
import json
from datetime import datetime

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
        bot_reply = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "I'm not sure how to respond to that.")

        # ✅ Fix Markdown issues before converting
        bot_reply = re.sub(r"^\s*[\*\-]\s*$", "", bot_reply, flags=re.MULTILINE)  # Remove bullets with no content
        bot_reply = re.sub(r"(\n\s*-|\n\s*\d+\.)", r"\n\n\1", bot_reply)  # Ensure proper list spacing
        bot_reply = re.sub(r"(\n\s*\*\s*\n)", r"\n", bot_reply)  # Remove empty bullet points

        # ✅ Convert Markdown reply to clean HTML
        html_response = markdown.markdown(bot_reply, extensions=["extra"])

        return jsonify({ "response": html_response })

    else:
        return jsonify({
            "error": "Failed to get response from Gemini API",
            "status_code": response.status_code,
            "details": response.text
        }), response.status_code

@app.route("/analytics", methods=["POST"])
def analytics():
    data = request.json

    data['timestamp'] = datetime.utcnow().isoformat()

    log_file = 'analytics_log.json'
    with open(log_file, 'a') as f:
        f.write(json.dumps(data) + '\n')

    return jsonify({'status': 'logged'})

if __name__ == '__main__':
    app.run(debug=True)