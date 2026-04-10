import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Sabhi origins ko allow karna presentation ke liye safe hai
CORS(app)

# Render ke Environment Variables se key uthana
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

@app.route('/')
def home():
    return "PathFind Backend is Live and Running!"

@app.route('/generate', methods=['POST'])
def generate_roadmap():
    try:
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({"error": "No prompt provided"}), 400

        user_input = data.get('prompt')

        # Model initialization
        model = genai.GenerativeModel('gemini-1.5-flash')

        # AI ko specific instruction dena Flowchart aur Mistakes ke liye
        system_instruction = (
            f"Generate a professional career roadmap for {user_input}. "
            "The response MUST have two clear sections:\n"
            "1. FLOWCHART: A 4-step logical journey (Step 1 -> Step 2 -> etc.)\n"
            "2. MISTAKES TO AVOID: 4 critical mistakes for this specific field.\n"
            "Use clear bullet points and professional tone."
        )

        response = model.generate_content(system_instruction)

        if response and response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "AI could not generate a response"}), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    # Render automatically sets the PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
