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

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400
    
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

import re  # 🚨 Import Regular Expressions at the Top

def format_bot_response(response_text):
    """
    Formats the bot's response for better readability.
    - Adds proper line breaks between numbered lists.
    - Ensures bold headings have spacing before them.
    - Converts list markers (-) into bullet points (•).
    - Forces new lines after punctuation to improve readability.
    """
    if not response_text:
        return "I'm not sure how to respond to that."

    # ✅ Ensure line breaks for numbered lists (e.g., "**1. Some text" → "\n\n1. **Some text**")
    formatted_text = re.sub(r"(?<!\n)\*\*(\d+)\. ", r"\n\n\1. **", response_text)

    # ✅ Ensure line breaks before bold headings (without excessive spacing)
    formatted_text = re.sub(r"(?<!\n)\*\*(.*?)\*\*", r"\n\n**\1**", formatted_text)

    # ✅ Convert "- " list markers into bullet points (only at start of lines)
    formatted_text = re.sub(r"(?m)^\- ", "• ", formatted_text)

    # ✅ Add newlines after full stops, question marks, and exclamation points for readability
    formatted_text = re.sub(r"([.!?])\s+", r"\1\n", formatted_text)

    return formatted_text.strip()

if __name__ == '__main__':
    app.run(debug=True)
