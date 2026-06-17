import os
import json
import uuid
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "semantic_cache"))
METADATA_FILE = os.path.join(CACHE_DIR, "metadata.json")
SIMILARITY_THRESHOLD = 0.85
MAX_CACHE_SIZE = 1000

cache_vector_store = None
lru_keys = []
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

def _load_metadata():
    global lru_keys
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                data = json.load(f)
                lru_keys = data.get("lru_keys", [])
        except Exception as e:
            print(f"Error loading metadata: {e}")
            lru_keys = []
    else:
        lru_keys = []

def _save_metadata():
    global lru_keys
    try:
        with open(METADATA_FILE, "w") as f:
            json.dump({"lru_keys": lru_keys}, f)
    except Exception as e:
        print(f"Error saving metadata: {e}")

def init_cache():
    global cache_vector_store
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR, exist_ok=True)
        
    _load_metadata()
        
    index_path = os.path.join(CACHE_DIR, "index.faiss")
    if os.path.exists(index_path):
        try:
            cache_vector_store = FAISS.load_local(
                CACHE_DIR, 
                embeddings, 
                allow_dangerous_deserialization=True
            )
            print("Semantic cache initialized successfully!")
        except Exception as e:
            print(f"Failed to load semantic cache: {e}")
            cache_vector_store = None
    else:
        print("Semantic cache not found. It will be created on the first query.")

def check_cache(query: str):
    global cache_vector_store, lru_keys
    if not cache_vector_store:
        return None
        
    try:
        results = cache_vector_store.similarity_search_with_relevance_scores(query, k=1)
        if results:
            doc, score = results[0]
            if score >= SIMILARITY_THRESHOLD:
                print(f"Cache HIT! Score: {score}")
                
                doc_id = doc.metadata.get("doc_id")
                if doc_id:
                    if doc_id in lru_keys:
                        lru_keys.remove(doc_id)
                    lru_keys.append(doc_id)
                    _save_metadata()
                    
                return {
                    "answer": doc.metadata.get("answer", ""),
                    "citations": json.loads(doc.metadata.get("citations", "[]")),
                    "cached": True
                }
    except Exception as e:
        print(f"Error checking semantic cache: {e}")
    return None

def add_to_cache(query: str, answer: str, citations: list):
    global cache_vector_store, lru_keys
    
    doc_id = str(uuid.uuid4())
    metadata = {
        "doc_id": doc_id,
        "answer": answer, 
        "citations": json.dumps(citations)
    }
    
    try:
        if not cache_vector_store:
            cache_vector_store = FAISS.from_texts([query], embeddings, metadatas=[metadata], ids=[doc_id])
        else:
            cache_vector_store.add_texts(texts=[query], metadatas=[metadata], ids=[doc_id])
            
        lru_keys.append(doc_id)
        
        if len(lru_keys) > MAX_CACHE_SIZE:
            oldest_id = lru_keys.pop(0)
            try:
                cache_vector_store.delete([oldest_id])
                print(f"Evicted oldest cache item: {oldest_id}")
            except Exception as e:
                print(f"Error evicting cache item: {e}")
                
        cache_vector_store.save_local(CACHE_DIR)
        _save_metadata()
        print("Added to semantic cache.")
    except Exception as e:
        print(f"Error adding to semantic cache: {e}")
