from fastapi import FastAPI
from pydantic import BaseModel
from retriever import retrieve
from google import genai
import os
from dotenv import load_dotenv

# =====================
# CONFIG
# =====================
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

FALLBACK_ANSWER = "Chính sách hiện tại chưa quy định trường hợp này."
MAX_DISTANCE = 0.4   # có thể tune: 0.35 → 0.5

app = FastAPI()


# =====================
# SCHEMA
# =====================
class AskRequest(BaseModel):
    question: str
    domain: str


# =====================
# API
# =====================
@app.post("/ask")
def ask(req: AskRequest):
    question = req.question.strip()

    # 1️⃣ Retrieve (semantic search)
    chunks = retrieve(
        question=question,
        domain=req.domain,
        top_k=3
    )
    print("=== RETRIEVE RESULT ===")
    print(chunks)

    if not chunks :
        return {
            "answer": FALLBACK_ANSWER,
            "sources": []
        }

    # 2️⃣ FILTER THEO DISTANCE (RẤT QUAN TRỌNG)
    filtered_chunks = [
        c for c in chunks
        if c.get("distance", 1.0) <= MAX_DISTANCE
    ]

    if not filtered_chunks:
        return {
            "answer": FALLBACK_ANSWER,
            "sources": []
        }

    # 3️⃣ Build context
    context = "\n".join(
        f"[{i+1}] {c['content']}"
        for i, c in enumerate(filtered_chunks)
    )

    # 4️⃣ Prompt khóa chặt
    prompt = f"""
Bạn là chatbot chăm sóc khách hàng của GEARVN.

NHIỆM VỤ:
- Trả lời câu hỏi của khách hàng DỰA HOÀN TOÀN vào nội dung chính sách được cung cấp.
- KHÔNG sử dụng kiến thức bên ngoài chính sách.
- KHÔNG bịa thêm thông tin.

QUY TẮC TRẢ LỜI:
- Nếu trong chính sách có nội dung cho phép SUY RA câu trả lời một cách rõ ràng → hãy trả lời ngắn gọn, đúng trọng tâm.
- Được phép diễn đạt lại nội dung chính sách bằng lời của bạn, miễn là KHÔNG thay đổi ý nghĩa.
- Chỉ khi chính sách HOÀN TOÀN không đề cập → trả lời đúng nguyên văn:
"Chính sách hiện tại chưa quy định trường hợp này."

CHÍNH SÁCH:
{context}

CÂU HỎI:
{question}

TRẢ LỜI:

Nếu trong CHÍNH SÁCH không có thông tin để trả lời →
chỉ trả về đúng câu:
"{FALLBACK_ANSWER}"
"""

    # 5️⃣ Call LLM
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    answer = (response.text or "").strip()
    if not answer:
        answer = FALLBACK_ANSWER

    # 6️⃣ Response
    return {
        "answer": answer,
        "sources": [
            {
                "id": c["id"],
                "domain": c["metadata"].get("domain"),
                "topic": c["metadata"].get("topic"),
                "source": c["metadata"].get("source"),
                "distance": round(c["distance"], 4)
            }
            for c in filtered_chunks
        ]
    }
