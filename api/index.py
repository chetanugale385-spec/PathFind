import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes and origins to prevent "Connection Failed" errors
CORS(app, resources={r"/*": {"origins": "*"}})

# Load API Key from Vercel Environment Variables
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/')
def health_check():
    return "PathFind AI Backend is Operational!"

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_roadmap():
    # Handle the browser's pre-flight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        # 1. Check if API Key exists
        if not API_KEY:
            return jsonify({"error": "System Configuration Error: API Key Missing"}), 500

        # 2. Configure Gemini
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 3. Get data from Frontend
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Invalid Request: No prompt received"}), 400

        user_prompt = data.get('prompt')

        # 4. Attempt to generate content with a safety block
        try:
            response = model.generate_content(user_prompt)
            
            if response and response.text:
                return jsonify({"roadmap": response.text})
            else:
                return jsonify({"error": "Gemini returned an empty response. Please retry."}), 503
                
        except Exception as ai_err:
            # Handle Quota (429) or Service Busy errors
            error_msg = str(ai_err)
            if "429" in error_msg:
                return jsonify({"error": "AI Quota Exceeded. Please wait 1 minute."}), 429
            return jsonify({"error": f"AI Engine Error: {error_msg}"}), 503

    except Exception as e:
        # General catch-all to prevent server 500 crashes
        return jsonify({"error": f"Server Crash: {str(e)}"}), 500

# Required for Vercel deployment
app = app
