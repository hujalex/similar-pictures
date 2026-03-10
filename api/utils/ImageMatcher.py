import os
import base64
import io
import torch
import numpy as np
import boto3
import uuid
import matplotlib.pyplot as plt
from tqdm import tqdm
from dotenv import load_dotenv
from datasets import load_dataset
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from api.config import COLLECTION_NAME, qdrant_client, s3


class ImageMatcher:
    
    BUCKET_NAME = 'wikiart-object-storage'

    def __init__(self, data_url, model, processor):
        print("CONSTRUCTOR")
        self.img = self.data_url_to_pillow(data_url) 
        self.model = model
        self.processor = processor
        self.query_vector = self.set_query_vector()
        self.results = self.search_image_embeddings()
     
     
    def data_url_to_pillow(self, data_url: str) -> Image.Image:
        base64_data = data_url.split(',')[1]
        image_bytes = base64.b64decode(base64_data)
        return Image.open(io.BytesIO(image_bytes))


    def search_image_embeddings(self, num_results = 5):
      results = qdrant_client.query_points(
        collection_name = COLLECTION_NAME,
        query = self.query_vector,
        limit = num_results,
        with_payload = True
      )
      return results


    def print_search_results(self):
      for hit in self.results.points:
          print(f"Match Score: {hit.score}")
          print(f"Image Id: {hit.payload['image_id']}")
          print(f"Artist: {hit.payload['artist']}")
          print(f"Genre: {hit.payload['genre']}")


    def display_results(self):
      num_results = len(self.results.points)
      fig, axes = plt.subplots(num_results, 1, figsize=(8, 5 * num_results))
      if num_results == 1:
        axes = [axes]
      for i, hit in enumerate(self.results.points):
        image_id = hit.payload['image_id']
        res = s3.get_object(Bucket = ImageMatcher.BUCKET_NAME, Key = f'{image_id:06}.webp')
        image_data = res['Body'].read()
        img = Image.open(io.BytesIO(image_data))
        axes[i].imshow(img)
        axes[i].set_title(f"Score: {hit.score:.4f} | Artist: {hit.payload['artist']}")
        axes[i].axis('off') # Hide X/Y axes
      
      plt.tight_layout()
      plt.show()


    def display_image(self):
      display(self.img)
      

    def set_query_vector(self):
      inputs = self.processor(images=self.img, return_tensors="pt")
      with torch.no_grad():
          outputs = self.model.get_image_features(**inputs)
          query_vector = outputs.pooler_output.flatten().tolist()
      return query_vector
