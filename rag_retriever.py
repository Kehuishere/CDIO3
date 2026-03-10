import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import CrossEncoder
from typing import List, Dict
import os

# =============================
# CONFIG & MODELS
# =============================
CHROMA_PATH = "./chroma"
COLLECTION_NAME = "KienthucforRag"

# Model 384 dims (Đồng bộ với file Ingest)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_func)

# =============================
# LOGIC HỖ TRỢ (INTENT DETECTION)
# =============================

def get_query_intent(query: str) -> str:
    """Xác định tìm trong kho Policy hay Product"""
    policy_keywords = ["lộ", "bảo mật", "an toàn", "dữ liệu", "chính sách", "bảo hành", "đổi trả", "thông tin cá nhân", "uy tín"]
    if any(k in query.lower() for k in policy_keywords):
        return "policy"
    return "product"

def generate_answer(query: str, relevant_docs: List[Dict], intent: str):
    """Tạo câu trả lời dựa trên kho dữ liệu đã lọc"""
    
    if not relevant_docs:
        return "Xin lỗi, tôi không tìm thấy thông tin phù hợp trong hệ thống."

    best_doc = relevant_docs[0]
    score = best_doc['score']
    meta = best_doc['metadata']
    content = best_doc['content']

    # Ngưỡng chặn rác (Threshold)
    if score < -8:
        return f"Tôi chưa tìm thấy thông tin cụ thể về {'chính sách' if intent == 'policy' else 'sản phẩm'} này. Bạn vui lòng cung cấp thêm chi tiết nhé."

    # Trả lời theo kho dữ liệu
    if meta.get('type') == 'product':
        brand = meta.get('brand', 'Sản phẩm')
        price = meta.get('price', 0)
        # Ép kiểu giá tiền nếu metadata trả về string
        try:
            formatted_price = f"{int(float(price)):,}đ"
        except:
            formatted_price = "liên hệ"
            
        return f"Thông tin sản phẩm {brand}: {content[:200]}... Giá tham khảo: {formatted_price}."
    
    elif meta.get('type') == 'policy':
        return f"Về vấn đề bạn quan tâm, chính sách cửa hàng quy định: {content}"

    return "Tôi đã tìm thấy thông tin nhưng chưa thể xác định câu trả lời chính xác."

# =============================
# CHAT PIPELINE (OPTIMIZED)
# =============================

def chat(user_input: str):
    # 1. Nhận diện intent để lọc Metadata (WHERE clause)
    intent = get_query_intent(user_input)
    
    # 2. Tìm kiếm CÓ ĐIỀU KIỆN - Đây là bước tối ưu nhất
    results = collection.query(
        query_texts=[user_input],
        n_results=10,
        where={"type": intent}, # Ép ChromaDB chỉ tìm trong policy hoặc product
        include=["documents", "metadatas", "distances"]
    )
    
    if not results["documents"][0]:
        return f"Hiện tại tôi chưa có dữ liệu về {intent} này.", []

    # 3. Format & Rerank
    docs = []
    for i in range(len(results["documents"][0])):
        docs.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        })

    pairs = [[user_input, d["content"]] for d in docs]
    scores = reranker.predict(pairs)
    for i, s in enumerate(scores): docs[i]['score'] = s
    
    ranked_docs = sorted(docs, key=lambda x: x['score'], reverse=True)

    # 4. Generate Answer
    answer = generate_answer(user_input, ranked_docs, intent)
    
    return answer, ranked_docs

if __name__ == "__main__":
    print("--- Hệ thống RAG đã được tối ưu (Gõ 'exit' để thoát) ---")
    while True:
        u = input("\nUser: ")
        if u.lower() in ['exit', 'quit']: break
        
        ans, sources = chat(u)
        print(f"\nBot: {ans}")
        
        if sources:
            # Sửa lỗi index sources[5] nếu kết quả trả về ít hơn 6
            best_score = round(float(sources[0]['score']), 2)
            doc_type = sources[0]['metadata'].get('type')
            print(f"[Debug] Score: {best_score} | Kho dữ liệu: {doc_type}")