import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Environment variable se key lena
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

        # Pehle 'gemini-1.5-flash' try karega, agar nahi mila toh 'gemini-pro'
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt_text)
        except:
            # Ye backup model hai jo 100% har key par chalta hai
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt_text)

        if response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "AI response is empty"}), 500

    except Exception as e:
        return jsonify({"error": "Model Error", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
