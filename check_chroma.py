import chromadb

client = chromadb.Client()
collection = client.get_collection("gearvn_policy")

print("Total docs:", collection.count())
