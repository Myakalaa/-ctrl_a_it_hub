import os
import time
import requests
import logging

logger = logging.getLogger(__name__)

# ===== CONFIGURATION =====
MAX_RETRIES = 3       # Retry failed API calls up to 3 times
RETRY_DELAY = 2       # Start with 2 seconds, then double (exponential backoff)
CONNECT_TIMEOUT = 5   # Seconds to wait for Meta server to respond
READ_TIMEOUT = 10     # Seconds to wait for Meta API response body

# Official Meta WhatsApp Cloud API Base URL
META_API_VERSION = os.environ.get('META_API_VERSION', 'v19.0')


def _sanitize_phone(phone: str) -> str:
    """
    Cleans a phone number to pure digits for Meta API compatibility.
    Meta requires full international format WITHOUT + sign.
    Examples:
        +91 91333 91401  ->  919133391401
        09133391401      ->  9133391401
        91 99899 85152   ->  919989985152
    """
    digits = ''.join(filter(str.isdigit, str(phone)))
    # Remove leading zero (Indian local format)
    if digits.startswith('0'):
        digits = digits[1:]
    return digits


def _send_meta_whatsapp(
    access_token: str,
    phone_number_id: str,
    to_phone: str,
    message_body: str
) -> bool:
    """
    Sends a single WhatsApp message using the Official Meta Cloud API.
    Uses retry logic with exponential backoff for reliability.

    Official Meta API Endpoint:
        POST https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages

    Required Environment Variables:
        META_WHATSAPP_TOKEN    -> Your permanent access token from Meta Developer Portal
        META_PHONE_NUMBER_ID   -> Your WhatsApp Phone Number ID (NOT the actual phone number)

    Returns True on success, False after all retries fail.
    """
    clean_phone = _sanitize_phone(to_phone)

    # Official Meta Cloud API endpoint
    url = f"https://graph.facebook.com/{META_API_VERSION}/{phone_number_id}/messages"

    # Official Meta API requires Bearer Token in Authorization header
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Official Meta API payload structure for free-text messages
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": clean_phone,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message_body
        }
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
            )

            if response.status_code == 200:
                resp_data = response.json()
                msg_id = resp_data.get('messages', [{}])[0].get('id', 'unknown')
                logger.info(
                    f"[Meta WhatsApp] ✓ Message sent to {clean_phone} "
                    f"(attempt {attempt}, message_id={msg_id})"
                )
                return True
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', response.text[:200])
                logger.warning(
                    f"[Meta WhatsApp] ✗ Attempt {attempt}/{MAX_RETRIES} failed for {clean_phone}. "
                    f"HTTP {response.status_code}: {error_msg}"
                )

        except requests.exceptions.ConnectTimeout:
            logger.warning(
                f"[Meta WhatsApp] ✗ Attempt {attempt}/{MAX_RETRIES} "
                f"— Connection timeout for {clean_phone}."
            )
        except requests.exceptions.ReadTimeout:
            logger.warning(
                f"[Meta WhatsApp] ✗ Attempt {attempt}/{MAX_RETRIES} "
                f"— Read timeout for {clean_phone}."
            )
        except requests.exceptions.ConnectionError:
            logger.warning(
                f"[Meta WhatsApp] ✗ Attempt {attempt}/{MAX_RETRIES} "
                f"— Network connection error for {clean_phone}."
            )
        except Exception as e:
            logger.error(
                f"[Meta WhatsApp] ✗ Attempt {attempt}/{MAX_RETRIES} "
                f"— Unexpected error for {clean_phone}: {e}"
            )

        # Exponential backoff before next retry: 2s, 4s, 8s
        if attempt < MAX_RETRIES:
            wait_seconds = RETRY_DELAY * (2 ** (attempt - 1))
            logger.info(f"[Meta WhatsApp] Waiting {wait_seconds}s before retry...")
            time.sleep(wait_seconds)

    logger.error(
        f"[Meta WhatsApp] ✗ All {MAX_RETRIES} attempts failed for {clean_phone}. Giving up."
    )
    return False


def send_whatsapp_alert(to_phone: str, student_name: str, course_name: str, enquiry_type: str = 'general') -> bool:
    """
    Main function: Sends automated WhatsApp alerts using the Official Meta Cloud API.

    Sends messages to:
        1. The student — a confirmation greeting after their enquiry.
        2. ALL THREE admin numbers (401, 402, 152) — a new lead alert so
           no coordinator ever misses a lead regardless of enquiry type.

    Required Server Environment Variables:
        META_WHATSAPP_TOKEN     -> Permanent Access Token from Meta Developer Portal
        META_PHONE_NUMBER_ID    -> WhatsApp Business Phone Number ID from Meta Developer Portal
        ADMIN_NUMBER_401        -> Admissions & Courses   (defaults to 919133391401)
        ADMIN_NUMBER_402        -> Corporate & Placements (defaults to 919133391402)
        ADMIN_NUMBER_152        -> General Enquiry        (defaults to 919989985152)
    """
    access_token = os.environ.get('META_WHATSAPP_TOKEN')
    phone_number_id = os.environ.get('META_PHONE_NUMBER_ID')

    # All three admin numbers always receive every lead alert
    admin_numbers = [
        os.environ.get('ADMIN_NUMBER_401', '919133391401'),   # Admissions & Courses
        os.environ.get('ADMIN_NUMBER_402', '919133391402'),   # Corporate & Placements
        os.environ.get('ADMIN_NUMBER_152', '919989985152'),   # General Enquiry
    ]

    # Safety check: skip silently if credentials are not configured
    if not access_token or not phone_number_id:
        logger.warning(
            f"[Meta WhatsApp] Skipping alert for '{student_name}' — "
            "META_WHATSAPP_TOKEN or META_PHONE_NUMBER_ID not set in environment variables. "
            "Please configure these in your hosting provider's dashboard."
        )
        return False

    # ─── MESSAGE 1: Student Confirmation ───────────────────────────────────────
    student_message = (
        f"Hello {student_name},\n\n"
        f"Thank you for contacting *CTRL A IT HUB*! \u2705\n\n"
        f"We have received your enquiry regarding our *'{course_name}'* program. "
        f"Our counseling expert will reach out to you within 24 hours.\n\n"
        f"Best regards,\n"
        f"*CTRL A IT HUB Team*\n"
        f"\ud83d\udcde +91 91333 91401\n"
        f"\ud83c\udf10 https://ctrlaithub.com"
    )

    # ─── MESSAGE 2: Admin New Lead Alert (sent to ALL 3 numbers) ───────────────
    admin_message = (
        f"\ud83d\udd14 *New Lead Alert ({enquiry_type.upper()}) \u2014 CTRL A IT HUB*\n\n"
        f"\ud83d\udc64 Name      : {student_name}\n"
        f"\ud83d\udcde Phone     : {to_phone}\n"
        f"\ud83d\udcda Course    : {course_name}\n"
        f"\ud83d\udccc Type      : {enquiry_type.title()} Enquiry\n\n"
        f"Please follow up with this lead as soon as possible.\n"
        f"\ud83c\udf10 https://ctrlaithub.com/admin/"
    )

    # Send greeting to the student
    student_result = _send_meta_whatsapp(
        access_token, phone_number_id, to_phone, student_message
    )

    # Send lead alert to ALL THREE admin numbers
    admin_results = []
    for admin_phone in admin_numbers:
        result = _send_meta_whatsapp(
            access_token, phone_number_id, admin_phone, admin_message
        )
        admin_results.append(result)
        logger.info(
            f"[Meta WhatsApp] Admin alert to {admin_phone}: "
            f"{'✓ Sent' if result else '✗ Failed'}"
        )

    # Return True only if student message AND at least one admin was notified
    return student_result and any(admin_results)

