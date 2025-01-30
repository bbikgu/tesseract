from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # 현재 파일의 디렉터리 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.ocr import read_img, extract_address_and_date
from app.utils import preprocess_image

app = FastAPI()

@app.post("/extract-info/")
async def extract_info(file: UploadFile = File()):
    contents = await file.read()

    file_bytes = np.asarray(bytearray(contents), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Failed to process the image"}

    # 이미지 전처리
    processed_img = preprocess_image(img)

    # OCR 수행
    raw_text = read_img(processed_img)

    # 주소와 날짜 추출
    result = extract_address_and_date(raw_text)

    return {"address": result.get("address"), "date": result.get("date")}

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI OCR Service!"}
