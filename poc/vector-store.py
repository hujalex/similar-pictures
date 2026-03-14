import requests
import os
from datasets import load_dataset
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
QDRANT_URL = os.getenv('CLUSTER_ENDPOINT')

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

COLLECTION_NAME = "wikiart_embeddings"
EMBEDDING_DIM = 768  # CLIP ViT-L/14



def reset_collection():
    try:
        qdrant_client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # Collection doesn't exist
    

def setup_collection():
    collections = qdrant_client.get_collections().collections
    if not any(c.name == COLLECTION_NAME for c in collections):
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE)
        )
        print(f"Created collection: {COLLECTION_NAME}")
    else:
        print(f"Collection {COLLECTION_NAME} already exists")


def process_batch(model, processor, device, images, metadata_batch, batch_start_idx):
    """Embed a batch of images and upload to Qdrant immediately."""
    inputs = processor(images=images, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
    embeddings = outputs.pooler_output.cpu().numpy()

    points = [
        PointStruct(
            id=batch_start_idx + i,
            vector=embedding.tolist(),
            payload=metadata
        )
        for i, (embedding, metadata) in enumerate(zip(embeddings, metadata_batch))
    ]
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    return len(points)


def process_dataset(batch_size=32):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

    ds = load_dataset("huggan/wikiart", split="train")
    
    artists = ds.features['artist'].names
    genres = ds.features['genre'].names
    style = ds.features['style'].names

    print(f"Dataset size: {len(ds)}")
    print(f"Sample fields: {ds[0].keys()}")

    reset_collection()
    setup_collection()

    total_uploaded = 0
    images = []
    metadata_batch = []

    for i in tqdm(range(len(ds)), desc="Processing images"):
        row = ds[i]
        images.append(row["image"])
        metadata = {
            "artist": artists[row["artist"]],
            "genre": genres[row["genre"]],
            "style": style[row["style"]],
            "image_id": i,
        }
        metadata_batch.append(metadata)

        if len(images) >= batch_size:
            total_uploaded += process_batch(model, processor, device, images, metadata_batch, i - len(images) + 1)
            images = []
            metadata_batch = []

    if images:
        total_uploaded += process_batch(model, processor, device, images, metadata_batch, len(ds) - len(images))

    print(f"Uploaded {total_uploaded} vectors to Qdrant")


def main() -> None:
    process_dataset()

if __name__ == "__main__":
    main()