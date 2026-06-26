import os
import torch
import open_clip
from PIL import Image

model, preprocess, _ = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)

tokenizer = open_clip.get_tokenizer("ViT-B-32")


def img_emb(path):
    image = preprocess(Image.open(path)).unsqueeze(0)
    with torch.no_grad():
        emb = model.encode_image(image)
    return emb / emb.norm(dim=-1, keepdim=True)


def build_index(folder="dataset"):
    index = []
    for f in os.listdir(folder):
        if f.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(folder, f)
            index.append({
                "path": path,
                "emb": img_emb(path)
            })
            print("indexed:", f)
    return index


def txt_emb(text):
    tokens = tokenizer([text])
    with torch.no_grad():
        emb = model.encode_text(tokens)
    return emb / emb.norm(dim=-1, keepdim=True)


def search(query, index):
    q = txt_emb(query)

    results = []
    for item in index:
        sim = (q @ item["emb"].T).item()
        results.append((sim, item["path"]))

    results.sort(reverse=True, key=lambda x: x[0])
    return results[:5]


if __name__ == "__main__":
    print("Building index...")
    index = build_index()

    print("\nGallery Copilot ready 🚀")

    while True:
        q = input("\nAsk: ")
        results = search(q, index)

        print("\nTop matches:\n")
        for score, path in results:
            print(round(score, 3), path)