import json
from PIL import Image
import re
import os

def extract_standings_from_image(image_path):
    """Extract standings from image using OCR"""
    try:
        import pytesseract
        # Set tesseract path for Windows installation
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        
        print(f"\n{'='*80}")
        print(f"Text extracted from {os.path.basename(image_path)}:")
        print('='*80)
        print(text)
        print('='*80)
        
        return text
    except Exception as e:
        print(f"Error reading image: {e}")
        return None

# Try to extract text from both images
print("Attempting to extract standings from images...")

image1_text = extract_standings_from_image('standings/PXL_20260109_025523745.jpg')
image2_text = extract_standings_from_image('standings/PXL_20260109_025537917.jpg')

print("\n" + "="*80)
print("Extraction complete. Review the text above.")
print("="*80)
