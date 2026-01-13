from PIL import Image
import torch
from transformers import AutoProcessor, AutoModel

class ImageVectorizer:
    def __init__(self, model_name: str = "google/siglip-base-patch16-224"):
        print(f"Loading SigLIP model: {model_name}...")
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        self.model.to(self.device)
        print(f"Model loaded on {self.device}")

    def vectorize(self, image: Image.Image):
        """
        Generate embedding for a single PIL Image.
        """
        # Ensure image is RGB
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.get_image_features(**inputs)
            
        # Normalize the embeddings if needed, SigLIP usually works with raw features or normalized.
        # Often helpful to normalize for cosine similarity.
        embeddings = outputs / outputs.norm(p=2, dim=-1, keepdim=True)
        return embeddings.cpu().numpy()[0]
