from typing import List, Optional
from app.models.chatbot import ChatMessage, ChatResponse, ConversationContext
from app.config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Try to import OpenAI, but don't fail if it's not installed
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI library not available. Chatbot will use fallback responses.")


def build_system_prompt(context: Optional[ConversationContext] = None) -> str:
    """Build system prompt with user context"""
    base_prompt = """You are a compassionate mental health support assistant for Lumora, 
a mental health tracking application. Your role is to:

1. Provide emotional support and active listening
2. Offer evidence-based coping strategies
3. Encourage healthy habits (sleep, exercise, social connection)
4. Recognize when professional help is needed
5. Never diagnose or prescribe medication
6. Always prioritize user safety

Important guidelines:
- Be empathetic, warm, and non-judgmental
- Use simple, clear language
- Validate feelings without dismissing concerns
- Suggest professional help when appropriate
- Provide crisis resources if needed (988 Suicide & Crisis Lifeline)
- Keep responses concise and actionable
"""
    
    if context:
        context_info = f"""

Current user context:
- Recent mood: {context.recent_mood_level or 'Not available'}
- Risk assessment: {f'{context.recent_risk_score:.0%} risk score' if context.recent_risk_score else 'Not assessed'}
- Total check-ins: {context.total_entries}
- Average mood: {f'{context.average_mood:.1f}/5' if context.average_mood else 'Not available'}

Use this context to provide personalized support, but don't mention these numbers unless relevant to the conversation.
"""
        base_prompt += context_info
    
    return base_prompt


async def get_chatbot_response(
    message: str,
    conversation_history: Optional[List[ChatMessage]] = None,
    context: Optional[ConversationContext] = None
) -> ChatResponse:
    """
    Get chatbot response using OpenAI API or fallback
    """
    try:
        if OPENAI_AVAILABLE and settings.OPENAI_API_KEY:
            return await get_openai_response(message, conversation_history, context)
        else:
            return get_fallback_response(message)
            
    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}")
        return ChatResponse(
            message="I apologize, but I'm having trouble processing your message right now. Please try again in a moment.",
            timestamp=datetime.utcnow(),
            suggestions=["Try again", "Contact support"]
        )


async def get_openai_response(
    message: str,
    conversation_history: Optional[List[ChatMessage]] = None,
    context: Optional[ConversationContext] = None
) -> ChatResponse:
    """Get response from OpenAI GPT model"""
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Build messages for API
        messages = [
            {"role": "system", "content": build_system_prompt(context)}
        ]
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-10:]:  # Last 10 messages
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model=settings.CHATBOT_MODEL,
            messages=messages,
            max_tokens=settings.CHATBOT_MAX_TOKENS,
            temperature=settings.CHATBOT_TEMPERATURE
        )
        
        assistant_message = response.choices[0].message.content
        
        # Generate suggestions based on context
        suggestions = generate_suggestions(message, context)
        
        return ChatResponse(
            message=assistant_message,
            timestamp=datetime.utcnow(),
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return get_fallback_response(message)


def get_fallback_response(message: str) -> ChatResponse:
    """Provide fallback responses when AI is unavailable"""
    message_lower = message.lower()
    
    # Crisis keywords
    crisis_keywords = ['suicide', 'kill myself', 'end it all', 'die', 'hurt myself']
    if any(keyword in message_lower for keyword in crisis_keywords):
        return ChatResponse(
            message=(
                "I'm very concerned about what you're sharing. Your safety is the top priority. "
                "Please reach out for immediate help:\n\n"
                "🆘 National Suicide Prevention Lifeline: 988\n"
                "💬 Crisis Text Line: Text 'HELLO' to 741741\n"
                "🏥 Go to your nearest emergency room\n\n"
                "You don't have to face this alone. Help is available 24/7."
            ),
            timestamp=datetime.utcnow(),
            suggestions=["Find local crisis resources", "Talk to someone now"]
        )
    
    # Mood-related queries
    mood_keywords = ['sad', 'depressed', 'down', 'anxious', 'worried', 'stressed']
    if any(keyword in message_lower for keyword in mood_keywords):
        return ChatResponse(
            message=(
                "I hear that you're going through a difficult time. It's important that you acknowledged these feelings. "
                "Here are some things that might help:\n\n"
                "• Take deep breaths - try the 4-7-8 technique\n"
                "• Go for a short walk or do gentle movement\n"
                "• Reach out to someone you trust\n"
                "• Practice self-compassion\n\n"
                "Remember, it's okay to not be okay. Consider talking to a mental health professional if these feelings persist."
            ),
            timestamp=datetime.utcnow(),
            suggestions=["Breathing exercises", "Find a therapist", "Track my mood"]
        )
    
    # Sleep-related
    sleep_keywords = ['sleep', 'insomnia', 'tired', 'exhausted']
    if any(keyword in message_lower for keyword in sleep_keywords):
        return ChatResponse(
            message=(
                "Sleep is crucial for mental health. Here are some tips for better sleep:\n\n"
                "• Maintain a consistent sleep schedule\n"
                "• Create a relaxing bedtime routine\n"
                "• Limit screen time before bed\n"
                "• Keep your bedroom cool and dark\n"
                "• Avoid caffeine in the afternoon\n\n"
                "If sleep problems persist, consider consulting a healthcare provider."
            ),
            timestamp=datetime.utcnow(),
            suggestions=["Sleep hygiene tips", "Track my sleep"]
        )
    
    # Default response
    return ChatResponse(
        message=(
            "Thank you for sharing. I'm here to support you. While I can provide general guidance, "
            "please remember that I'm not a substitute for professional mental health care. "
            "How are you feeling today? Is there something specific you'd like to talk about?"
        ),
        timestamp=datetime.utcnow(),
        suggestions=["Check my mood", "View my progress", "Find resources"]
    )


def generate_suggestions(message: str, context: Optional[ConversationContext]) -> List[str]:
    """Generate contextual suggestions for follow-up"""
    suggestions = []
    
    message_lower = message.lower()
    
    if 'mood' in message_lower or 'feeling' in message_lower:
        suggestions.extend(["Log today's mood", "View mood trends"])
    
    if 'sleep' in message_lower or 'tired' in message_lower:
        suggestions.append("Track sleep quality")
    
    if 'stress' in message_lower or 'anxious' in message_lower:
        suggestions.extend(["Try breathing exercise", "Stress management tips"])
    
    if 'help' in message_lower or 'support' in message_lower:
        suggestions.extend(["Find a therapist", "Crisis resources"])
    
    # Add general suggestions if not enough specific ones
    if len(suggestions) < 3:
        suggestions.extend(["View my progress", "Get daily tips", "Learn about mental health"])
    
    return suggestions[:4]  # Limit to 4 suggestions
