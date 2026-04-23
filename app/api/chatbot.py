from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
import json
import logging
from app.database import get_db
from app.models.chatbot import (
    ChatMessage,
    ConversationContext,
    FrontendChatBootstrapResponse,
    FrontendChatMessageRequest,
    FrontendChatMessageResponse,
)
from app.models.user import User
from pydantic.json import pydantic_encoder
from app.crud import mood_entry as mood_crud, depression_risk_result as risk_crud, chat_history as chat_history_crud
from app.services.chatbot_service import (
    init_gemini_chat,
    dict_to_message,
    message_to_dict,
)
from app.api.auth import get_current_user
from app.utils.security import decode_access_token
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


def _build_conversation_context(db: Session, user_id: int) -> ConversationContext:
    """Build personalized context from user's recent data."""
    recent_moods = mood_crud.get_user_mood_entries(db, user_id=user_id, limit=1)
    recent_mood = recent_moods[0] if recent_moods else None

    recent_risk = risk_crud.get_latest_risk_result(db, user_id=user_id)
    stats = mood_crud.get_mood_statistics(db, user_id=user_id, days=30)

    return ConversationContext(
        user_id=user_id,
        recent_mood_level=recent_mood.mood_level if recent_mood else None,
        recent_risk_score=recent_risk.risk_score if recent_risk else None,
        total_entries=stats.get("total_entries", 0),
        average_mood=stats.get("average_mood"),
    )


@router.get("/conversation/bootstrap", response_model=FrontendChatBootstrapResponse)
async def conversation_bootstrap(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Bootstrap payload for frontend chatbot screen."""
    context = _build_conversation_context(db=db, user_id=current_user.id)

    starter_suggestions = [
        "How are you feeling today?",
        "Help me manage stress",
        "Give me a short breathing exercise",
        "How can I sleep better tonight?",
    ]

    return FrontendChatBootstrapResponse(
        session_id=str(uuid4()),
        welcome_message=(
            "Hi, I'm Lumora Assistant. I'm here to support your mental wellbeing. "
            "You can share how you're feeling, and I'll offer practical suggestions."
        ),
        suggestions=starter_suggestions,
        context_summary={
            "recent_mood_level": context.recent_mood_level,
            "recent_risk_score": context.recent_risk_score,
            "total_entries": context.total_entries,
            "average_mood": context.average_mood,
        },
    )

async def get_user_from_token(token: str, db: Session) -> dict:
    """Extract user info from auth token"""
    try:
        token_data = decode_access_token(token)
        if not token_data or not token_data.user_id:
            print("Invalid token data:", token_data)
            return None
        return {"user_id": token_data.user_id}
    except Exception as e:
        print(f"Token decode error: {str(e)}")
        logger.error(f"Token decode error: {str(e)}")
        return None


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(None)):
    """
    WebSocket endpoint for real-time chat with Gemini AI.
    Query parameter: token (JWT token for authentication)
    
    Message format (JSON):
    {
        "type": "message",
        "content": "user message"
    }
    
    Response format (JSON):
    {
        "type": "message",
        "role": "assistant",
        "content": "assistant response"
    }
    """

    if not token:
        print("WebSocket connection rejected: Missing token")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Missing authentication token")
        return
    
    # Get database session
    db = next(get_db())

    user_id = None  # Initialize user_id for scope access in finally block

    try:
        # Authenticate user
        user_info = await get_user_from_token(token, db)
        if not user_info:
            print("WebSocket connection rejected: Invalid token")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
            return
        
        print(user_info)
        
        user_id = user_info["user_id"]
        
        # Accept connection
        await websocket.accept()
        
        logger.info(f"WebSocket connection established for user {user_id}")
        
         # Load previous chat history
        existing_history = chat_history_crud.get_user_chat_history(db, user_id)
        if existing_history and existing_history.messages:
        # Initialize Gemini chat
            print("here is a message")
            history_messages = [dict_to_message(msg) for msg in json.loads(existing_history.messages)]
            chat = init_gemini_chat(history=history_messages)
        else:
            chat = init_gemini_chat()

        if not chat:
            await websocket.send_json({
                "type": "error",
                "content": "Failed to initialize chat. Please try again."
            })
            raise Exception("Failed to initialize Gemini chat")

        # Send welcome message
        await websocket.send_json({
            "type": "welcome",
            "content": "Hi, I'm Lumora Assistant. I'm here to support your mental wellbeing. How can I help you today?"
        })
        
        # Main message loop
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_json()
                
                if data.get("type") == "message":
                    user_message = data.get("content", "").strip()
                    
                    if not user_message:
                        await websocket.send_json({
                            "type": "error",
                            "content": "Please send a non-empty message."
                        })
                        continue
                    
                    # Send message to Gemini
                    try:
                        print(f"Sending message to Gemini: {user_message}")
                        response = chat.send_message(user_message)
                        assistant_message = response.text
                        
                        # Format and send response
                        await websocket.send_json({
                            "type": "message",
                            "role": "assistant",
                            "content": assistant_message
                        })
                        
                    except Exception as e:
                        logger.error(f"Gemini API error: {str(e)}")
                        await websocket.send_json({
                            "type": "error",
                            "content": f"Error processing message: {str(e)}"
                        })
                        
            except WebSocketDisconnect:
                logger.info(f"WebSocket disconnected for user {user_id}")
                # Save chat history
                try:
                    history_messages = chat.get_history()
                    if history_messages:
                        chat_history_crud.update_chat_history(db, user_id, json.dumps([message_to_dict(msg) for msg in history_messages], default=pydantic_encoder))
                        logger.info(f"Saved {len(history_messages)} messages for user {user_id}")
                except Exception as e:
                    logger.error(f"Error saving chat history: {str(e)}")
                break
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "content": "Invalid message format"
                })
            except Exception as e:
                logger.error(f"WebSocket error: {str(e)}")
                await websocket.send_json({
                    "type": "error",
                    "content": "An error occurred"
                })
                break
    
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}")
        try:
            await websocket.close(code=status.WS_1011_SERVER_ERROR)
        except:
            pass
    finally:
        # Close database session
        try:
            db.close()
        except:
            pass


@router.get("/conversation/history", response_model=list[ChatMessage])
async def get_conversation_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve the user's chat history."""
    history = chat_history_crud.get_user_chat_history(db, user_id=current_user.id)
    if not history or not history.messages:
        return []
    
    messages = json.loads(history.messages)
    
    # Convert the loaded messages into ChatMessage objects
    chat_messages = [ChatMessage(role='assistant' if msg['role'] == 'model' else 'user', content=msg['parts'][0]['text']) for msg in messages]
    
    return chat_messages


