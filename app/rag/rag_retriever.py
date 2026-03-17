import chromadb
from chromadb.utils import embedding_functions

from app.rag.answer_generator import generate_answer
from app.rag.gemini_api import ask_gemini

CHROMA_PATH = "../chroma"
COLLECTION_NAME = "KienthucforRag"

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_func
)


def chat(user_input: str, mode: str):
    # ===== MODE AI =====
    if mode == "ai":
        answer = ask_gemini(user_input)
        return {
            "answer": answer,
            "related_questions": []
        }

    # ===== SEARCH KNOWLEDGE =====
    knowledge_results = collection.query(
        query_texts=[user_input],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )

    knowledge_docs = []

    for i in range(len(knowledge_results["documents"][0])):
        knowledge_docs.append({
            "content": knowledge_results["documents"][0][i],
            "metadata": knowledge_results["metadatas"][0][i],
            "distance": knowledge_results["distances"][0][i]
        })

    ranked_knowledge = sorted(knowledge_docs, key=lambda x: x["distance"])
    top_knowledge = ranked_knowledge[:5]
    answer = generate_answer(user_input, top_knowledge)
    # ===== GENERATE ANSWER =====
    related_questions = []
    for i in ranked_knowledge:
        print(i["distance"], " | ", i["content"][:60])
    for doc in knowledge_results["documents"][0][:5]:
        first_line = doc.split("\n")[0]
        related_questions.append(first_line)
    return {
    "answer": answer,
    "related_questions": related_questions
}