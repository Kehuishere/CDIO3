import chromadb
import json
from sentence_transformers import SentenceTransformer

# 🔴 QUAN TRỌNG: path lưu DB
client = chromadb.PersistentClient(path="./chroma")

collection = client.get_or_create_collection(
    name="gearvn_policy"
)

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("policy-chunks.json", "r", encoding="utf-8") as f:
    docs = json.load(f)

documents = [d["content"] for d in docs]
metadatas = [d["metadata"] for d in docs]
ids = [d["id"] for d in docs]

embeddings = model.encode(documents).tolist()

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
    embeddings=embeddings
)

print("✅ ChromaDB indexed & persisted")
