# Documentation

## Dataset

Dataset - Wikiart fetched by Hugging Face

## main.py

This script vectorizes WikiArt images using OpenAI's CLIP model.

### Functions

**`get_image_embeddings(model, processor, images, batch_size=32)`**
- Extracts CLIP image embeddings from a list of PIL images
- Uses `model.get_image_features()` to get the vision embedding
- Processes images in batches for efficiency
- Returns numpy array of shape `(num_images, 768)` (CLIP ViT-L/14)

**`process_dataset()`**
- Loads the CLIP model and processor
- Loads the WikiArt dataset from HuggingFace (`huggan/wikiart`)
- Extracts embeddings for all images
- Returns the embedding array

**`main()`**
- Entry point that runs `process_dataset()` and prints results

### Usage

```bash
python main.py
```

### Output

- Embeddings shape: `(num_images, 768)` where 768 is the CLIP ViT-L/14 embedding dimension

### Dependencies

- `transformers` - for CLIP model
- `datasets` - for loading WikiArt dataset
- `torch` - backend
- `numpy` - for embeddings
- `tqdm` - progress bar
