import torch
from PIL import Image
from transformers import (
    AutoProcessor,
    LlavaOnevisionForConditionalGeneration
)

MODEL_ID = "llava-hf/llava-onevision-qwen2-0.5b-ov-hf"

processor = AutoProcessor.from_pretrained(MODEL_ID)
model = LlavaOnevisionForConditionalGeneration.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32,
    device_map="cpu"
)

def reason_about_image(image_path: str, question: str) -> str:
    image = Image.open(image_path).convert("RGB")

    # 🔴 REQUIRED: image placeholder token
    prompt = (
        "You are an expert assistant.\n"
        "<image>\n"
        f"QUESTION: {question}\n"
        "ANSWER:"
    )

    inputs = processor(
        text=prompt,
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False,
            pad_token_id=processor.tokenizer.eos_token_id
        )

    return processor.decode(output[0], skip_special_tokens=True)
