import streamlit as st
import os
import torch
import open_clip
from PIL import Image
import json

with open("gallery_data.json") as f:
    gallery = json.load(f)

# st.write(gallery[0])

st.set_page_config(page_title="Gallery Copilot", layout="wide")

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


@st.cache_resource
def build_index(folder="dataset"):
    index = []
    for f in os.listdir(folder):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(folder, f)
            index.append({
                "path": path,
                "emb": img_emb(path)
            })
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


st.title("📸 Gallery Copilot")

index = build_index()

query = st.text_input(
    "Ask your gallery",
    placeholder="family photos, sunset, beach, coffee..."
)

if query:
    results = search(query, index)

    st.subheader("Top Matches")

    cols = st.columns(len(results))

    for i, (score, path) in enumerate(results):
        with cols[i]:
            st.image(path, use_container_width=True)
            with open("gallery_data.json") as f:
                gallery = json.load(f)

            photo_info = next(
                x for x in gallery
                if x["path"] == path
            )

            st.caption(f"Score: {score:.3f}")

            st.write("Caption:")
            st.write(photo_info["caption"])

            st.write("Tags:")
            st.write(", ".join(photo_info["tags"]))