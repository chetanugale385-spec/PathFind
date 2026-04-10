import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Sabse open CORS policy
CORS(app, resources={r"/*": {"origins": "*"}})

# API Key check
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/')
def home():
    return "PathFind Backend is Live and Secure!"

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_roadmap():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        if not API_KEY:
            return jsonify({"error": "API Key not found in Vercel environment variables"}), 500

        genai.configure(api_key=API_KEY)
        
        # --- AUTOMATIC MODEL DISCOVERY ---
        # Ye logic available models ki list nikalega aur pehla working model select karega
        model_to_use = None
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    # Hum 1.5-flash ko priority denge, agar nahi mila toh koi bhi working model
                    if 'gemini-1.5-flash' in m.name:
                        model_to_use = m.name
                        break
                    if not model_to_use:
                        model_to_use = m.name
        except Exception as e:
            # Agar list_models fail ho (rare), toh manually fallback
            model_to_use = "models/gemini-1.5-flash"

        model = genai.GenerativeModel(model_to_use)
        # ----------------------------------

        data = request.get_json()
        user_prompt = data.get('prompt', 'Professional career roadmap')
        
        response = model.generate_content(user_prompt)
        
        if response and response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "AI response was empty. Please try again."}), 500

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Vercel entry point
app = app
