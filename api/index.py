import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API Key check
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if not API_KEY:
            return jsonify({"error": "API Key Missing"}), 500

        genai.configure(api_key=API_KEY)
        # Yahan 'models/gemini-1.5-flash' use kar rahe hain jo sabse stable hai
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        data = request.get_json()
        prompt = data.get('prompt')
        
        response = model.generate_content(prompt)
        return jsonify({"roadmap": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ye line Vercel ke liye zaroori hai
app = app
