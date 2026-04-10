import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# CORS ko pure tarah open rakho
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
            return jsonify({"error": "Vercel mein API Key nahi mili!"}), 500

        genai.configure(api_key=API_KEY)
        
        # Sabse stable model direct use karo
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Frontend se prompt nahi aaya"}), 400

        # Generation with error handling
        try:
            response = model.generate_content(data.get('prompt'))
            if response and response.text:
                return jsonify({"roadmap": response.text})
            else:
                return jsonify({"error": "Gemini ne khali response diya. Quota check karo."}), 503
        except Exception as ai_err:
            # Agar Gemini busy hai ya quota khatam hai
            return jsonify({"error": f"Gemini Error: {str(ai_err)}"}), 503

    except Exception as e:
        # Ye server crash hone se bachayega
        print(f"System Crash: {str(e)}")
        return jsonify({"error": "Internal Server Crash. Check Vercel Logs."}), 500

app = app
