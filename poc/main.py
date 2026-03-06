import os
import io
import toch
import numpy as np
import boto3
from dotenv import load_dotenv
from PIL import Image
from qdrant_client import QdrantClient

load_dotenv()
QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
COLLECTION_NAME = 'wikiart_embeddings'

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

s3 = boto3.client(
    service_name='s3',
    endpoint_url=f'https://{ACCOUNT_ID}.r2.cloudflarestorage.com',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name="auto"
)


def search(query_vector):
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
   
def main():
    img = Image.open('uploaded-image.jpg')
    query_vector = set_query_vector(img)
    res = search(query_vector)
    print_search_results(res)

if __name__ == "__main__":
   main() 