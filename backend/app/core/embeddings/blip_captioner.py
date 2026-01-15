from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import time

MODEL_NAME = "Salesforce/blip-image-captioning-base"

# Global variables for lazy loading
_blip_processor = None
_blip_model = None

def load_blip_model():
    """Lazy load BLIP model on first use (singleton pattern)"""
    global _blip_processor, _blip_model
    
    if _blip_processor is not None and _blip_model is not None:
        return _blip_processor, _blip_model
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[INFO] Loading BLIP model (attempt {attempt + 1}/{max_retries})...")
            _blip_processor = BlipProcessor.from_pretrained(MODEL_NAME)
            _blip_model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
            print("[INFO] BLIP model loaded successfully!")
            return _blip_processor, _blip_model
        except Exception as e:
            print(f"[ERROR] Failed to load BLIP model (attempt {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"[INFO] Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise Exception(f"Failed to load BLIP model after {max_retries} attempts: {str(e)}")

def generate_caption(image_path: str) -> str:
    processor, model = load_blip_model()  # Load only when called
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(**inputs, max_length=50)

    return processor.decode(output[0], skip_special_tokens=True)
