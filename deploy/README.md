# 🚀 CTRL A IT HUB - Professional Server Deployment Guide

Complete step-by-step instructions to deploy **CTRL A IT HUB** on a Linux Cloud Server / VPS (Ubuntu 22.04 / 24.04 LTS or Debian).

---

## 📋 Server Stack Architecture
- **Web Server & Reverse Proxy:** Nginx (Port 80 / 443 with HTTPS SSL)
- **WSGI Application Server:** Gunicorn (running via systemd socket `/run/gunicorn.sock`)
- **Framework & Runtime:** Django 5.1 / Python 3.12
- **Background Worker & Broker:** Celery + Redis (for asynchronous emails & WhatsApp alerts)
- **SSL Certificate:** Free automated Let's Encrypt SSL via Certbot
- **Project Directory:** `/var/www/ctrl_a_it_hub`

---

## 🛠️ Step 1: Prepare the Server Packages

SSH into your cloud server as root:
```bash
ssh root@YOUR_SERVER_IP
```

Update packages and install all dependencies:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential \
                    libpq-dev nginx redis-server git curl certbot python3-certbot-nginx
```

Enable and start Redis:
```bash
sudo systemctl enable --now redis-server
```

---

## 📂 Step 2: Clone & Set Up the Project

Create the web directory and clone your repository:
```bash
sudo mkdir -p /var/www/ctrl_a_it_hub
sudo chown -R $USER:$USER /var/www/ctrl_a_it_hub
git clone <YOUR_GIT_REPO_URL> /var/www/ctrl_a_it_hub
cd /var/www/ctrl_a_it_hub
```

Create and activate Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

---

## ⚙️ Step 3: Configure Environment Variables

Create your production `.env` from the template:
```bash
cp .env.example .env
nano .env
```
Ensure you configure:
- `DEBUG=False`
- `SECRET_KEY=<generate a strong secret key>`
- `ALLOWED_HOSTS=ctrlaithub.com,www.ctrlaithub.com,YOUR_SERVER_IP`
- `CSRF_TRUSTED_ORIGINS=https://ctrlaithub.com,https://www.ctrlaithub.com`
- `EMAIL_HOST_USER` & `EMAIL_HOST_PASSWORD` (Gmail App password)
- Save with `CTRL+O`, `Enter`, and exit with `CTRL+X`.

---

## 🗄️ Step 4: Run Migrations, Seed Data & Collect Static

While inside the virtual environment (`source venv/bin/activate`):
```bash
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --no-input
```

---

## 🔧 Step 5: Install Systemd Services (Gunicorn & Celery)

Copy the pre-configured service unit files:
```bash
sudo cp deploy/gunicorn.service /etc/systemd/system/
sudo cp deploy/celery.service /etc/systemd/system/
```

Reload systemd daemon, enable, and start the services:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn.service
sudo systemctl enable --now celery.service
```

Verify service status:
```bash
sudo systemctl status gunicorn.service
sudo systemctl status celery.service
```

---

## 🌐 Step 6: Configure Nginx & Firewall

Copy the Nginx site configuration:
```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/ctrla_hub
sudo ln -sf /etc/nginx/sites-available/ctrla_hub /etc/nginx/sites-enabled/ctrla_hub
sudo rm -f /etc/nginx/sites-enabled/default
```

Test Nginx syntax and restart:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

Set correct folder permissions so Nginx can read static and write uploaded media:
```bash
sudo chown -R www-data:www-data /var/www/ctrl_a_it_hub
sudo chmod -R 775 /var/www/ctrl_a_it_hub/media /var/www/ctrl_a_it_hub/staticfiles
```

Configure UFW firewall:
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable
```

---

## 🔒 Step 7: Install Free SSL Certificate (HTTPS)

Make sure your domain (`ctrlaithub.com` and `www.ctrlaithub.com`) has **DNS A records** pointing to `YOUR_SERVER_IP`. Then run:
```bash
sudo certbot --nginx -d ctrlaithub.com -d www.ctrlaithub.com
```
Follow the prompt to provide your email. Certbot will automatically issue and configure the HTTPS certificate and auto-renewal.

---

## 🔄 Updating Code in Future (Zero Downtime)

Whenever you make updates and push to Git, run on the server:
```bash
cd /var/www/ctrl_a_it_hub
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
sudo systemctl restart gunicorn
sudo systemctl restart celery
```

---

## 🛡️ Automated Nightly Database Backups

Set up automated nightly backups:
```bash
crontab -e
```
Add this line at the bottom:
```bash
0 2 * * * /var/www/ctrl_a_it_hub/venv/bin/python /var/www/ctrl_a_it_hub/manage.py backup_database
```
Save and exit. Your SQLite database backup will be emailed to your admin email every morning at 2:00 AM!

