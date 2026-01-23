from retriever import retrieve

docs = retrieve(
    question="Bao lâu thì tôi nhận được hàng kể từ lúc đặt?",
    domain="shipping"
)

print("DOC COUNT:", len(docs))

for d in docs:
    print("DISTANCE:", d["distance"])
    print("CONTENT:", d["content"][:120])
    print("-" * 50)
