import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/')
def home():
    return "PathFind Backend is Live!"

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_roadmap():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        if not API_KEY:
            return jsonify({"error": "API Key Missing"}), 500

        genai.configure(api_key=API_KEY)
        
        # --- SAFE MODEL SELECTION ---
        # Hum dono options try karenge: 'gemini-1.5-flash' aur 'models/gemini-1.5-flash'
        model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
        model = None
        
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                # Chhota sa test check
                break 
            except:
                continue

        if not model:
            return jsonify({"error": "No valid Gemini model found"}), 500
        # ----------------------------

        data = request.get_json()
        prompt = data.get('prompt', 'B.Tech roadmap')
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "AI response was empty"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

app = app
