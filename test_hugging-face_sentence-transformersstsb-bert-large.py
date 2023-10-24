# https://huggingface.co/sentence-transformers/stsb-bert-large
# This model returns vector embeddings with 1024 dimensions

from sentence_transformers import SentenceTransformer
sentences = ["This is an example sentence", "Each sentence is converted"]

model = SentenceTransformer('sentence-transformers/stsb-bert-large')
embeddings = model.encode(sentences)
print(embeddings)
