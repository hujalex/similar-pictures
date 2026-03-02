import requests
from datasets import load_dataset
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

def applyModel(model, inputs) -> None:
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    return [outputs, logits_per_image, probs]

def processImg(processor, image):
    inputs = processor(text=["a photo of a cat", "a photo of a dog"], images=image, return_tensors="pt", padding=True)
    return inputs

def getImg(url):
    image = Image.open(requests.get(url, stream=True).raw)
    return image

def main() -> None:
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
    url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    
    img = getImg(url)
    inputs = processImg(processor, img)
    results = applyModel(model, inputs)
     
    

if __name__ == "__main__":
    main()