from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import google.generativeai as genai
import io
import os

app = FastAPI()


# ✅ CORS Middleware (add this block)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://educart-marketplace.vercel.app", "http://localhost:3000"],  # Or your frontend URL: ["https://educart.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


genai.configure(api_key="AIzaSyDof_h470pTXw9njYrbsXXoa9s6T5RjU-Q")

@app.get("/")
async def root():
    return {"message": "Welcome to the Gemini OCR API"}

@app.post("/api/ocr")
async def ocr(image: UploadFile = File(...)):
    # Read and open the image
    image_bytes = await image.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Use Gemini Vision model
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([
        "If this image is a valid ID (e.g., government-issued or student ID), extract and return ONLY the full name from it. Disregard the middle name or middle initial—return only the first name (including second given name if present) and last name. If it is not an ID, just return this exact message: 'This is not an ID.'",
        image
    ])

    text_response = response.text.strip()

    if "This is not an ID" in text_response:
        return {"Error": "This is not an ID."}
    else:
        return {"Name": text_response}
