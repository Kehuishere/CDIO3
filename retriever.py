# # import chromadb
# # from chromadb.utils import embedding_functions
# # import os

# # client = chromadb.Client()


# # embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
# #     model_name="all-MiniLM-L6-v2"
# # )

# # collection = client.get_or_create_collection(
# #     name="policies",
# #     embedding_function=embedding_fn
# # )


# # # =====================
# # # RETRIEVE FUNCTION
# # # =====================
# # import chromadb
# # from chromadb.utils import embedding_functions
# # import os

# # # =====================
# # # INIT CHROMA
# # # =====================
# # client = chromadb.Client()

# # embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
# #     model_name="all-MiniLM-L6-v2"
# # )

# # collection = client.get_or_create_collection(
# #     name="policies",
# #     embedding_function=embedding_fn
# # )


# # # =====================
# # # RETRIEVE FUNCTION
# # # =====================
# # def retrieve(question: str, domain: str, top_k: int = 3):
# #     results = collection.query(
# #         query_texts=[question],
# #         n_results=top_k,
# #         where={"domain": domain},
# #         include=["documents", "metadatas", "distances"]
# #     )

# #     if not results["documents"]:
# #         return []

# #     docs = []
# #     for i in range(len(results["documents"][0])):
# #         docs.append({
# #             "id": results["ids"][0][i],
# #             "content": results["documents"][0][i],
# #             "metadata": results["metadatas"][0][i],
# #             "distance": results["distances"][0][i]
# #         })

# #     return docs

# import chromadb

# # PHẢI TRÙNG PATH với lúc ingest
# client = chromadb.PersistentClient(path="./chroma")

# # ✅ CHỈ DÙNG get_collection
# # ❌ KHÔNG embedding_function
# collection = client.get_collection(
#     name="gearvn_policy"
# )

# def retrieve(question: str, domain: str, top_k: int = 3, max_distance: float = 0.45):
#     results = collection.query(
#         query_texts=[question],
#         n_results=top_k,
#         where={"domain": domain},
#         include=["documents", "metadatas", "distances"]
#     )

#     if not results["documents"] or not results["documents"][0]:
#         return []

#     docs = []
#     for i in range(len(results["documents"][0])):
#         distance = results["distances"][0][i]

#         if distance > max_distance:
#             continue

#         docs.append({
#             "content": results["documents"][0][i],
#             "metadata": results["metadatas"][0][i],
#             "distance": distance
#         })

#     return docs


# # TEST TRỰC TIẾP
# if __name__ == "__main__":
#     print("Count:", collection.count())
import chromadb
from typing import List, Dict

# =====================
# CONFIG
# =====================
CHROMA_PATH = "./chroma"          # đúng path đã ingest
COLLECTION_NAME = "gearvn_policy"
DEFAULT_TOP_K = 5
MAX_DISTANCE = 1.2                # chỉnh theo thực tế (0.8–1.5)

# =====================
# INIT CLIENT (PERSISTED)
# =====================
client = chromadb.PersistentClient(path=CHROMA_PATH)

# ⚠️ QUAN TRỌNG:
# KHÔNG truyền embedding_function
collection = client.get_collection(
    name=COLLECTION_NAME
)

# =====================
# RETRIEVE FUNCTION
# =====================
def retrieve(
    question: str,
    domain: str,
    top_k: int = DEFAULT_TOP_K
) -> List[Dict]:

    results = collection.query(
        query_texts=[question],
        n_results=top_k,
        where={"domain": domain},
        include=["documents", "metadatas", "distances"]
    )

    # Không có kết quả
    if not results or not results.get("documents") or not results["documents"][0]:
        return []

    docs = []
    for i in range(len(results["documents"][0])):
        distance = results["distances"][0][i]

        # Optional: lọc theo độ gần ngữ nghĩa
        if distance > MAX_DISTANCE:
            continue

        docs.append({
            "id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": distance
        })

    return docs
