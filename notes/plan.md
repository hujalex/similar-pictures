**Requirements**

- Design a ranking system to rank images based on similarity - should be explainable

- should be fairly performant and easy to extend

**Strategy**

- Select a few photos online to validate model ensuring that quality remains top-notch as well as consistent
  - First classicial images
  - then images from other genres like sports

- Vectorized Database (likely Qdrant) to store the vectorized images

- Object Store to store the actual image in a compressed format (webp) to reduce storage size
  - Cloudflare R2 (10 gb limit)
  - Images set to webp file format with quality of 60

- Vectorized Database will contain metadata for each record that maps to the respective image in the Object Store

**Tech Stack**

- Vectorized Database - Qdrant
- Object Store - Cloudflare R2
- Similarity Matching - FastAPI, CLIP
- Web App - Next js

General idea of Web App

- User will upload an image, immediately running the similarity matching algorithm on FastAPI Backend. Backend should return brief descriptions of matched images. If successfully, make another API call to fetch images from Cloudflare R2 Object Store
