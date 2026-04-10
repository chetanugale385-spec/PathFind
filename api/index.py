import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# API Key setup
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/')
def home():
    return "Backend is active!"

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_roadmap():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        if not API_KEY:
            return jsonify({"error": "API Key missing in Vercel settings"}), 500

        genai.configure(api_key=API_KEY)
        
        # --- DYNAMIC MODEL DISCOVERY ---
        # Ye code tumhare account mein available saare models check karega
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            return jsonify({"error": "No generative models found for this API key"}), 500
        
        # Priority list: sabse pehle 1.5-flash try karega, phir pro, phir jo bhi mile
        selected_model = None
        for target in ['1.5-flash', 'gemini-pro', '1.0-pro']:
            for am in available_models:
                if target in am:
                    selected_model = am
                    break
            if selected_model: break
        
        if not selected_model:
            selected_model = available_models[0] # Fallback to first available

        model = genai.GenerativeModel(selected_model)
        # -------------------------------

        data = request.get_json()
        prompt = data.get('prompt', 'Career roadmap for engineering')
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "Model found but response was empty"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

app = app
