
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Setup
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

class UserRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "Server is running!", "message": "Backend Live!"}

@app.post("/generate")
async def generate_roadmap(request: UserRequest):
    if not GEMINI_KEY:
        raise HTTPException(status_code=500, detail="API Key missing")
    try:
        # UPDATED MODEL NAME HERE
        model = genai.GenerativeModel('gemini-1.5-flash') 
        response = model.generate_content(f"Provide a clear 4-step roadmap for: {request.prompt}")
        return {"roadmap": response.text}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
