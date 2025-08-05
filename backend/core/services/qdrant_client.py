import os
import requests
from typing import List, Dict

QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
QDRANT_COLLECTION = os.getenv('QDRANT_COLLECTION', 'global_kb')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY', None)

HEADERS = {'api-key': QDRANT_API_KEY} if QDRANT_API_KEY else {}

def ensure_collection(collection: str, vector_size: int = 1536, distance: str = "Cosine"):
    url = f"{QDRANT_URL}/collections/{collection}"
    
    # Check if we're using Qdrant Cloud (requires API key)
    if QDRANT_URL != 'http://localhost:6333' and not QDRANT_API_KEY:
        raise RuntimeError('QDRANT_API_KEY is required for Qdrant Cloud.')
    
    try:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 200:
            return
        payload = {
            "vectors": {
                "size": vector_size,
                "distance": distance
            }
        }
        resp = requests.put(url, json=payload, headers=HEADERS)
        resp.raise_for_status()
    except Exception as e:
        import logging
        logger = logging.getLogger('ai_manager')
        logger.error(f"Failed to ensure collection {collection}: {e}")
        raise

# --- Upsert vectors ---
def upsert_vectors(vectors: List[Dict], collection: str = QDRANT_COLLECTION):
    ensure_collection(collection)

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
    
    # Check if we're using Qdrant Cloud (requires API key)
    if QDRANT_URL != 'http://localhost:6333' and not QDRANT_API_KEY:
        raise RuntimeError('QDRANT_API_KEY is required for Qdrant Cloud.')
    
    try:
        r = requests.put(url, json=payload, headers=HEADERS)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        import logging
        logger = logging.getLogger('ai_manager')
        logger.error(f"Failed to upsert vectors to {collection}: {e}")
        raise

# --- Delete vectors by doc_id ---
def delete_vectors_by_doc_id(doc_id: str, collection: str = QDRANT_COLLECTION):
    """Delete all vectors in the collection with the given doc_id in payload."""
    url = f"{QDRANT_URL}/collections/{collection}/points/delete"
    payload = {
        "filter": {
            "must": [
                {"key": "doc_id", "match": {"value": doc_id}}
            ]
        }
    }
    if not QDRANT_API_KEY:
        raise RuntimeError('QDRANT_API_KEY is required for Qdrant Cloud.')
    try:
        r = requests.post(url, json=payload, headers=HEADERS)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        import logging
        logging.getLogger('ai_manager').error(f"Failed to delete vectors for doc_id={doc_id} in {collection}: {e}")
        return None

# --- Search vectors ---
def search_vectors(query_embedding: List[float], collection: str = QDRANT_COLLECTION, top: int = 5):
    url = f"{QDRANT_URL}/collections/{collection}/points/search"
    payload = {
        "vector": query_embedding,
        "limit": top,
        "with_payload": True
    }
    
    # Check if we're using Qdrant Cloud (requires API key)
    if QDRANT_URL != 'http://localhost:6333' and not QDRANT_API_KEY:
        raise RuntimeError('QDRANT_API_KEY is required for Qdrant Cloud.')
    
    try:
        r = requests.post(url, json=payload, headers=HEADERS)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        import logging
        logger = logging.getLogger('ai_manager')
        logger.error(f"Failed to search vectors in {collection}: {e}")
        raise