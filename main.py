from fastapi import FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import google.generativeai as genai
from dotenv import load_dotenv
import os
import base64
import re

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_audio")
async def process_audio(audio: UploadFile = File(...)):
    audio_content = await audio.read()
    audio_base64 = base64.b64encode(audio_content).decode('utf-8')
    
    audio_part = {
        "mime_type": audio.content_type,
        "data": audio_base64
    }
    
    response = model.generate_content([
        "Transcribe the following audio input:",
        audio_part
    ])
    
    transcription = response.text if response.text else "I'm sorry, I couldn't understand the audio input."
    
    # Define more flexible patterns for image and navigation queries
    image_patterns = [
        r"what('s| is)?.*(in front|ahead|before me)",
        r"can I cross.*(road|street)",
        r"what do you see",
        r"describe.*(scene|surroundings)",
        r"identify.*(object|thing)"
    ]
    
    navigation_patterns = [
        r"(where|how).*(nearest|closest)",
        r"(take|bring) me to",
        r"(how can|bring) go to",
        r"(how|way) to (go|get to)",
        r"navigate to",
        r"(find|locate)",
        r"directions? to"
    ]
    
    # Check if the transcription matches any of the patterns
    capture_image = any(re.search(pattern, transcription.lower()) for pattern in image_patterns)
    is_navigation = any(re.search(pattern, transcription.lower()) for pattern in navigation_patterns)
    
    if capture_image:
        return JSONResponse(content={"capture_image": True})
    elif is_navigation:
        response = model.generate_content([
            "Hey whenever i ask anything related to navigation like a place or directionthen only reply1 thing: opening google maps, for _____, in dash put the location that i said. thats it nothing else no emojis symbols etc",
            transcription
        ])
        return JSONResponse(content={"response": response.text, "is_navigation": True})
    else:
        response = model.generate_content([
            "You are an AI assistant. Respond to the following query:",
            transcription
        ])
        return JSONResponse(content={"response": response.text, "capture_image": False, "is_navigation": False})

@app.post("/process_image")
async def process_image(image: UploadFile = File(...)):
    image_content = await image.read()
    image_base64 = base64.b64encode(image_content).decode('utf-8')
    
    image_part = {
        "mime_type": image.content_type,
        "data": image_base64
    }
    
    response = model.generate_content([
        "I am a blind person. What's in front of me? Are there any safety concerns? Please be very concise.",
        image_part
    ])
    
    return JSONResponse(content={"response": response.text})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
