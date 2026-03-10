import chromadb
from chromadb.utils import embedding_functions

from app.rag.answer_generator import generate_answer

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


def chat(user_input: str):

    results = collection.query(
        query_texts=[user_input],
        n_results=10,
        include=["documents", "metadatas", "distances"]
    )

    docs = []

    for i in range(len(results["documents"][0])):
        docs.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    # Debug retrieval
    print("\n===== RETRIEVE RESULT =====")
    for d in docs:
        print("Distance:", d["distance"])
        print("Content:", d["content"][:100])
        print("---------------------")

    # Sắp xếp theo distance 
    ranked_docs = sorted(docs, key=lambda x: x["distance"])

    print("\n===== AFTER SORT =====")
    for d in ranked_docs[:5]:
        print("Distance:", d["distance"])
        print("Content:", d["content"])
        print("---------------------")

    # lấy top context
    top_docs = ranked_docs[:5]

    answer = generate_answer(user_input, top_docs)

    return answer