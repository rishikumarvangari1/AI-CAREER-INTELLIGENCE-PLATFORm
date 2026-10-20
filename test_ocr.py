import io
import os
import fitz
import pytesseract

from PIL import Image, ImageOps, ImageEnhance

tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

pdf_path = r"C:\Users\rishi\OneDrive\rishikumar resume.pdf"

try:
    with fitz.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            print(f"\nProcessing page {page_number}...")

            pix = page.get_pixmap(
                matrix=fitz.Matrix(3, 3),
                alpha=False
            )

            image = Image.open(io.BytesIO(pix.tobytes("png")))
            image = ImageOps.grayscale(image)
            image = ImageEnhance.Contrast(image).enhance(2)

            text = pytesseract.image_to_string(
                image,
                lang="eng",
                config="--psm 3"
            )

            print("\nExtracted text:\n")
            print(text if text.strip() else "OCR returned no text.")

except Exception as error:
    print("OCR ERROR:", type(error).__name__, str(error))