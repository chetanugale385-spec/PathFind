import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# CORS ko asaan banate hain taaki koi block na kare
CORS(app, resources={r"/*": {"origins": "*"}})

# API Key setup
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

@app.route('/')
def home():
    return "PathFind Backend is Live!"

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_roadmap():
    # CORS handling for preflight requests
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        data = request.json
        prompt_text = data.get('prompt', 'Provide a career roadmap.')

        # Sabse stable model use karenge
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt_text)

        if response and response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "AI could not generate text"}), 500

    except Exception as e:
        # Ye line logs mein error dikhayegi
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
        
