import qdrant_client
from sentence_transformers import SentenceTransformer, util
import numpy as np
import sys

DATABASE_FILE = "urban-dictionary.db"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "vector-meanings"

# --- Initialize ---
client = qdrant_client.QdrantClient(url=QDRANT_URL)
embedding_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True, device='cuda' if util.torch.cuda.is_available() else 'cpu')

# --- Connect to Qdrant collection--
if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
    print(f"Collection '{COLLECTION_NAME}' does not exist.")
    sys.exit(0)


query = "What are some words originating from Ottawa?"
query_embedding = embedding_model.encode(query)

search_result = client.search(
    collection_name=COLLECTION_NAME,
    query_vector=query_embedding.tolist(),
    limit=10,    
    with_payload=True
)

# 6. Print Results
print(f"Query: {query}")
for result in search_result:
    print(f"Score: {result.score}")
    print(f"Word ID: {result.payload['word_id']}")
    print(f"Word: {result.payload['disambiguation']}")
    print(f"Meaning: {result.payload['meaning']}")
    print(f"Example: {result.payload['example']}")
    print("-" * 20)

# Close the client when done
client.close()