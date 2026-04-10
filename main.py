import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Environment variable setup
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

@app.route('/')
def home():
    return "PathFind Backend is Live!"

@app.route('/generate', methods=['POST'])
def generate_roadmap():
    try:
        data = request.json
        prompt_text = data.get('prompt', 'Career roadmap')

        # Sabse safe model jo har version par chalta hai
        model_name = 'gemini-pro' 
        
        # Try block to handle model selection
        try:
            model = genai.GenerativeModel(model_name)
            # Simple content generation
            response = model.generate_content(prompt_text)
            
            if response.text:
                return jsonify({"roadmap": response.text})
            else:
                return jsonify({"error": "No text returned"}), 500
                
        except Exception as model_err:
            return jsonify({"error": "Model Error", "details": str(model_err)}), 404

    except Exception as e:
        return jsonify({"error": "Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
