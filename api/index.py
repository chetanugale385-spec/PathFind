import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    response = model.generate_content(data.get('prompt'))
    return jsonify({"roadmap": response.text})

app = app
