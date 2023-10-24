# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
# pip install -U sentence-transformers

from sentence_transformers import SentenceTransformer
sentences = ["This is an example sentence", "Each sentence is converted"]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(sentences)
print(embeddings)


