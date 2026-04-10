import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Sabse open CORS policy taaki browser se connection block na ho
CORS(app, resources={r"/*": {"origins": "*"}})

# API Key setup from Vercel Environment Variables
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
            return jsonify({"error": "API Key Missing in Vercel Settings"}), 500

        genai.configure(api_key=API_KEY)
        
        # --- STABLE MODEL SELECTION ---
        # Agar 1.5-flash nahi mil raha, toh 'gemini-pro' har jagah chalta hai
        try:
            model = genai.GenerativeModel('gemini-pro')
        except:
            model = genai.GenerativeModel('models/gemini-pro')
        # ------------------------------

        data = request.get_json()
        prompt = data.get('prompt', 'B.Tech Roadmap')
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "AI response was empty"}), 500

    except Exception as e:
        # Ye error message website par dikhega agar fail hua toh
        return jsonify({"error": str(e)}), 500

app = app
