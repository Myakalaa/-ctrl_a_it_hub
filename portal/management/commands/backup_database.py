import os
import shutil
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates a backup of the SQLite database and emails it to the admin'

    def handle(self, *args, **kwargs):
        # 1. Define paths
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
        date_str = datetime.now().strftime('%Y-%m-%d')
        backup_filename = f'backup_{date_str}.sqlite3'
        backup_path = os.path.join(settings.BASE_DIR, backup_filename)

        if not os.path.exists(db_path):
            self.stdout.write(self.style.ERROR(f'Database file not found at {db_path}'))
            return

        # 2. Copy the database securely
        try:
            shutil.copy2(db_path, backup_path)
            self.stdout.write(self.style.SUCCESS(f'Successfully created backup file: {backup_filename}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to copy database: {e}'))
            return

        # 3. Email the backup
        admin_email = settings.DEFAULT_FROM_EMAIL
        subject = f'🛡️ Nightly Database Backup - CTRL A IT HUB ({date_str})'
        body = (
            f"Hello Admin,\n\n"
            f"Please find attached your automated nightly database backup for {date_str}.\n\n"
            f"This file contains all your current Enquiries, Job Applications, Courses, and User Accounts. "
            f"Keep this email safe in your archives.\n\n"
            f"— CTRL A IT HUB Automated Backup System"
        )

        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email],
            )
            email.attach_file(backup_path)
            email.send(fail_silently=False)
            self.stdout.write(self.style.SUCCESS(f'Successfully emailed backup to {admin_email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {e}'))

        # 4. Clean up the temporary backup file from the server
        if os.path.exists(backup_path):
            os.remove(backup_path)
            self.stdout.write(self.style.SUCCESS('Cleaned up temporary backup file from server disk.'))
