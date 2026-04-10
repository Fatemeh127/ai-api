# from openai import OpenAI
# from fastapi import FastAPI, HTTPException
# from datetime import datetime, timezone
# from config import Message, ChatRequest, ChatResponse, PersonalityRequest, settings

# app = FastAPI()
# client = OpenAI(api_key=settings.openai_api_key)  # use settings not os.getenv!

# @app.get("/health")
# def health():
#     return {
#         "status": "ok",
#         "model": settings.model_name    
#     }

# conversation_history = []  # In-memory conversation history
# @app.post("/chat", response_model=ChatResponse)
# def chat(request: ChatRequest):
#     try:
#         response = client.chat.completions.create(
#             model=settings.model_name,          
#             max_tokens=request.max_tokens,      
#             messages=[
#                 {"role": "user", "content": request.message}
#             ]
#         )
#         ai_response = response.choices[0].message.content

#         result = ChatResponse(
#             user_name=request.user_name,        
#             user_message=request.message,
#             ai_response=ai_response,
#             tokens_used=response.usage.total_tokens  
#         )
#         conversation_history.append({
#             "user_name": request.user_name,
#             "message": request.message,
#             "response": ai_response,
#             "timestamp": datetime.now(timezone.utc).isoformat()
#         })
#         return result

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"OpenAI error: {str(e)}"   
#         )
    
# @app.post("/chat/with-personality", response_model=ChatResponse)
# def chat_personality(request: PersonalityRequest):
#     try:
#         response = client.chat.completions.create(
#             model=settings.model_name,
#             max_tokens=request.max_tokens,
#             messages=[
#                 {"role": "system", "content": request.personality},  
#                 {"role": "user", "content": request.message}
#             ]
#         )
#         ai_response = response.choices[0].message.content

#         result = ChatResponse(              
#             user_name=request.user_name,
#             user_message=request.message,
#             ai_response=ai_response,
#             tokens_used=response.usage.total_tokens
#         )
#         conversation_history.append({
#             "user_name": request.user_name,
#             "message": request.message,
#             "response": ai_response,
#             "timestamp": datetime.now(timezone.utc).isoformat()
#         })
#         return result
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"OpenAI error: {str(e)}"
#         )
    
# @app.get("/conversation-history")
# def get_conversation_history():
#     return conversation_history 

#-------------------------------- USE DATABASE  ------------------ --------------
# from openai import OpenAI
# from fastapi import FastAPI, HTTPException
# from datetime import datetime, timezone
# from .config import ChatRequest, ChatResponse, PersonalityRequest, settings
# from .database import ChatHistory, get_db
# from sqlalchemy.orm import Session
# from fastapi import Depends


# app = FastAPI()
# client = OpenAI(api_key=settings.openai_api_key)  # use settings not os.getenv!

# @app.get("/health")
# def health():
#     return {
#         "status": "ok",
#         "model": settings.model_name    
#     }

# @app.post("/chat", response_model=ChatResponse)
# def chat(request: ChatRequest, db: Session = Depends(get_db)):
#     try:
#         response = client.chat.completions.create(
#             model=settings.model_name,          
#             max_tokens=request.max_tokens,      
#             messages=[
#                 {"role": "user", "content": request.message}
#             ]
#         )
#         ai_response = response.choices[0].message.content

#         new_record = ChatHistory(
#             user_name=request.user_name,        
#             user_message=request.message,
#             ai_response=ai_response,
#             timestamp=datetime.now(timezone.utc).isoformat(),
#             tokens_used=response.usage.total_tokens  
#         )
#         db.add(new_record)
#         db.commit()
        
#         return ChatResponse(
#             user_name=request.user_name,        
#             user_message=request.message,
#             ai_response=ai_response,
#             tokens_used=response.usage.total_tokens  
#         )

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"OpenAI error: {str(e)}"   
#         )
    
# @app.post("/chat/with-personality", response_model=ChatResponse)
# def chat_personality(request: PersonalityRequest, db: Session = Depends(get_db)):
#     try:
#         response = client.chat.completions.create(
#             model=settings.model_name,
#             max_tokens=request.max_tokens,
#             messages=[
#                 {"role": "system", "content": request.personality},  
#                 {"role": "user", "content": request.message}
#             ]
#         )
#         ai_response = response.choices[0].message.content

#         new_record = ChatHistory(
#             user_name=request.user_name,
#             user_message=request.message,
#             ai_response=ai_response,
#             timestamp=datetime.now(timezone.utc).isoformat(),
#             tokens_used=response.usage.total_tokens
#         )
#         db.add(new_record)
#         db.commit()

#         return ChatResponse(              
#             user_name=request.user_name,
#             user_message=request.message,
#             ai_response=ai_response,
#             tokens_used=response.usage.total_tokens
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"OpenAI error: {str(e)}"
#         )
    
# @app.get("/conversation-history")
# def get_conversation_history(db: Session = Depends(get_db)):
#     return db.query(ChatHistory).all()

# @app.get("/conversation-history/{user_name}")
# def get_conversation_history_by_user(user_name: str, db: Session = Depends(get_db)):
#     return db.query(ChatHistory).filter(ChatHistory.user_name == user_name).all()

# @app.delete("/conversation-history/{user_name}")
# def delete_conversation_history_by_user(user_name: str, db: Session = Depends(get_db)):
#     records = db.query(ChatHistory).filter(ChatHistory.user_name == user_name).all()
#     if not records:
#         raise HTTPException(status_code=404, detail="No conversation history found for this user.")
#     for record in records:
#         db.delete(record)
#     db.commit()
#     return {"detail": f"Deleted conversation history for user {user_name}."}


#---------------use async-----------------------
from openai import AsyncOpenAI         # ✅ async client!
from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime, timezone
from config import ChatRequest, ChatResponse, PersonalityRequest, settings
from database import ChatHistory, get_db
from sqlalchemy.orm import Session

app = FastAPI()
client = AsyncOpenAI(api_key=settings.openai_api_key)  # ✅ async client!

@app.get("/health")
async def health():                    
    return {
        "status": "ok",
        "model": settings.model_name
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        response = await client.chat.completions.create(  
            model=settings.model_name,
            max_tokens=request.max_tokens,
            messages=[
                {"role": "user", "content": request.message}
            ]
        )
        ai_response = response.choices[0].message.content

        new_record = ChatHistory(
            user_name=request.user_name,
            user_message=request.message,
            ai_response=ai_response,
            timestamp=datetime.now(timezone.utc).isoformat(),
            tokens_used=response.usage.total_tokens
        )
        db.add(new_record)            
        db.commit()                   

        return ChatResponse(
            user_name=request.user_name,
            user_message=request.message,
            ai_response=ai_response,
            tokens_used=response.usage.total_tokens
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")


@app.post("/chat/with-personality", response_model=ChatResponse)
async def chat_personality(request: PersonalityRequest, db: Session = Depends(get_db)):
    try:
        response = await client.chat.completions.create( 
            model=settings.model_name,
            max_tokens=request.max_tokens,
            messages=[
                {"role": "system", "content": request.personality},
                {"role": "user", "content": request.message}
            ]
        )
        ai_response = response.choices[0].message.content

        new_record = ChatHistory(
            user_name=request.user_name,
            user_message=request.message,
            ai_response=ai_response,
            timestamp=datetime.now(timezone.utc).isoformat(),
            tokens_used=response.usage.total_tokens
        )
        db.add(new_record)            
        db.commit()                  

        return ChatResponse(
            user_name=request.user_name,
            user_message=request.message,
            ai_response=ai_response,
            tokens_used=response.usage.total_tokens
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")


@app.get("/conversation-history")
async def get_conversation_history(db: Session = Depends(get_db)):  
    return db.query(ChatHistory).all()


@app.get("/conversation-history/{user_name}")
async def get_conversation_history_by_user(
    user_name: str,
    db: Session = Depends(get_db)
):  
    return db.query(ChatHistory).filter(
        ChatHistory.user_name == user_name
    ).all()


@app.delete("/conversation-history/{user_name}")
async def delete_conversation_history_by_user(
    user_name: str,
    db: Session = Depends(get_db)
):
    records = db.query(ChatHistory).filter(   
        ChatHistory.user_name == user_name
    ).all()
    if not records:
        raise HTTPException(status_code=404, detail="No history found!")
    for record in records:
        db.delete(record)                     
    db.commit()                                
    return {"detail": f"Deleted history for {user_name}!"}
