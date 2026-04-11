import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# CORS setup for zero connection issues
CORS(app, resources={r"/*": {"origins": "*"}})

# Fetching Key
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/')
def home():
    return "PathFind AI Backend is Running!"

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_roadmap():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        if not API_KEY:
            return jsonify({"error": "API Key is missing in Vercel settings"}), 500

        genai.configure(api_key=API_KEY)
        
        # Using 1.5 Pro as it's highly available
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        data = request.get_json()
        user_prompt = data.get('prompt')
        
        if not user_prompt:
            return jsonify({"error": "Prompt is empty"}), 400

        # AI Generation
        response = model.generate_content(user_prompt)
        
        if response and response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "AI returned empty text. Check Quota."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for Vercel
app = app
