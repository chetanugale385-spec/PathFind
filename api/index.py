import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Vercel Environment Variable madhun key ghene
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if not API_KEY:
            return jsonify({"error": "Backend Config Error: API Key Missing"}), 500
        
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        data = request.get_json()
        prompt_text = data.get('prompt', 'Create a general engineering roadmap')
        
        # AI कडून प्रतिसाद मिळवणे
        response = model.generate_content(prompt_text)
        
        if response and response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "AI response was empty"}), 500
            
    except Exception as e:
        print(f"Error: {str(e)}") # He Vercel logs madhe disel
        return jsonify({"error": "AI Connection Timeout. Please try again."}), 500

app = app
