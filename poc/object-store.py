import os
import boto3
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")


s3 = boto3.client(
    service_name='s3',
    endpoint_url=f'https://{ACCOUNT_ID}.r2.cloudflarestorage.com',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name="auto"
)

def batch_upload_r2(bucket_name, local_folder):
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            # R2 object key (path inside the bucket)
            relative_path = os.path.relpath(local_path, local_folder)
            
            s3.upload_file(local_path, bucket_name, relative_path)
            print(f"Uploaded {file}")


def upload_to_object_store():
    batch_upload_r2('wikiart-object-storage', './wikiart_images')

def convert_to_webp():
    pass

def load_wikiart_dataset():
    return load_dataset("huggan/wikiart", split="train")

def main():
    upload_to_object_store()

if __name__ == "__main__":
    main()