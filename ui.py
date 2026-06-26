import streamlit as st
import os
import torch
import open_clip
from PIL import Image

st.set_page_config(page_title="Gallery Copilot", layout="wide")

model, preprocess, _ = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)

tokenizer = open_clip.get_tokenizer("ViT-B-32")

def get_reason(score):
    if score > 0.8:
        return "Excellent match for your request"
    elif score > 0.6:
        return "Strong visual match"
    elif score > 0.4:
        return "Reasonably relevant"
    elif score > 0.2:
        return "Somewhat related"
    else:
        return "Weak match"

def img_emb(path):
    image = preprocess(Image.open(path)).unsqueeze(0)
    with torch.no_grad():
        emb = model.encode_image(image)
    return emb / emb.norm(dim=-1, keepdim=True)


@st.cache_resource
def build_index(folder="dataset"):
    index = []
    for f in os.listdir(folder):
        if f.lower().endswith((".jpg", ".png", ".jpeg")):
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

mode = st.selectbox(
    "Mode",
    ["General", "LinkedIn Photo", "Travel Memory", "Family Moments"]
)

def search(query, index):
    q = txt_emb(query)

    results = []

    for item in index:
        sim = (q @ item["emb"].T).item()

        results.append({
            "score": sim,
            "path": item["path"]
        })

    # normalize scores
    scores = [r["score"] for r in results]
    mx = max(scores)
    mn = min(scores)

    for r in results:
        r["score"] = (r["score"] - mn) / (mx - mn + 1e-6)

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:5]


st.title("📸 Gallery Copilot")

index = build_index()

query = st.text_input("Ask your gallery:")

if mode == "LinkedIn Photo":
    query = "professional headshot portrait person facing camera business profile photo"

elif mode == "Travel Memory":
    query = "travel landmark vacation outdoors scenic"

elif mode == "Family Moments":
    query = "family people smiling candid group photo emotional"

if query:
    results = search(query, index)

    st.subheader("Top Matches")

    cols = st.columns(5)

    for i, result in enumerate(results):
        with cols[i]:
            st.image(result["path"], use_container_width=True)
            st.caption(f"Score: {result['score']:.2f}")
            st.caption(get_reason(result["score"]))