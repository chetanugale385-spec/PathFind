import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Sabse important: Ye line har tarah ki request allow karegi
CORS(app, supports_credentials=True)

# API Key load
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/')
def home():
    return "PathFind Backend is Live and Connected!"

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_roadmap():
    # Pre-flight request handling
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        if not API_KEY:
            return jsonify({"error": "Missing API Key"}), 500

        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "No prompt provided"}), 400

        response = model.generate_content(data.get('prompt'))
        
        if response and response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "AI response was empty"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
