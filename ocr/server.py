import numpy as np
import io
import cv2
import pytesseract
from fastapi import FastAPI, File

def read_img(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(img)
    return text

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI OCR Service is running"}

@app.post("/predict/")
def prediction(file: bytes = File(...)):
    try:
        image_stream = io.BytesIO(file)
        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if frame is None:
            return {"error": "Uploaded file is not a valid image"}

        label = read_img(frame)
        return {"text": label}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}