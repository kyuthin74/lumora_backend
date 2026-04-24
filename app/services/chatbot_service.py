from typing import List, Optional, Dict, Any
from app.models.chatbot import ChatMessage, ChatResponse, ConversationContext
from app.config import settings
from datetime import datetime
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

_gemini_client = None


def get_gemini_client():
    """Create and cache the Gemini client only when first used."""
    global _gemini_client
    if _gemini_client is not None:
        return _gemini_client

    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not configured; chatbot AI features are disabled")
        return None

    try:
        _gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return _gemini_client
    except Exception as exc:
        logger.error("Failed to initialize Gemini client: %s", exc)
        return None


def build_system_prompt(context: Optional[ConversationContext] = None) -> str:
    """Build system prompt with user context"""
    base_prompt = """You are Lumora, a compassionate mental health support assistant. Keep responses to one or two sentences. Be warm, brief, and natural like texting a friend.

Only answer questions about mental health, emotions, and well-being. For other topics (math, history, science, etc.), politely decline and redirect to mental health support.

Listen, validate feelings, suggest simple coping strategies. Never diagnose or prescribe.
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


def init_gemini_chat(history: Optional[List[Dict[str, str]]] = None):
    """Initialize Gemini chat session with context"""
    gemini_client = get_gemini_client()
    if gemini_client is None:
        return None

    # Initialize chat with system prompt
    system_prompt = build_system_prompt()
    
    # Create chat session
    chat = gemini_client.chats.create(
        model=settings.GEMINI_MODEL,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
            top_p=0.9,
            top_k=40,
            seed=50
        ),
        history=history
    )

    return chat

def message_to_dict(message):
        """Converts a content message object to a dictionary, handling function calls and responses."""
        parts_data = []
        # logging.info(f"Converting message to dict: {message}")
        for part in message.parts:
            part_data = {}
            if part.text is not None:
                if message.role == 'user':
                    part_data['text'] = part.text.split("User Prompt:", 1)[-1].strip()
                else:
                    part_data['text'] = part.text
            parts_data.append(part_data)
        return {'role': message.role, 'parts': parts_data}
    
def dict_to_message(data):
    """Converts a dictionary back to a content message object, handling function calls and responses."""
    parts = []

    for part_data in data['parts']:
        if 'text' in part_data:
            parts.append(types.Part(text=part_data['text']))
        else:
            parts.append(types.Part())  # Handle cases with no specific content

    return types.Content(role=data['role'], parts=parts)

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
