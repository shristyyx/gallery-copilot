import os
import requests

os.makedirs("dataset", exist_ok=True)

for i in range(100):
    url = f"https://picsum.photos/800/600?random={i}"

    img = requests.get(url).content

    with open(f"dataset/img_{i}.jpg", "wb") as f:
        f.write(img)

    print(f"Downloaded {i+1}/100")