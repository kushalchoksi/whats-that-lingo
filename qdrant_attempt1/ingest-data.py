import sqlite3
import qdrant_client
from qdrant_client.models import Distance, VectorParams, models
from sentence_transformers import SentenceTransformer, util
from datetime import datetime
import re
import logging

DATABASE_FILE = "urban-dictionary.db"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "vector-meanings"

# --- Initialize ---
client = qdrant_client.QdrantClient(url=QDRANT_URL)
embedding_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True, device='cuda' if util.torch.cuda.is_available() else 'cpu')

# Configure logging (do this once at the beginning of your script)
logging.basicConfig(filename='ingest_data.log', level=logging.INFO,  # Adjust level as needed
                    format='%(asctime)s - %(levelname)s - %(message)s')


# --- Create Qdrant collection if it doesn't exist ---
try:
    client.get_collection(COLLECTION_NAME)
    print(f"Collection '{COLLECTION_NAME}' already exists.")
except qdrant_client.http.exceptions.ApiException as e:
    print(e.status_code)
    if e.status_code == 404:  # Collection not found
        client.create_collection(
            collection_name=COLLECTION_NAME,
            # vectors_config=qdrant_client.models.VectorParams(size=embedding_model.get_sentence_embedding_dimension(), distance=qdrant_client.models.Distance.COSINE), # Important: Define vector size and distance
            vectors_config=models.VectorParams(size=embedding_model.get_sentence_embedding_dimension(), distance=Distance.COSINE)
        )
        print(f"Collection '{COLLECTION_NAME}' created.")
    else:
        raise  # Re-raise other exceptions


# --- Database interaction and data ingestion ---
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

cursor.execute("SELECT * FROM meanings")  # Select all rows from the meanings table
rows = cursor.fetchall()

points = [] # list to store points
index = 1

for row in rows:
    meaning_id, word_id, def_id, disambiguation, meaning, example, author, upvotes, downvotes, permalink, date_written = row

    logging.debug(f"Processing row: meaning_id={meaning_id}, word_id={word_id}, def_id={def_id}") # Detailed row info

    # --- Create payload (metadata) ---
    payload = {
        "word_id": word_id,
        "def_id": def_id,
        "disambiguation": disambiguation,
        "meaning": meaning,
        "example": example,
        "author": author,
        "upvotes": upvotes,
        "downvotes": downvotes,
        "permalink": permalink,
        "date_written": date_written,  # Store the date in the payload
    }

    logging.debug(f"Payload created: {payload}")  # Log the created payload

    # --- Generate embedding ---
    stripped_meaning = re.sub(r'\[(.*?)\]', r'\1', meaning)
    full_meaning = f"{disambiguation} - {stripped_meaning}"
    text_to_embed = re.sub(r'\[(.*?)\]', r'\1', full_meaning)  # Embed the 'meaning' field. You can change this if needed.

    logging.debug(f"Text to embed: {text_to_embed}")

    embedding = embedding_model.encode(text_to_embed)

    # --- Create a point for Qdrant ---
    point = qdrant_client.models.PointStruct(
        id=meaning_id,  # Use meaning_id as the point ID (important for updates)
        vector=embedding.tolist(),  # Embeddings must be lists
        payload=payload,
    )

    logging.debug(f"Qdrant point created: id={point.id}, vector[:5]={point.vector[:5]}..., payload={point.payload.keys()}") # Log point info

    points.append(point)
    logging.info(f"Point added to list: meaning_id={meaning_id}") 

    print(f"Completed {index} of {len(rows)}")
    index += 1

# Upsert points to Qdrant.  Batching significantly improves performance.
batch_size = 100 # Adjust batch size as needed
for i in range(0, len(points), batch_size):
    batch = points[i:i + batch_size]
    client.upsert(
        collection_name=COLLECTION_NAME,
        wait=True, # Wait for the operation to complete
        points=batch,
    )
    print(f"Upserted batch {i//batch_size + 1} of {len(points)//batch_size + 1}")

conn.close()
client.close()

print("Data ingestion complete.")