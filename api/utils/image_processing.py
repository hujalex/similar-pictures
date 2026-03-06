import base64
from io import BytesIO
from PIL import Image
import os
import io
import torch
import numpy as np
import boto3
from config import qdrant_client, COLLECTION_NAME, model, processor


def data_url_to_pillow(data_url: str) -> Image.Image:
    base64_data = data_url.split(',')[1]
    image_bytes = base64.b64decode(base64_data)
    return Image.open(BytesIO(image_bytes))

def search_image_embeddings(query_vector):
    results = qdrant_client.query_points(
        collection_name = COLLECTION_NAME,
        query = query_vector,
        limit = 5,
        with_payload = True
    )
    return results

def print_search_results(results):
    for res in results.points:
        print(f"Match Score: {hit.score}")
        print(f"Image Id": {hit.payload{"image_id"}})
        print(f"Artist: {hit.payload['artist']}")
        print(f"Genre: {hit.payload['genre']}")
        print(f"Image URL: {hit.payload['image_url']}")
        
def display_image(image_id):
    res = s3.get_object(bucket = BUCKET_NAME, key = '')
    image_data = res['Body'].read()
    img = Image.open(io.BytesIO(image_data))
    img.show()

def set_query_vector(img):
    inputs = processor(images=img, return_tensors="pt")
    with torch.no_grad():
        query_vector = model.get_image_features(**inputs).flatten().tolist()
    return query_vector
   
# def main():
#     img = Image.open('uploaded-image.jpg')
#     query_vector = set_query_vector(img)
#     res = search(query_vector)
#     print_search_results(res)

