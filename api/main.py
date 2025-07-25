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
    allow_origins=["https://educart-marketplace.vercel.app/register"],  # Or your frontend URL: ["https://educart.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key="AIzaSyC3Bdoy3DIDhWES760c0pm6lKm-0rHZIng")

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
        "Extract the full name from this image and just return the name",
        image
    ])

    return {"Name": response.text}
