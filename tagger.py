import json

with open("captions.json") as f:
    data = json.load(f)

for item in data:

    caption = item["caption"].lower()

    tags = []

    if "man and woman" in caption:
        tags.extend([
            "parents",
            "family",
            "couple"
        ])

    if "group" in caption:
        tags.extend([
            "friends",
            "group",
            "people"
        ])

    if "mirror" in caption:
        tags.extend([
            "selfie",
            "portrait"
        ])

    if "coffee" in caption:
        tags.extend([
            "cafe",
            "coffee"
        ])

    if "sunset" in caption:
        tags.extend([
            "sunset",
            "nature"
        ])

    if "beach" in caption:
        tags.extend([
            "beach",
            "vacation",
            "travel"
        ])

    item["tags"] = tags

with open("gallery_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved gallery_data.json")