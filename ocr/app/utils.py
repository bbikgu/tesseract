import cv2
def preprocess_image(img):
    """
    OCR 인식률을 높이기 위한 이미지 전처리
    """
    # Grayscale 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 이진화 (Thresholding)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 이미지 크기 조정 (OCR 가독성 향상)
    resized = cv2.resize(binary, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

    # 노이즈 제거
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    clean = cv2.morphologyEx(resized, cv2.MORPH_CLOSE, kernel)

    return clean