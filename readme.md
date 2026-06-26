# 📸 Gallery Copilot

Gallery Copilot is an AI-powered photo search assistant that allows users to search their personal gallery using natural language.

Instead of manually scrolling through thousands of photos, users can ask questions such as:

* "Find a good LinkedIn profile picture"
* "Show me my travel photos"
* "Find family memories"
* "Show photos with sunsets"
* "Find a mirror selfie"

The system uses computer vision and natural language processing to understand image content and retrieve relevant photos.

---

## Features

### AI Image Understanding

* Automatic image caption generation using BLIP
* Semantic image search using CLIP
* Metadata enrichment through tags

### Natural Language Search

Users can search using plain English:

Examples:

* family
* parents
* beach vacation
* sunset
* mirror selfie
* coffee shop

### Gallery Knowledge Base

Each image is converted into structured metadata:

```json
{
  "path": "dataset/momdad.jpeg",
  "caption": "a man and woman sitting at a table",
  "tags": ["parents", "family", "couple"]
}
```

### Interactive UI

Built with Streamlit for fast experimentation and prototyping.

---

## Tech Stack

### Frontend

* Streamlit

### AI / Machine Learning

* OpenCLIP
* BLIP Image Captioning
* Sentence Transformers

### Computer Vision

* Pillow (PIL)
* PyTorch

### Data Storage

* JSON

### Language

* Python 3

---

## Project Structure

gallery-copilot/

├── app.py

├── caption_test.py

├── caption_all.py

├── caption_search.py

├── tagger.py

├── captions.json

├── gallery_data.json

├── dataset/

└── README.md

---

## How It Works

1. Images are loaded from the dataset folder.
2. BLIP generates captions for each image.
3. Captions are enriched with tags.
4. Metadata is stored in gallery_data.json.
5. User enters a natural language query.
6. Semantic search retrieves relevant images.
7. Results are displayed through Streamlit.

---

## Future Improvements

* Face detection
* Personal photo clustering
* Aesthetic scoring
* Travel location recognition
* Best profile photo recommendations
* Memory timeline generation
* Local gallery integration
* Mobile application support

---

## Motivation

Most photo galleries are searchable only through filenames or limited metadata.

Gallery Copilot aims to act as an AI assistant for personal photo collections, helping users rediscover memories and quickly find meaningful images through conversation.
