from datetime import datetime, timedelta
from typing import List, Dict, Any
import json


def format_date(date: datetime, format: str = "%Y-%m-%d") -> str:
    """Format datetime to string"""
    return date.strftime(format)


def format_datetime(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string with time"""
    return dt.strftime(format)


def get_date_range(days: int) -> tuple[datetime, datetime]:
    """Get date range from today going back specified days"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def calculate_average(values: List[float]) -> float:
    """Calculate average of a list of values"""
    if not values:
        return 0.0
    return sum(values) / len(values)


def map_mood_to_numeric(mood: str) -> int:
    """Map mood level string to numeric value"""
    mood_map = {
        'very_poor': 1,
        'poor': 2,
        'fair': 3,
        'good': 4,
        'excellent': 5
    }
    return mood_map.get(mood.lower(), 3)


def map_sleep_quality_to_numeric(quality: str) -> int:
    """Map sleep quality string to numeric value"""
    quality_map = {
        'very_poor': 1,
        'poor': 2,
        'fair': 3,
        'good': 4,
        'excellent': 5
    }
    return quality_map.get(quality.lower(), 3)


def determine_risk_level(risk_score: float) -> str:
    """Determine risk level from risk score"""
    if risk_score < 0.3:
        return "Low"
    elif risk_score < 0.7:
        return "Medium"
    else:
        return "High"


def generate_risk_recommendation(risk_level: str, risk_score: float) -> str:
    """Generate recommendation based on risk level"""
    if risk_level == "Low":
        return (
            "Your mental health indicators are positive. Continue maintaining "
            "healthy habits like regular sleep, physical activity, and social connections."
        )
    elif risk_level == "Medium":
        return (
            "Your mental health shows some concerning patterns. Consider speaking "
            "with a mental health professional and focus on stress management, "
            "better sleep hygiene, and regular exercise."
        )
    else:
        return (
            "Your mental health indicators suggest you may be at high risk. "
            "We strongly recommend consulting with a mental health professional immediately. "
            "Contact crisis support if you're having thoughts of self-harm: "
            "National Suicide Prevention Lifeline: 988"
        )


def format_alert_message(risk_level: str, risk_score: float, user_name: str) -> str:
    """Format alert message for notifications"""
    return (
        f"Mental Health Alert for {user_name}\n\n"
        f"Risk Level: {risk_level}\n"
        f"Risk Score: {risk_score:.2f}\n\n"
        f"Recommendation: {generate_risk_recommendation(risk_level, risk_score)}"
    )


def paginate_results(items: List[Any], page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """Paginate a list of items"""
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        'items': items[start:end],
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    }


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON string"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(obj: Any, default: Any = "{}") -> str:
    """Safely dump object to JSON string"""
    try:
        return json.dumps(obj)
    except (TypeError, ValueError):
        return default
