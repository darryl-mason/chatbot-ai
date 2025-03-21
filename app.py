from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Get API Key
API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

# Gemini API URL
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"

@app.route('/')
def home():
    return '✅ Chatbot backend is running! Use the /chat endpoint to POST messages.'

import markdown  # Make sure this is at the top of your file

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    # Markdown-formatted reply (with **bold**, *bullets*, etc.)
    markdown_text = """
**Paris:**
* Eiffel Tower
* Louvre Museum

**Rome:**
* Colosseum
* Vatican City

Visit [this link](https://example.com) for more info!
"""

    # Convert Markdown to safe HTML
    html_response = markdown.markdown(markdown_text)

    return jsonify({ "response": html_response })
    
    user_message = data["message"]

    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [{"parts": [{"text": user_message}]}], 
        "generationConfig": {"temperature": 0.7}
    }

    # Make API request
    response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()

        # FIX: Ensure we're calling the correct function
        bot_reply = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "I'm not sure how to respond to that.")
        
        formatted_reply = format_bot_response(bot_reply)  # ✅ CORRECT FUNCTION

        return jsonify({"response": formatted_reply})  # ✅ Returns JSON response
    else:
        return jsonify({
            "error": "Failed to get response from Gemini API",
            "status_code": response.status_code,
            "details": response.text  # Log error details
        }), response.status_code

import re

def format_bot_response(response_text):
    """
    Formats the bot's response for better readability.
    - Ensures numbered lists have line breaks.
    - Converts list markers (-) into bullet points (•).
    - Adds new lines after punctuation for better readability.
    """
    if not response_text:
        return "I'm not sure how to respond to that."

    # Ensure line breaks for numbered lists (e.g., "1. " -> "\n1. ")
    formatted_text = re.sub(r"(\d+)\.\s", r"\n\1. ", response_text)

    # Convert "- " into bullet points "• "
    formatted_text = formatted_text.replace("- ", "• ")

    # Add newlines after sentences for better readability
    formatted_text = re.sub(r"([.!?])\s", r"\1\n", formatted_text)

    return formatted_text.strip()

if __name__ == '__main__':
    app.run(debug=True)
