import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

with open("captions.json") as f:
    data = json.load(f)

captions = [x["caption"] for x in data]

caption_embeddings = model.encode(captions)

while True:
    query = input("Ask: ")

    query_embedding = model.encode([query])

    scores = cosine_similarity(
        query_embedding,
        caption_embeddings
    )[0]

    ranked = sorted(
        zip(scores, data),
        reverse=True
    )

    print()

    for score, item in ranked[:5]:
        print(
            round(score, 3),
            item["path"],
            "->",
            item["caption"]
        )

    print()