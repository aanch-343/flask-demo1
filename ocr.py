# ocr.py
from PIL import Image
import io
import pytesseract

def process_image(image_data):
    try:
        # Convert base64 encoded image data to PIL Image object
        image = Image.open(io.BytesIO(image_data))

        # Preprocessing:
        gray = image.convert('L')  # Convert to grayscale
        thresh = gray.point(lambda x: 0 if x < 128 else 255, '1')  # Thresholding

        # Perform OCR on the preprocessed image
        text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')

        return text
    except Exception as e:
        print("Error processing image:", str(e))
        return ""
