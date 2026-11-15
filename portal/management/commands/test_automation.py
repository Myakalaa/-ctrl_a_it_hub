import os
from django.core.management.base import BaseCommand
from portal.gemini_service import generate_course_advice, trigger_n8n_webhook
from portal.whatsapp import _sanitize_phone


class Command(BaseCommand):
    help = "Tests Gemini AI, WhatsApp API, and n8n Webhook connectivity"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("\n=== CTRL A IT HUB INTEGRATION STATUS CHECK ===\n"))

        # 1. TEST GEMINI API
        self.stdout.write("1. Testing Google Gemini API...")
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip()

        if not api_key:
            self.stdout.write(self.style.WARNING("   [!] GEMINI_API_KEY is not set in environment."))
        else:
            self.stdout.write(f"   Model: {model}")
            try:
                advice = generate_course_advice(
                    student_name="Test Student",
                    course_interested="Python Full Stack",
                    user_message="Looking for career change"
                )
                self.stdout.write(self.style.SUCCESS("   [OK] Gemini API Connected Successfully!"))
                self.stdout.write(f"   Sample Output: \"{advice[:120]}...\"\n")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   [FAIL] Gemini Error: {e}\n"))

        # 2. TEST WHATSAPP API CONFIGURATION
        self.stdout.write("2. Testing WhatsApp API Configuration...")
        wa_token = os.environ.get("META_WHATSAPP_TOKEN", "").strip()
        wa_phone_id = os.environ.get("META_PHONE_NUMBER_ID", "").strip()
        admin_152 = os.environ.get("ADMIN_NUMBER_152", "919989985152").strip()

        self.stdout.write(f"   Lead Receiver (ADMIN_NUMBER_152): +{_sanitize_phone(admin_152)}")

        if not wa_token or not wa_phone_id:
            self.stdout.write(self.style.WARNING("   [!] META_WHATSAPP_TOKEN or META_PHONE_NUMBER_ID not set."))
            self.stdout.write("       (Add META_WHATSAPP_TOKEN & META_PHONE_NUMBER_ID to .env when ready to send live WhatsApp)")
        else:
            self.stdout.write(self.style.SUCCESS(f"   [OK] Meta Phone Number ID: {wa_phone_id}"))
            self.stdout.write(self.style.SUCCESS("   [OK] Meta Token is present.\n"))

        # 3. TEST N8N WEBHOOK
        self.stdout.write("\n3. Testing n8n Webhook Dispatcher...")
        n8n_url = os.environ.get("N8N_WEBHOOK_URL", "").strip()
        if not n8n_url:
            self.stdout.write(self.style.WARNING("   [!] N8N_WEBHOOK_URL not set (Optional)."))
        else:
            self.stdout.write(f"   Webhook URL: {n8n_url}")
            ok = trigger_n8n_webhook("test_ping", {"message": "Test ping from CTRL A IT HUB"})
            if ok:
                self.stdout.write(self.style.SUCCESS("   [OK] n8n Webhook dispatched successfully!"))
            else:
                self.stdout.write(self.style.ERROR("   [FAIL] n8n Webhook failed to respond."))

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== STATUS CHECK COMPLETE ===\n"))
