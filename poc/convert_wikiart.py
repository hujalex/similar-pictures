from datasets import load_dataset
from PIL import Image
from tqdm import tqdm
import os
import json

OUTPUT_DIR = "wikiart_images"
METADATA_FILE = "wikiart_metadata.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

ds = load_dataset("huggan/wikiart", split="train")
print(f"Dataset size: {len(ds)}")

metadata_list = []

for i in tqdm(range(len(ds))):
    img = ds[i]["image"]

    # Resize to max 1024px while preserving aspect ratio
    max_size = (1024, 1024)
    img.thumbnail(max_size, Image.LANCZOS)

    filename = f"{i:06d}.webp"
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath, "WEBP", quality=45, method=6, subsampling=0)
    
    metadata_list.append({
        "image_id": i,
        "filename": filename,
        "artist": ds[i]["artist"],
        "genre": ds[i]["genre"],
        "style": ds[i]["style"]
    })

with open(METADATA_FILE, "w") as f:
    json.dump(metadata_list, f, indent=2)

print(f"Saved {len(metadata_list)} images to {OUTPUT_DIR}")
