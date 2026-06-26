import json

with open("gallery_data.json") as f:
    photos = json.load(f)

query = input("Ask: ").lower()

scores = []

for photo in photos:

    score = 0

    tags = photo["tags"]

    if "father" in query:
        if "parents" in tags:
            score += 10
        if "family" in tags:
            score += 5

    if "family" in query:
        if "family" in tags:
            score += 10

    if "travel" in query:
        if "travel" in tags:
            score += 10

    if "selfie" in query:
        if "selfie" in tags:
            score += 10

    scores.append((score, photo))

scores.sort(reverse=True, key=lambda x: x[0])

for score, photo in scores[:5]:
    print()
    print(score)
    print(photo["path"])
    print(photo["caption"])
    print(photo["tags"])