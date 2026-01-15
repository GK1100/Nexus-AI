import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import time

MODEL_NAME = "openai/clip-vit-base-patch32"

# Global variables for lazy loading
_clip_model = None
_clip_processor = None

def load_clip_model():
    """Lazy load CLIP model on first use (singleton pattern)"""
    global _clip_model, _clip_processor
    
    if _clip_model is not None and _clip_processor is not None:
        return _clip_model, _clip_processor
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[INFO] Loading CLIP model (attempt {attempt + 1}/{max_retries})...")
            _clip_model = CLIPModel.from_pretrained(MODEL_NAME)
            _clip_processor = CLIPProcessor.from_pretrained(MODEL_NAME)
            print("[INFO] CLIP model loaded successfully!")
            return _clip_model, _clip_processor
        except Exception as e:
            print(f"[ERROR] Failed to load CLIP model (attempt {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"[INFO] Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise Exception(f"Failed to load CLIP model after {max_retries} attempts: {str(e)}")

def embed_image(image_path: str):
    clip_model, clip_processor = load_clip_model()  # Load only when called
    image = Image.open(image_path).convert("RGB")
    inputs = clip_processor(images=image, return_tensors="pt")

    with torch.no_grad():
        features = clip_model.get_image_features(**inputs)

    features = features / features.norm(dim=-1, keepdim=True)
    return features[0].tolist()


def embed_text_clip(text: str):
    clip_model, clip_processor = load_clip_model()  # Load only when called
    inputs = clip_processor(text=[text], return_tensors="pt", padding=True)

    with torch.no_grad():
        features = clip_model.get_text_features(**inputs)

    features = features / features.norm(dim=-1, keepdim=True)
    return features[0].tolist()
