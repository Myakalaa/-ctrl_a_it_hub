import os
import logging
import requests
import time
from celery import shared_task
from .whatsapp import send_whatsapp_alert, _send_meta_whatsapp, _sanitize_phone

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════
# TASK 1: Student Enquiry WhatsApp Notification
# Triggered when a student submits an enquiry form (home or contact page).
# Sends a greeting to the student AND a lead alert to the admin.
# ═══════════════════════════════════════════════════════════════════════
@shared_task(
    name="portal.tasks.send_whatsapp_notification_task",
    max_retries=3,
    default_retry_delay=30,
    autoretry_for=(Exception,)
)
def send_whatsapp_notification_task(to_phone, student_name, course_name, enquiry_type='general'):
    """
    Asynchronous Celery task: sends WhatsApp confirmation to student
    and a new lead alert to the admin using the Official Meta Cloud API.
    Automatically retries up to 3 times if the API call fails.
    """
    logger.info(f"[Task] WhatsApp notification started for '{student_name}' ({to_phone})")
    success = send_whatsapp_alert(
        to_phone=to_phone,
        student_name=student_name,
        course_name=course_name,
        enquiry_type=enquiry_type
    )
    if success:
        logger.info(f"[Task] ✓ WhatsApp notification completed for '{student_name}'.")
    else:
        logger.error(f"[Task] ✗ WhatsApp notification failed for '{student_name}'.")
    return success


# ═══════════════════════════════════════════════════════════════════════
# TASK 2: HR Job Application WhatsApp Alert
# Triggered when a candidate submits a job application via the careers page.
# Sends an internal alert to the HR admin's WhatsApp number.
# Uses the Official Meta Cloud API (same credentials as Task 1).
# ═══════════════════════════════════════════════════════════════════════
@shared_task(
    name="portal.tasks.send_hr_notification_task",
    max_retries=3,
    default_retry_delay=30,
    autoretry_for=(Exception,)
)
def send_hr_notification_task(name, phone, job_title):
    """
    Asynchronous Celery task: sends HR coordinator a WhatsApp alert
    about a new job applicant using the Official Meta Cloud API.
    """
    access_token = os.environ.get('META_WHATSAPP_TOKEN')
    phone_number_id = os.environ.get('META_PHONE_NUMBER_ID')
    admin_phone = os.environ.get('ADMIN_WHATSAPP_NUMBER', '919989985152')

    if not access_token or not phone_number_id:
        logger.warning(
            "[Task] HR WhatsApp alert skipped — "
            "META_WHATSAPP_TOKEN or META_PHONE_NUMBER_ID not configured."
        )
        return False

    hr_message = (
        f"💼 *New Job Applicant Alert — CTRL A IT HUB*\n\n"
        f"📋 Position: {job_title}\n"
        f"👤 Candidate: {name}\n"
        f"📞 Contact: {phone}\n\n"
        f"Please log in to the Admin Dashboard to review their "
        f"qualifications and download their resume.\n"
        f"🌐 https://ctrlaithub.com/admin/"
    )

    logger.info(f"[Task] Sending HR WhatsApp alert for applicant '{name}'...")
    success = _send_meta_whatsapp(
        access_token=access_token,
        phone_number_id=phone_number_id,
        to_phone=admin_phone,
        message_body=hr_message
    )

    if success:
        logger.info(f"[Task] ✓ HR WhatsApp alert sent for applicant '{name}'.")
    else:
        logger.error(f"[Task] ✗ HR WhatsApp alert failed for applicant '{name}'.")
    return success


# ═══════════════════════════════════════════════════════════════════════
# TASK 3: BPO Enquiry Email Alert
# Triggered when a student submits an enquiry (home or contact page).
# Sends a formatted email notification to the BPO support team inbox.
# ═══════════════════════════════════════════════════════════════════════
@shared_task(
    name="portal.tasks.send_bpo_enquiry_email_task",
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,)
)
def send_bpo_enquiry_email_task(name, email, phone, enquiry_type, message):
    """
    Asynchronous Celery task: emails student enquiry details to the BPO team.
    Automatically retries up to 3 times with a 60-second delay if Gmail fails.
    """
    from django.core.mail import send_mail

    subject = f"🔔 New Student Enquiry Alert ({enquiry_type.upper()})"
    body = (
        f"Hello BPO Team,\n\n"
        f"A student has submitted a new enquiry through the CTRL A IT HUB portal.\n\n"
        f"{'='*50}\n"
        f"ENQUIRY DETAILS\n"
        f"{'='*50}\n"
        f"Name          : {name}\n"
        f"Email         : {email}\n"
        f"Phone         : {phone}\n"
        f"Enquiry Type  : {enquiry_type.title()}\n\n"
        f"Message:\n{message}\n\n"
        f"{'='*50}\n"
        f"Please log in to the Admin Dashboard to mark this enquiry as Resolved.\n"
        f"Admin URL: https://ctrlaithub.com/admin/portal/enquiry/\n\n"
        f"— CTRL A IT HUB Automated Notification System"
    )

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
            recipient_list=['ctrlaithubempoweringtechnology@gmail.com'],
            fail_silently=False,
        )
        logger.info(f"[Task] ✓ BPO enquiry email sent for '{name}'.")
        return True
    except Exception as e:
        logger.error(f"[Task] ✗ BPO enquiry email failed for '{name}': {e}")
        raise  # Re-raise so Celery can autoretry


# ═══════════════════════════════════════════════════════════════════════
# TASK 4: HR Candidate Application Email (with Resume PDF Attachment)
# Triggered when a job application is submitted via the careers page.
# Sends a structured email with the candidate's full details and resume
# PDF attachment directly to the HR team inbox.
# ═══════════════════════════════════════════════════════════════════════
@shared_task(
    name="portal.tasks.send_hr_candidate_email_task",
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,)
)
def send_hr_candidate_email_task(
    name, email, phone, job_title,
    qualification, experience,
    resume_url=None, resume_path=None
):
    """
    Asynchronous Celery task: emails full candidate application details
    to the HR team with their resume attached as a PDF file.
    Automatically retries up to 3 times with a 60-second delay if Gmail fails.
    """
    from django.core.mail import EmailMessage
    from django.conf import settings

    subject = f"💼 New Job Application Received: {job_title}"
    body = (
        f"Hello HR Team,\n\n"
        f"A candidate has applied for a position through the CTRL A IT HUB Careers portal.\n\n"
        f"{'='*50}\n"
        f"CANDIDATE DETAILS\n"
        f"{'='*50}\n"
        f"Position       : {job_title}\n"
        f"Name           : {name}\n"
        f"Email          : {email}\n"
        f"Phone          : {phone}\n"
        f"Qualification  : {qualification}\n"
        f"Experience     : {experience}\n"
    )

    if resume_url:
        body += f"Resume Link    : {resume_url}\n"

    body += (
        f"\n{'='*50}\n"
        f"Their resume PDF is attached to this email for download.\n"
        f"You can also review this application on the Admin Dashboard:\n"
        f"Admin URL: https://ctrlaithub.com/admin/portal/jobapplication/\n\n"
        f"— CTRL A IT HUB Automated Notification System"
    )

    try:
        email_msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['hr.ctrlaithub@gmail.com', 'amyakala01@gmail.com']
        )

        # Attach the actual resume PDF file if it exists on the server disk
        if resume_path:
            full_path = os.path.join(settings.MEDIA_ROOT, resume_path)
            if os.path.exists(full_path):
                email_msg.attach_file(full_path)
                logger.info(f"[Task] Resume attached from path: {full_path}")
            else:
                logger.warning(f"[Task] Resume file not found on disk: {full_path}")

        email_msg.send(fail_silently=False)
        logger.info(f"[Task] ✓ HR candidate email sent for '{name}' applying for '{job_title}'.")
        return True

    except Exception as e:
        logger.error(f"[Task] ✗ HR candidate email failed for '{name}': {e}")
        raise  # Re-raise so Celery can autoretry
