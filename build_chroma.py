# # import json
# # import chromadb
# # from chromadb.utils import embedding_functions
# # from pathlib import Path

# # # =====================
# # # CONFIG
# # # =====================
# # CHROMA_PATH = "./chroma"
# # COLLECTION_NAME = "KienthucforRag"

# # POLICY_FILE = "policy-chunks.json"
# # PRODUCT_FILE = "cleaned_kb_articles.json"

# # EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# # # =====================
# # # INIT CHROMA
# # # =====================
# # embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
# #     model_name=EMBEDDING_MODEL
# # )

# # client = chromadb.PersistentClient(path=CHROMA_PATH)

# # collection = client.get_or_create_collection(
# #     name=COLLECTION_NAME,
# #     embedding_function=embedding_fn
# # )

# # # =====================
# # # CLEAR OLD DATA
# # # =====================
# # existing = collection.get(include=[])["ids"]
# # if existing:
# #     collection.delete(ids=existing)
# #     print(f"🧹 Cleared {len(existing)} documents")

# # # =====================
# # # INGEST POLICY
# # # =====================
# # with open(POLICY_FILE, "r", encoding="utf-8") as f:
# #     policies = json.load(f)

# # policy_docs, policy_metas, policy_ids = [], [], []

# # for p in policies:
# #     content = p.get("content")
# #     pid = p.get("id")

# #     if not content or not pid:
# #         continue

# #     meta = p.get("metadata", {})

# #     policy_docs.append(content)
# #     policy_metas.append({
# #         "type": "policy",
# #         "domain": meta.get("domain"),
# #         "topic": meta.get("topic"),
# #         "source": meta.get("source", "GEARVN")
# #     })
# #     policy_ids.append(pid)

# # if policy_docs:
# #     collection.add(
# #         documents=policy_docs,
# #         metadatas=policy_metas,
# #         ids=policy_ids
# #     )

# # print(f"📄 Policy docs ingested: {len(policy_docs)}")

# # # =====================
# # # INGEST PRODUCT
# # # =====================
# # def product_to_text(p: dict) -> str:
# #     return f"""
# # Tên sản phẩm: {p.get("title")}
# # Giá bán: {p.get("_meta", {}).get("price")} VND
# # Thương hiệu: {p.get("_meta", {}).get("brand")}
# # Danh mục: {p.get("_meta", {}).get("category")}
# # Cấu hình: {p.get("body_md")}

# # Mô tả chi tiết:
# # {p.get("body_md")}
# # """.strip()

# # with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
# #     products = json.load(f)

# # if isinstance(products, dict):
# #     products = [products]

# # product_docs, product_metas, product_ids = [], [], []

# # for p in products:
# #     if not p.get("id") or not p.get("body_md"):
# #         continue

# #     product_docs.append(product_to_text(p))
# #     product_metas.append({
# #         "type": "product",
# #         "code": p.get("code"),
# #         "title": p.get("title"),
# #         "brand": p.get("_meta", {}).get("brand"),
# #         "category": p.get("_meta", {}).get("category"),
# #         "price": p.get("_meta", {}).get("price")
# #     })
# #     product_ids.append(p["id"])

# # if product_docs:
# #     collection.add(
# #         documents=product_docs,
# #         metadatas=product_metas,
# #         ids=product_ids
# #     )

# # print(f"💻 Product docs ingested: {len(product_docs)}")

# # # =====================
# # # VERIFY
# # # =====================
# # print("✅ BUILD COMPLETED")
# # print("🔎 Policy count :", len(collection.get(where={"type": "policy"})["ids"]))
# # print("🔎 Product count:", len(collection.get(where={"type": "product"})["ids"]))
# import json
# import chromadb
# from chromadb.utils import embedding_functions
# from parsed import parse_body_md

# # =====================
# # CONFIG
# # =====================
# CHROMA_PATH = "./chroma"
# COLLECTION_NAME = "KienthucforRag"

# POLICY_FILE = "policy-chunks.json"
# PRODUCT_FILE = "cleaned_kb_articles.json"

# EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# # =====================
# # INIT CHROMA
# # =====================
# embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
#     model_name=EMBEDDING_MODEL
# )

# client = chromadb.PersistentClient(path=CHROMA_PATH)

# collection = client.get_or_create_collection(
#     name=COLLECTION_NAME,
#     embedding_function=embedding_fn
# )

# # =====================
# # CLEAR OLD DATA
# # =====================
# existing = collection.get(include=[])["ids"]
# if existing:
#     collection.delete(ids=existing)
#     print(f"🧹 Cleared {len(existing)} documents")

# # =====================
# # INGEST POLICY
# # =====================
# with open(POLICY_FILE, "r", encoding="utf-8") as f:
#     policies = json.load(f)

# policy_docs, policy_metas, policy_ids = [], [], []

# for p in policies:
#     if not p.get("id") or not p.get("content"):
#         continue

#     policy_docs.append(p["content"])
#     policy_metas.append({
#         "type": "policy",
#         "domain": p.get("metadata", {}).get("domain"),
#         "topic": p.get("metadata", {}).get("topic"),
#         "source": p.get("metadata", {}).get("source", "GEARVN")
#     })
#     policy_ids.append(p["id"])

# if policy_docs:
#     collection.add(
#         documents=policy_docs,
#         metadatas=policy_metas,
#         ids=policy_ids
#     )

# print(f"📄 Policy docs ingested: {len(policy_docs)}")

# # =====================
# # INGEST PRODUCT (ĐÃ SỬA)
# # =====================
# def product_to_text(p: dict) -> str:
#     parsed_body = parse_body_md(p.get("body_md", ""))

#     return f"""
# Sản phẩm: {p.get("title")}
# Thương hiệu: {p.get("_meta", {}).get("brand")}
# Danh mục: {p.get("_meta", {}).get("category")}
# Giá bán: {p.get("_meta", {}).get("price")} VND

# Thông tin kỹ thuật:
# {parsed_body}
# """.strip()

# with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
#     products = json.load(f)

# if isinstance(products, dict):
#     products = [products]

# product_docs, product_metas, product_ids = [], [], []

# for p in products:
#     if not p.get("id") or not p.get("body_md"):
#         continue

#     product_docs.append(product_to_text(p))
#     product_metas.append({
#         "type": "product",
#         "code": p.get("code"),
#         "title": p.get("title"),
#         "brand": p.get("_meta", {}).get("brand"),
#         "category": p.get("_meta", {}).get("category"),
#         "price": p.get("_meta", {}).get("price")
#     })
#     product_ids.append(p["id"])

# if product_docs:
#     collection.add(
#         documents=product_docs,
#         metadatas=product_metas,
#         ids=product_ids
#     )

# print(f"💻 Product docs ingested: {len(product_docs)}")

# # =====================
# # VERIFY
# # =====================
# print("✅ BUILD COMPLETED")
# print("🔎 Policy count :", len(collection.get(where={"type": "policy"})["ids"]))
# print("🔎 Product count:", len(collection.get(where={"type": "product"})["ids"]))

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

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Xóa và tạo mới collection để đảm bảo sạch sẽ
try:
    client.delete_collection(COLLECTION_NAME)
except:
    pass
collection = client.create_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)

# =====================
# 1. NẠP POLICY (Chính sách)
# =====================
with open("policy-chunks.json", "r", encoding="utf-8") as f:
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
print(f"✅ Đã nạp {len(p_docs)} câu chính sách từ policy-chunks.json")

# =====================
# 2. NẠP PRODUCT (Sản phẩm)
# =====================
with open("cleaned_kb_articles.json", "r", encoding="utf-8") as f:
    products = json.load(f)

prod_docs, prod_metas, prod_ids = [], [], []
for p in products:
    if not p.get("body_md"): continue
    # Format lại nội dung để model dễ hiểu
    text = f"Sản phẩm: {p.get('title')}\nGiá: {p.get('_meta',{}).get('price')}đ\nThông số: {p.get('body_md')}"
    
    prod_docs.append(text)
    prod_metas.append({
        "type": "product",
        "brand": p.get("_meta", {}).get("brand"),
        "price": p.get("_meta", {}).get("price")
    })
    prod_ids.append(f"prod_{p.get('id')}")

collection.add(documents=prod_docs, metadatas=prod_metas, ids=prod_ids)
print(f"✅ Đã nạp {len(prod_docs)} sản phẩm từ cleaned_kb_articles.json")