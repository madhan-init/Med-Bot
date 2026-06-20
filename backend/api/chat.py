from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from services.database import SessionLocal, ChatLog
import json
import redis
import os

router = APIRouter()

# Initialize Redis client. We use decode_responses=True to get strings back instead of bytes.
redis_url = os.getenv("REDIS_URL")
redis_client = redis.from_url(redis_url, decode_responses=True) if redis_url else None

class ChatRequest(BaseModel):
    message: str
    role: str = "Patient"

@router.post("/chat")
async def chat_endpoint(request: Request, payload: ChatRequest):
    rag_chain = request.app.state.rag_chain
    
    if not rag_chain:
        return {"answer": "The database is currently empty or updating.", "citations": []}

    cache_key = f"medbot:{payload.role}:{payload.message.strip().lower()}"
    
    # 1. Check Redis Cache
    if redis_client:
        try:
            cached_result = redis_client.get(cache_key)
            if cached_result:
                print("⚡ Redis Cache Hit!")
                return json.loads(cached_result)
        except Exception as e:
            print(f"Redis error on get: {e}")

    # 2. RAG Generation
    response = rag_chain.invoke({
        "input": payload.message,
        "role": payload.role
    })
    
    citations = []
    if "context" in response:
        for doc in response["context"]:
            source_file = doc.metadata.get("source", "Unknown Document")
            page_num = doc.metadata.get("page", "N/A")
            
            clean_name = source_file.split("/")[-1].split("\\")[-1] 
            
            citations.append({
                "file": clean_name,
                "page": page_num,
                "content_preview": doc.page_content[:150] + "..."
            })

    unique_citations = [dict(t) for t in {tuple(d.items()) for d in citations}]

    final_response = {
        "answer": response["answer"],
        "citations": unique_citations
    }

    # 3. Save to Redis Cache (Expire after 24 hours = 86400 seconds)
    if redis_client:
        try:
            redis_client.setex(cache_key, 86400, json.dumps(final_response))
            print("💾 Saved to Redis Cache")
        except Exception as e:
            print(f"Redis error on set: {e}")

    # Save to Database
    db = SessionLocal()
    try:
        new_log = ChatLog(
            role=payload.role,
            question=payload.message,
            answer=response["answer"]
        )
        db.add(new_log)
        db.commit()
    except Exception as e:
        print(f"Error saving to database: {e}")
        db.rollback()
    finally:
        db.close()

    return final_response