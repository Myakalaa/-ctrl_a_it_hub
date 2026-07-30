# Celery Background Worker Deployment

To ensure that your background tasks (Emails and WhatsApp messages) always run on your live VPS, you need to set up Celery as a Linux Systemd service. This ensures that Celery starts automatically if the server reboots and automatically restarts if it crashes.

### Step 1: Copy the Service File
Copy the `celery.service` file from this folder into the Linux systemd directory:
```bash
sudo cp /var/www/-ctrl_a_it_hub/deploy/celery.service /etc/systemd/system/
```

### Step 2: Reload Systemd
Tell Linux to read the new file you just copied:
```bash
sudo systemctl daemon-reload
```

### Step 3: Enable and Start Celery
Run these two commands to activate Celery permanently:
```bash
sudo systemctl enable celery.service
sudo systemctl start celery.service
```

### Troubleshooting
If you ever need to check if Celery is running properly or read its logs, run this:
```bash
sudo systemctl status celery.service
```

---

# Automated Nightly Backups (CRON)

To ensure your database is never lost, we have created a custom script that zips your database and securely emails it to you. You should configure the Linux server to run this every single night automatically using a CRON job.

### Step 1: Open the CRON Editor
On your VPS terminal, type:
```bash
crontab -e
```

### Step 2: Paste the Schedule Command
Scroll to the very bottom of the file and paste this exact line:
```bash
0 2 * * * /var/www/-ctrl_a_it_hub/venv/bin/python /var/www/-ctrl_a_it_hub/manage.py backup_database
```
*(This tells the server to run the script at exactly 2:00 AM every night).*

### Step 3: Save and Exit
If it opened in `nano`, press `CTRL+X`, then `Y`, then `Enter`. The server will now email you a fresh backup of your database every single night!
