from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.chatbot import ChatRequest, ChatResponse, ConversationContext
from app.crud import mood_entry as mood_crud, depression_risk_result as risk_crud
from app.services.chatbot_service import get_chatbot_response
from app.api.auth import get_current_user

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with the AI assistant"""
    # Build context from user data
    context = None
    
    if chat_request.context or True:  # Always try to build context
        # Get recent mood entry
        recent_moods = mood_crud.get_user_mood_entries(db, user_id=current_user.id, limit=1)
        recent_mood = recent_moods[0] if recent_moods else None
        
        # Get recent risk assessment
        recent_risk = risk_crud.get_latest_risk_result(db, user_id=current_user.id)
        
        # Get statistics
        stats = mood_crud.get_mood_statistics(db, user_id=current_user.id, days=30)
        
        context = ConversationContext(
            user_id=current_user.id,
            recent_mood_level=recent_mood.mood_level if recent_mood else None,
            recent_risk_score=recent_risk.risk_score if recent_risk else None,
            total_entries=stats.get('total_entries', 0),
            average_mood=stats.get('average_mood')
        )
    
    # Get chatbot response
    response = await get_chatbot_response(
        message=chat_request.message,
        conversation_history=chat_request.conversation_history,
        context=context
    )
    
    return response


@router.get("/suggestions", response_model=dict)
async def get_suggestions(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized suggestions based on user data"""
    suggestions = []
    
    # Get recent mood
    recent_moods = mood_crud.get_user_mood_entries(db, user_id=current_user.id, limit=3)
    
    if not recent_moods:
        suggestions.append("Start by logging your first mood check-in!")
        suggestions.append("Tell me how you're feeling today")
    else:
        # Analyze recent trends
        recent_mood = recent_moods[0]
        
        if recent_mood.stress_level >= 7:
            suggestions.append("Your stress seems high. Would you like some relaxation techniques?")
        
        if recent_mood.sleep_hours < 6:
            suggestions.append("Your sleep might be affecting your mood. Want tips for better sleep?")
        
        if recent_mood.physical_activity_minutes < 30:
            suggestions.append("Physical activity can boost mood. Can I suggest some exercises?")
        
        if recent_mood.social_interaction_level <= 2:
            suggestions.append("Social connection is important. Let's talk about ways to connect with others.")
    
    # Get risk assessment
    recent_risk = risk_crud.get_latest_risk_result(db, user_id=current_user.id)
    if recent_risk and recent_risk.risk_level in ["Medium", "High"]:
        suggestions.append("I noticed your risk assessment. Would you like to talk about it?")
    
    # Default suggestions
    if len(suggestions) < 3:
        suggestions.extend([
            "How are you feeling today?",
            "Would you like some mental health tips?",
            "Tell me about your day"
        ])
    
    return {"suggestions": suggestions[:5]}
