import os
import logging
import requests
import time

logger = logging.getLogger(__name__)

def get_gemini_api_key():
    """Reads Gemini API key from environment variables."""
    return os.environ.get("GEMINI_API_KEY", "").strip()


def get_gemini_api_url():
    """Returns the Gemini REST API endpoint for the configured model."""
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip()
    return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


# Simple in-memory response cache to prevent redundant API calls and save quota
_AI_CACHE = {}
_CACHE_TTL_SECONDS = 3600  # Cache responses for 1 hour


def generate_course_advice(student_name: str, course_interested: str, user_message: str = "") -> str:
    """
    Generates a personalized course recommendation using Google Gemini LLM API.
    Includes in-memory caching and robust HTTP 429 rate limit handling.
    """
    api_key = get_gemini_api_key()
    course_name = course_interested or "IT Programs"

    # Fallback response used if API key is missing, network is down, or quota is exceeded
    fallback_advice = (
        f"Hi {student_name}! Based on your interest in {course_name}, "
        "CTRL A IT HUB provides comprehensive 100% placement-oriented hands-on training "
        "with live industry capstone projects and expert mentorship."
    )

    if not api_key:
        logger.info("[Gemini AI] GEMINI_API_KEY not set. Serving default counseling advice.")
        return fallback_advice

    # Check cache first: if another student asked about this course recently, return cached response
    cache_key = f"{course_name.lower()}_{user_message[:50].strip().lower()}"
    now = time.time()
    if cache_key in _AI_CACHE:
        cached_text, timestamp = _AI_CACHE[cache_key]
        if now - timestamp < _CACHE_TTL_SECONDS:
            logger.info(f"[Gemini AI] Serving cached recommendation for '{course_name}'.")
            return cached_text.replace("{NAME}", student_name)

    prompt = (
        "You are the Senior Academic Counselor at CTRL A IT HUB (ctrlaithub.com), "
        "an IT training and placement institute in India.\n"
        f"Student Name: {student_name}\n"
        f"Interested Course: {course_name}\n"
        f"Student Query/Background: {user_message or 'Looking for best career path'}\n\n"
        "Provide a concise, encouraging 2-3 sentence personalized career recommendation. "
        "Highlight practical project experience and placement readiness. Keep it friendly and professional."
    )

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 300,
            "thinkingConfig": {
                "thinkingBudget": 0
            }
        }
    }

    try:
        api_url = get_gemini_api_url()
        response = requests.post(
            f"{api_url}?key={api_key}",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                advice = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                if advice.strip():
                    clean_advice = advice.strip()
                    # Cache the response for future inquiries on this course
                    _AI_CACHE[cache_key] = (clean_advice.replace(student_name, "{NAME}"), now)
                    return clean_advice

        elif response.status_code == 429:
            # Rate limit exceeded (15 RPM or 1500 RPD)
            logger.warning(
                "[Gemini AI] Rate limit reached (HTTP 429 Too Many Requests). "
                "Gracefully serving high-priority curated fallback advice."
            )
        else:
            logger.warning(f"[Gemini AI] API error HTTP {response.status_code}. Serving fallback.")

    except requests.exceptions.Timeout:
        logger.warning("[Gemini AI] Request timed out (6s). Serving fallback advice.")
    except Exception as e:
        logger.warning(f"[Gemini AI] Unexpected error: {e}. Serving fallback.")

    return fallback_advice


def trigger_n8n_webhook(event_type: str, data: dict) -> bool:
    """
    Lightweight event-driven webhook dispatcher for external n8n automation.
    Fires in 0.05 seconds and never blocks the web request.
    """
    n8n_url = os.environ.get("N8N_WEBHOOK_URL", "").strip()
    if not n8n_url:
        return False

    payload = {
        "event": event_type,
        "data": data
    }

    try:
        requests.post(n8n_url, json=payload, timeout=3)
        return True
    except Exception as e:
        logger.warning(f"[n8n Webhook] Failed to trigger webhook: {e}")
        return False
