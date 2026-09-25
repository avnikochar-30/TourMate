import pytesseract
import cv2
from translator import translate

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_and_translate(image_path, lang="en"):

    img = cv2.imread(image_path)

    if img is None:
        print("❌ Image not found")
        return ""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.threshold(
        gray, 150, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    text = pytesseract.image_to_string(
        gray,
        lang="eng+tam+mal+hin"
    )

    print("\n📷 RAW OCR TEXT:", repr(text))

    if not text or text.strip() == "":
        return ""

    translated = translate(text, "en")

    return translated