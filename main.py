import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API Key setup
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

@app.route('/')
def home():
    return "PathFind Backend is Live on Vercel!"

@app.route('/generate', methods=['POST'])
def generate_roadmap():
    try:
        data = request.json
        prompt_text = data.get('prompt', 'Career roadmap for B.Tech student')

        # Mobile compatibility ke liye 'gemini-pro' use kar rahe hain
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt_text)

        if response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "Empty AI response"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel ko is line ki zaroorat hoti hai
# if __name__ == "__main__": app.run() hata sakte ho, Vercel handle kar lega.
