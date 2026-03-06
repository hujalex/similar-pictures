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
