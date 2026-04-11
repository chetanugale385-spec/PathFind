import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# 1. API KEY CHECK
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if not API_KEY:
            return jsonify({"error": "API Key Missing"}), 500
        
        genai.configure(api_key=API_KEY)
        
        # 2. MODEL NAME FIX (Use this specific one)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        data = request.get_json()
        prompt = data.get('prompt')
        
        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "Empty Response"}), 500
            
    except Exception as e:
        # Ye line logs mein error dikhayegi
        print(f"CRASH ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

# For Vercel
app = app
