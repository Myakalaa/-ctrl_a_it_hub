# 🚀 CTRL A IT HUB — Enterprise Academic & Corporate Training Platform

![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![Django Version](https://img.shields.io/badge/django-5.1.4-green.svg)
![Database](https://img.shields.io/badge/database-PostgreSQL%20%7C%20SQLite-blue.svg)
![Security](https://img.shields.io/badge/security-OWASP%20Level%203-orange.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

**CTRL A IT HUB** is a production-grade, multi-tenant enterprise web application engineered for IT skill development, corporate software incubation, and academic project training. Built with **Django, PostgreSQL, Gunicorn, WhiteNoise, and modern UI/UX design systems**, the platform seamlessly interlinks Administrators, HR Managers, Executive Directors, Students, and Corporate Partners.

---

## 🌟 Key Architectural Features

### 🏛️ 1. Osmania University Style Leadership Desk
* **Executive Showcase**: Inspired by top university executive portals (e.g., Osmania University Vice-Chancellor Desk).
* **Dual Managing Director Cards**: Side-by-side executive cards featuring top-center passport framing (`director1.jpg` & `director2.jpg`), gold governance badges, and official logo watermark overlays (`logo.png`).

### 🔐 2. Multi-Tenant Role-Based Access Control (RBAC)
* **Master Admin (Centralized)**: Full system configuration, database management, and permission delegation.
* **HR Operations (Decentralized)**: Student onboarding, roll number assignments, enquiry resolution, attendance tracking, and candidate resume screening (`JobApplication`).
* **Executive Directors**: High-level governance, institutional vision, corporate client partnerships (JLL, KPMG, Capgemini, Mahindra), and analytics reporting.
* **Student Portal (Client Isolation)**: Secure student dashboard to access course materials, submit assignments, track attendance, and view online-verified **Certificates** (`CTA-2026-XXXX`).

### 🛡️ 3. OWASP Level-3 Security & Anti-Caching Engine
* **`NoCacheMiddleware`**: Custom Django middleware sending HTTP headers (`Cache-Control: no-cache, no-store, must-revalidate`) preventing unauthorized browser back-button history viewing after logout.
* **Anti-BFcache Event Listener**: Front-end `pageshow` listener forcing instant re-authentication if a logged-out user clicks the browser Back Arrow (←).
* **Session Flush**: Complete session token destruction upon logout (`request.session.flush()`).

### 🎨 4. Modern Responsive Design & Aesthetics
* **Theme System**: Dynamic Light and Dark Mode toggle with root CSS custom tokens.
* **Interactive Vision Wheel**: Central hub logo with 8 orbiting interactive bubbles animating on hover/scroll.
* **Full-Width Edge-to-Edge Slider**: Gallery slider with `object-fit: cover` and automatic image alignment for all future Django Admin uploads.
* **Glassmorphism Modals**: Frosted-glass job application popups with live AJAX response feedback.

### 💬 5. Outreach & Communication Engine
* **WhatsApp Router**: Floating multi-department WhatsApp widget routing enquiries directly to Admissions (`+91 91333 91401`), Placements (`+91 91333 91402`), and General Support (`+91 99899 85152`).
* **Async Email Engine**: Gmail SMTP configuration with Celery/Redis background task queues for non-blocking email dispatch.

---

## 🏗️ System Architecture

```
                       ┌──────────────────────────────┐
                       │   Master Centralized Admin   │
                       │   (Full System Control)      │
                       └──────────────┬───────────────┘
                                      │
           ┌──────────────────────────┴──────────────────────────┐
           ▼                                                     ▼
┌───────────────────────┐                             ┌───────────────────────┐
│  HR Operations Group  │                             │ Executive Board Group │
│  (Student Onboarding, │                             │  (Governance Desk &   │
│ Enquiries, Attendance)│                             │  Analytics Reporting) │
└──────────┬────────────┘                             └───────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Students as Clients / End-Users                       │
│        (Access Enrolled Course, Download Materials, View Certificate)       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3.12 / Django 5.1.4 |
| **Database** | PostgreSQL (Production) / SQLite3 (Development) |
| **Web Server / WSGI** | Gunicorn (Multithreaded WSGI) / Nginx Reverse Proxy |
| **Static Asset Engine** | WhiteNoise (`CompressedManifestStaticFilesStorage`) |
| **Task Queue** | Celery + Redis (Asynchronous Jobs) |
| **Frontend** | HTML5, Vanilla CSS3 (Custom Design System), JavaScript ES6+ |
| **Security** | Custom Anti-Caching Middleware, CSRF, SSL/HSTS, OWASP Guidelines |

---

## 📂 Project Structure

```
CTRL A IT HUB/
├── build.sh                  # Automated PaaS/Cloud Build Script
├── render.yaml               # Cloud Deployment Infrastructure Manifest
├── requirements.txt          # Production Python Dependencies
├── manage.py                 # Django Command-Line Utility
├── ctrla_hub/                # Main Project Configuration
│   ├── settings.py           # Production & Environment Settings
│   ├── urls.py               # Root URL Routing
│   ├── wsgi.py               # WSGI Application Server Entry
│   └── celery.py             # Celery Task Queue Setup
├── portal/                   # Core Business Application
│   ├── admin.py              # Custom Admin Portal Registration
│   ├── middleware.py         # NoCache Security Middleware
│   ├── models.py             # Database Schemas (Course, Student, Enquiry, etc.)
│   ├── views.py              # Business Logic & Views
│   ├── urls.py               # Portal URL Patterns
│   └── tasks.py              # Asynchronous Celery Tasks
├── static/                   # Static Assets (CSS, JS, Images, Logos)
│   └── images/               # Directors Photos, Logos, Gallery Images
├── staticfiles/              # Post-Processed Production Static Assets
└── templates/                # HTML5 Templates
    ├── base.html             # Main Site Master Layout
    ├── home.html             # Home Page with Vision Wheel & Gallery
    ├── about.html            # Osmania Style Board of Directors Showcase
    └── portal/               # Student & Admin Dashboards
```

---

## ⚙️ Local Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Myakalaa/-ctrl_a_it_hub.git
   cd -ctrl_a_it_hub
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install Production Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables (`.env`)**:
   Create a `.env` file in the project root:
   ```env
   DEBUG=True
   SECRET_KEY=django-insecure-key-for-local-dev
   ALLOWED_HOSTS=*
   ```

5. **Run Migrations & Start Development Server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000/`.

---

## 🚀 Production VPS Deployment (Gunicorn + Nginx + SSL)

For full deployment instructions on Ubuntu VPS / CloudExter using **Nginx, Gunicorn, PostgreSQL, and Certbot SSL**, refer to the built-in deployment pipeline guide.

1. **Collect Static Assets**:
   ```bash
   python manage.py collectstatic --no-input
   ```
2. **Execute Production Script**:
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

---

## 🛡️ Security & Integrity

This application is built according to **OWASP Security Best Practices**:
* ✅ **Zero Hardcoded Secrets**: Credentials managed via environment variables (`django-environ`).
* ✅ **Anti-BFcache Navigation**: Protected dashboards cannot be accessed via browser history after logout.
* ✅ **Data Isolation**: Student client data is strictly segregated from administrative operations.

---

## 👨‍💻 Maintainer & Leadership

**CTRL A IT HUB Executive Board & Tech Team**  
📍 ECIL X Road, Hyderabad, Telangana – 500062  
🌐 Website: [https://ctrlaithub.com](https://ctrlaithub.com)  
📞 Contact: +91 91333 91401 / +91 91333 91402  
📧 Email: info@ctrlaithub.com  
