
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI()

# 1. CORS Configuration (Sabse Important)
# Isse aapka GitHub website Render se bina kisi error ke baat kar payega
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Saari websites ko allow karta hai
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST sab allow hai
    allow_headers=["*"],
)

# 2. Gemini API Setup
# Environment variable se key uthayega (Security First!)
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_KEY:
    print("WARNING: GEMINI_API_KEY environment variable nahi mila!")
else:
    genai.configure(api_key=GEMINI_KEY)

# Data model for incoming requests
class UserRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "Server is running!", "message": "Chetan, your backend is live!"}

@app.post("/generate")
async def generate_roadmap(request: UserRequest):
    if not GEMINI_KEY:
        raise HTTPException(status_code=500, detail="API Key not configured on server.")

    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Professional prompt for
