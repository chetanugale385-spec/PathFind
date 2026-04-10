
import os
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS settings taaki GitHub website se request aa sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 PRIVACY SECURED: Ye line system se key uthayegi, code me nahi dikhegi
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.post("/generate")
async def generate(data: dict):
    user_input = data.get("prompt", "B.Tech AIML roadmap")
    response = model.generate_content(f"Generate a short 4-step roadmap for: {user_input}")
    return {"roadmap": response.text}
