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
        "Task: Analyze the image and extract the full name if it is a valid ID (e.g., government-issued ID, student ID). Rules: Return only the full name if an ID is detected, The name must follow this format: Include the full first name (including second given name, if present), Include the last name, f a middle name is present (whether fully spelled or abbreviated), include only its first letter followed by a period (e.g., A.), Do not include the full middle name — always reduce it to its initial, If the image is not an ID, return exactly: This is not an ID.",
        image
    ])

    text_response = response.text.strip()

    if "This is not an ID" in text_response:
        return {"Error": "This is not an ID."}
    else:
        return {"Name": text_response}
