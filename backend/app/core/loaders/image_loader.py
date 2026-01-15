import os

SUPPORTED_IMAGE_EXT = (".png", ".jpg", ".jpeg")


def load_images(image_dir):
    os.makedirs(image_dir, exist_ok=True)

    images = []
    for file in os.listdir(image_dir):
        if file.lower().endswith(SUPPORTED_IMAGE_EXT):
            images.append({
                "image_path": os.path.join(image_dir, file),
                "type": "image"
            })

    print(f"🖼️ Loaded {len(images)} images")
    return images
