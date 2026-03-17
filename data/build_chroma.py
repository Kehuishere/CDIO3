import json
import chromadb
from chromadb.utils import embedding_functions
import os

# =====================
# CONFIG
# =====================
CHROMA_PATH = "./chroma"
COLLECTION_NAME = "KienthucforRag"
# Sử dụng model đa ngôn ngữ để hỗ trợ tiếng Việt tốt nhất (384 dims)
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
# tudong chuyen tẽxt ->vecto
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Xóa và tạo mới collection để đảm bảo sạch sẽ
try:
    client.delete_collection(COLLECTION_NAME)
except:
    pass
collection = client.create_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)


with open("D:\HOC\DOANCDIO3\Demo_CDIO3\CDIO3\data\policy-chunks.json", "r", encoding="utf-8") as f:
    policies = json.load(f)

p_docs, p_metas, p_ids = [], [], []
for p in policies:
    if not p.get("content"): continue
    p_docs.append(p["content"])
    p_metas.append({
        "type": "policy",
        "topic": p.get("metadata", {}).get("topic", "general")
    })
    p_ids.append(f"pol_{p.get('id')}")

collection.add(documents=p_docs, metadatas=p_metas, ids=p_ids)
print(f"Đã nạp {len(p_docs)} câu chính sách từ policy-chunks.json")

with open("D:\HOC\DOANCDIO3\Demo_CDIO3\CDIO3\data\cleaned_kb_articles.json", "r", encoding="utf-8") as f:
    products = json.load(f)

prod_docs, prod_metas, prod_ids = [], [], []
for p in products:
    if not p.get("body_md"): continue
    # Format lại nội dung để model dễ hiểu
    text = f"Sản phẩm: {p.get('title')}\nGiá: {p.get('_meta',{}).get('price')}đ\nThông số: {p.get('body_md')}"

    prod_docs.append(text)
    prod_metas.append({
    "type": "product",
    "name": p.get("title"),
    "brand": p.get("_meta", {}).get("brand"),
    "price": p.get("_meta", {}).get("price")
    })
    prod_ids.append(f"prod_{p.get('id')}")

collection.add(documents=prod_docs, metadatas=prod_metas, ids=prod_ids)
print(f"Đã nạp {len(prod_docs)} sản phẩm từ cleaned_kb_articles.json")