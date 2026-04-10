import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Sabse open CORS policy taaki browser error na de
CORS(app, resources={r"/*": {"origins": "*"}})

# API Key setup from Vercel Environment Variables
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/')
def home():
    return "PathFind Backend is Live and Connected!"

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_roadmap():
    # CORS handling for pre-flight requests
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        if not API_KEY:
            return jsonify({"error": "API Key not found in Vercel settings"}), 500

        # AI Configuration
        genai.configure(api_key=API_KEY)
        
        # UPDATED MODEL NAME: Using 1.5-flash for speed and compatibility
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "No prompt provided"}), 400

        # AI Generation
        response = model.generate_content(data.get('prompt'))
        
        if response and response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "AI response was empty"}), 500

    except Exception as e:
        # Error logging for Vercel
        print(f"Server Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Vercel needs the 'app' object to run
