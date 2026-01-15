import easyocr

# Global variable for lazy loading
_ocr_reader = None

def get_ocr_reader():
    """Lazy load EasyOCR reader on first use (singleton pattern)"""
    global _ocr_reader
    
    if _ocr_reader is not None:
        return _ocr_reader
    
    print("[INFO] Loading EasyOCR reader...")
    _ocr_reader = easyocr.Reader(['en'], gpu=False)
    print("[INFO] EasyOCR reader loaded successfully!")
    return _ocr_reader

def extract_text_from_image(image_path: str) -> str:
    reader = get_ocr_reader()  # Load only when called
    results = reader.readtext(image_path, detail=0)
    text = " ".join(results).strip()
    return text
