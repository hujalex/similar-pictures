Currently in dev, model prototype can be found here https://colab.research.google.com/drive/1rXJOUN_DZQQroj3ms-aqUKKAlniwo1bH

The provided Google Colab Script currently serves as a prototype for identifying similar pictures from Wikiart’s database of around ~81k paintings. I plan to post a follow-up submission once I have refined the model further and deployed it to a web application.


The public dataset can be found in the given URL https://huggingface.co/datasets/huggan/wikiart 

The model’s Tech Stack primarily consists of
- Python: Programming Language
- Hugging Face: Dataset and Models
- OpenAI CLIP: Image Embedding Model
- Qdrant: Vector Database
- Cloudflare R2: Object Storage


Qdrant’s vector database enables image embeddings to persist after a one-time calculation, allowing us to skip recalculating embeddings for every Google Colab runtime. We would only require a query, given the target’s image embeddings, to identify machines within a pre-calculated set of image embeddings through cosine similarity. 

Each point within the Qdrant vector database consists of not only the image embeddings for the corresponding image but also metadata regarding the image’s ID, artist, genre, and style. The image ID in particular allows us to map image embeddings in the Qdrant vector database to the corresponding static image in Cloudflare R2. 

The following script establishes a Qdrant collection and inserts Qdrant points containing the image ID, image embeddings, and any metadata. We notably Kill and Fill the collection, although performing an Upsert based on the image ID may be more reasonable, especially in future development iterations, to enable uploading individual pictures to the database or updating specific information for images already existing within the database. https://github.com/hujalex/similar-pictures/blob/main/poc/vector-store.py 



Cloudflare R2 allows us to store and retrieve Wikiart paintings, enabling our program to skip loading the entire dataset into memory for each Google Colab runtime. We will also only need to fetch the static image from the Object Store through an API call. This significantly reduces preprocessing time not only in Google Colab but also in serverless functions for a possible matching-painting web application. Furthermore, leveraging an object store along with a vector database enables our framework to accept new additions to the dataset without performing a full reindex.


The following Python script loads the image files from the Wikiart Hugging Face Dataset into a local directory (https://github.com/hujalex/similar-pictures/blob/main/poc/convert_wikiart.py). Due to sizing limitations on the Cloudflare R2 free plan, the script stores images as a “.webp” with a webp quality of “45” and shrinks images larger than 1024 x 1024 pixels. This offers a practical balance between minimizing resource requirements without sacrificing image quality.


OpenAI’s CLIP acts as the primary engine for generating image embeddings (https://huggingface.co/openai/clip-vit-large-patch14). I quickly selected CLIP as a baseline for this prototype, dedicating time instead to first establishing the surrounding framework, with the possibility of evaluating other image embedding models in the future. A Python ImageMatcher class provides a skeleton for leveraging the model to identify and view matches, along with providing a set of utility functions to display images and results. 


Going Forward
- Integrate the script within a web application for a more professional and accessible user experience - maybe even a game or additional features beyond finding similar paintings
- Consider and validate Image models besides CLIP
- Provide functionality to upload images to the Cloudflare R2 Object Store and their embeddings into the Qdrant vector DB.
