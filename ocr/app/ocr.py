import re
import pytesseract
import cv2
from .config import TESSERACT_CMD, LANG

# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def read_img(img):
    """
    OCR 수행 및 텍스트 반환
    """
    custom_config = f'--oem 3 --psm 3 -l {LANG}'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text

def extract_address_and_date(text):
    """
    OCR 텍스트에서 주소와 날짜를 추출
    """
    # 주소 패턴: "서울특별시 강남구" 또는 "경기도 성남시 분당구" 등
    address_pattern = r'(서울특별시|부산광역시|대구광역시|인천광역시|광주광역시|대전광역시|울산광역시|세종특별자치시|제주특별자치도|경기도|강원도|충청북도|충청남도|전라북도|전라남도|경상북도|경상남도)[\s\S]?(구|군|시)[^\n]'

    # 날짜 패턴: YYYY-MM-DD 또는 YYYY년 MM월 DD일
    date_pattern = r'(\d{4}년\s\d{1,2}월\s\d{1,2}일|\d{4}-\d{1,2}-\d{1,2})'

    # 주소와 날짜 추출
    address_matches = re.findall(address_pattern, text)
    date_matches = re.findall(date_pattern, text)

    # 정제된 주소와 날짜 반환
    address = " ".join([match[0] + match[1] for match in address_matches]) if address_matches else None
    date = date_matches[0] if date_matches else None

    return {"address": address, "date": date}