import os
import requests
from typing import List, Dict

QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
QDRANT_COLLECTION = os.getenv('QDRANT_COLLECTION', 'global_kb')

# --- Upsert vectors ---
def upsert_vectors(vectors: List[Dict], collection: str = QDRANT_COLLECTION):
    url = f"{QDRANT_URL}/collections/{collection}/points"
    payload = {
        "points": [
            {
                "id": i,
                "vector": v['embedding'],
                "payload": {"chunk": v['chunk'], **v.get('metadata', {})}
            }
            for i, v in enumerate(vectors)
        ]
    }
    r = requests.put(url, json=payload)
    r.raise_for_status()
    return r.json()

# --- Search vectors ---
def search_vectors(query_embedding: List[float], collection: str = QDRANT_COLLECTION, top: int = 5):
    url = f"{QDRANT_URL}/collections/{collection}/points/search"
    payload = {
        "vector": query_embedding,
        "limit": top
    }
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json() 