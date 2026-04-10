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

        # ERROR DEBUGGED HERE: model name se 'models/' prefix hata diya hai
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Flowchart aur Mistakes ke liye customized prompt
        refined_prompt = (
            f"Act as a career coach. For a {prompt_text}, provide:\n"
            "1. JOURNEY FLOWCHART: 4 clear steps with '->' arrows.\n"
            "2. 4 CRITICAL MISTAKES TO AVOID.\n"
            "Keep it professional and concise."
        )

        response = model.generate_content(refined_prompt)

        if response.text:
            return jsonify({"roadmap": response.text})
        else:
            return jsonify({"error": "Empty response from AI"}), 500

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
