import os
import json
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

captions = []

for file in os.listdir("dataset"):
    if file.lower().endswith((".jpg", ".jpeg", ".png")):

        path = os.path.join("dataset", file)

        image = Image.open(path).convert("RGB")

        inputs = processor(image, return_tensors="pt")

        out = model.generate(
            **inputs,
            max_new_tokens=30
        )

        caption = processor.decode(
            out[0],
            skip_special_tokens=True
        )

        print(f"{file} -> {caption}")

        captions.append({
            "path": path,
            "caption": caption
        })

with open("captions.json", "w") as f:
    json.dump(captions, f, indent=2)

print("\nSaved captions.json")