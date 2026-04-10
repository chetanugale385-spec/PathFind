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
        
        # AUTOMATIC MODEL SELECTION
        # Ye code check karega ki tumhari library ke liye kaunsa model available hai
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Agar flash ya pro milta hai toh wo use karo, warna list ka pehla model
        selected_model = 'models/gemini-1.5-flash'
        if 'models/gemini-1.5-flash' not in available_models:
            if available_models:
                selected_model = available_models[0]
            else:
                return jsonify({"error": "No Gemini models available for this API Key"}), 500

        model = genai.GenerativeModel(selected_model)
        
        data = request.get_json()
        response = model.generate_content(data.get('prompt', 'career roadmap'))
        
        if response and response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "AI response was empty"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
