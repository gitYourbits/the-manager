import openai
import os
from typing import List, Dict
import tiktoken
from PyPDF2 import PdfReader
import docx

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# --- Token-based chunking with overlap ---
def chunk_text_token_overlap(text: str, max_tokens: int = 512, overlap: int = 64, model: str = 'text-embedding-3-small') -> List[Dict]:
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    chunks = []
    i = 0
    while i < len(tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append({
            'chunk': chunk_text,
            'chunk_index': len(chunks),
            'start_token': i,
            'end_token': i+len(chunk_tokens)
        })
        i += max_tokens - overlap
    return chunks

# --- Embedding utility ---
def embed_text(texts: List[str], model: str = 'text-embedding-3-small') -> List[List[float]]:
    response = openai.embeddings.create(input=texts, model=model)
    return [d['embedding'] for d in response['data']]

# --- File extraction utilities ---
def extract_text_from_pdf(file_field) -> str:
    file_field.seek(0)
    reader = PdfReader(file_field)
    text = "\n".join(page.extract_text() or '' for page in reader.pages)
    return text

def extract_text_from_docx(file_field) -> str:
    file_field.seek(0)
    doc = docx.Document(file_field)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text

# --- Main ingestion function ---
def ingest_document(file_field, file_type: str, doc_metadata: Dict = None, user_id: int = None, is_global: bool = False) -> List[Dict]:
    doc_metadata = doc_metadata or {}
    if file_type == 'txt':
        file_field.seek(0)
        text = file_field.read().decode('utf-8')
    elif file_type == 'pdf':
        text = extract_text_from_pdf(file_field)
    elif file_type == 'docx':
        text = extract_text_from_docx(file_field)
    else:
        raise ValueError('Unsupported file type for ingestion')
    chunks = chunk_text_token_overlap(text)
    chunk_texts = [c['chunk'] for c in chunks]
    embeddings = embed_text(chunk_texts)
    results = []
    for chunk, embedding in zip(chunks, embeddings):
        meta = {
            **doc_metadata,
            'chunk_index': chunk['chunk_index'],
            'start_token': chunk['start_token'],
            'end_token': chunk['end_token'],
            'is_global': is_global
        }
        if user_id is not None:
            meta['user_id'] = user_id
        results.append({
            'chunk': chunk['chunk'],
            'embedding': embedding,
            'metadata': meta
        })
    return results 