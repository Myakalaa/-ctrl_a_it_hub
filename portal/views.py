from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse, Http404
import csv

from .models import (
    HeroBanner, Service, Course, StudentProfile, 
    Assignment, CourseMaterial, Certificate, 
    Enquiry, Testimonial, PartnerLogo, GalleryItem,
    JobApplication, JobOpening
) 
from .forms import (
    EnquiryForm, StudentRegisterForm, StudentLoginForm,
    HeroBannerForm, CourseForm, CertificateForm, 
    StudentProfileUpdateForm, AssignmentForm, CourseMaterialForm,
    JobOpeningForm, GalleryItemForm
)

def is_staff(user):
    return user.is_authenticated and user.is_staff

# --- CLIENT PAGES ---

def home(request):
    import os
    import shutil
    from django.conf import settings

    banners = HeroBanner.objects.filter(is_active=True).order_by('display_order', '-id')
    featured_courses = Course.objects.filter(is_featured=True)[:6]
    services = Service.objects.all()[:4]
    testimonials = Testimonial.objects.all()
    partners = PartnerLogo.objects.all()
    
    # Auto-initialize default gallery items if empty
    if GalleryItem.objects.count() == 0:
        default_gallery = [
            {
                "title": "Interactive Workshop & Seminar",
                "category": "Hands on Future",
                "description": "Interactive learning session focusing on industry readiness, soft skills, and tech concepts.",
                "file": "gallery/training1.jpg"
            },
            {
                "title": "Skill Development Sessions",
                "category": "Placement Program",
                "description": "Special training sessions covering accounting principles, advanced excel, and digital literacy.",
                "file": "gallery/training2.jpg"
            },
            {
                "title": "Faculty & Student Gathering",
                "category": "Career Path Guidance",
                "description": "Engaging interactive feedback session with our students and certified training leaders.",
                "file": "gallery/training3.jpg"
            },
            {
                "title": "Classroom Training Lectures",
                "category": "Hands on Coding",
                "description": "Lectures on structured programming, algorithms, database systems, and full-stack development.",
                "file": "gallery/training4.png"
            },
            {
                "title": "Classroom Group Discussion",
                "category": "Assured Placements",
                "description": "Group discussions, mock interviews, and presentation training sessions for placement readiness.",
                "file": "gallery/training5.jpg"
            },
            {
                "title": "One-on-One Career Advice",
                "category": "Student Mentorship",
                "description": "Individual mentorship sessions to help choose career tracks, specialize, and secure jobs.",
                "file": "gallery/training6.jpg"
            },
            {
                "title": "Mock Interview Assessment",
                "category": "MNC Prep Sessions",
                "description": "Comprehensive mock interview rounds with customized review and improvement reports.",
                "file": "gallery/training7.jpg"
            },
            {
                "title": "Outdoor Mobility Campaign",
                "category": "CSR Placement Drive",
                "description": "Student placement drives and outdoor technical outreach campaigns across communities.",
                "file": "gallery/training8.jpg"
            }
        ]
        
        for item in default_gallery:
            src_file = os.path.join(settings.BASE_DIR, "static", "images", "gallery", os.path.basename(item["file"]))
            dest_rel_path = os.path.join("gallery", os.path.basename(item["file"]))
            dest_abs_path = os.path.join(settings.MEDIA_ROOT, dest_rel_path)
            
            os.makedirs(os.path.dirname(dest_abs_path), exist_ok=True)
            
            if os.path.exists(src_file) and not os.path.exists(dest_abs_path):
                shutil.copy(src_file, dest_abs_path)
            
            GalleryItem.objects.create(
                title=item["title"],
                category=item["category"],
                description=item["description"],
                media_type="image",
                file=dest_rel_path
            )
            
    gallery = GalleryItem.objects.all().order_by('-created_at')

    # Handle quick enquiry raw POST from home page form
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        if name and email and phone:
            enquiry = Enquiry.objects.create(
                name=name, email=email, phone=phone,
                enquiry_type='general',
                message="Quick enquiry from home page."
            )
            # Dispatch automated WhatsApp notification alert asynchronously in background
            from .tasks import send_whatsapp_notification_task, send_bpo_enquiry_email_task
            send_whatsapp_notification_task.delay(
                to_phone=enquiry.phone,
                student_name=enquiry.name,
                course_name="General IT Training / Enquiry",
                enquiry_type=enquiry.enquiry_type
            )
            # Dispatch BPO enquiry email alert asynchronously
            send_bpo_enquiry_email_task.delay(
                name=enquiry.name,
                email=enquiry.email,
                phone=enquiry.phone,
                enquiry_type=enquiry.enquiry_type,
                message=enquiry.message
            )
            messages.success(request, "Thank you! Your enquiry has been submitted. We will contact you shortly.")
        return redirect('home')

    companies = [
        {"name": "TCS", "logo": "images/clients/tcs.png"},
        {"name": "IBM", "logo": "images/clients/ibm.png"},
        {"name": "Google", "logo": "images/clients/google.png"},
        {"name": "Microsoft", "logo": "images/clients/microsoft.png"},
        {"name": "Amazon", "logo": "images/clients/amazon.png"},
        {"name": "Accenture", "logo": "images/clients/accenture.png"},
        {"name": "Deloitte", "logo": "images/clients/deloitte.png"},
        {"name": "Meta", "logo": "images/clients/meta.png"},
        {"name": "Cognizant", "logo": "images/clients/cognizant.png"},
        {"name": "Wipro", "logo": "images/clients/wipro.png"},
        {"name": "HCLTech", "logo": "images/clients/hcltech.png"},
        {"name": "FACTSET", "logo": "images/clients/factset.png"},
        {"name": "J.P.Morgan", "logo": "images/clients/jpmorgan.png"},
        {"name": "ADP", "logo": "images/clients/adp.png"},
        {"name": "HSBC", "logo": "images/clients/hsbc.png"},
        {"name": "Mindra", "logo": "images/clients/mindra.png"},
        {"name": "Wells Fargo", "logo": "images/clients/wellsfargo.png"},
        {"name": "Citibank", "logo": "images/clients/citibank.png"},
        {"name": "Capgemini", "logo": "images/clients/capgemini.png"},
        {"name": "L&T Infotech", "logo": "images/clients/ltinfotech.png"}
    ]

    # Auto-initialize default openings if empty
    if JobOpening.objects.count() == 0:
        JobOpening.objects.create(
            title="Tally & Advanced Excel Trainer",
            department="technical",
            location="ECIL X Road, Hyderabad",
            experience="2+ Years",
            description="Train students in accounting standards, Tally Prime features, GST calculations, and advanced Microsoft Excel spreadsheets (vlookup, pivot tables, macros)."
        )
        JobOpening.objects.create(
            title="Student Mobilizer & Recruiter",
            department="operations",
            location="ECIL X Road, Hyderabad",
            experience="1+ Year",
            description="Conduct college seminars, drive student mobilization campaigns, manage course awareness programs, and guide enrollments for skill development plans."
        )
    openings = JobOpening.objects.filter(is_active=True).order_by('-created_at')

    context = {
        'banners': banners,
        'featured_courses': featured_courses,
        'services': services,
        'testimonials': testimonials,
        'partners': partners,
        'gallery': gallery,
        'companies': companies,
        'openings': openings,
    }
    return render(request, 'home.html', context)


def about(request):
    testimonials = Testimonial.objects.all()[:3]
    return render(request, 'about.html', {'testimonials': testimonials})


def services(request):
    it_consulting = Service.objects.filter(category='it_consulting')
    bpo_projects = Service.objects.filter(category='bpo_projects')
    csr_training = Service.objects.filter(category='csr_training')
    gov_projects = Service.objects.filter(category='gov_projects')
    
    context = {
        'it_consulting': it_consulting,
        'bpo_projects': bpo_projects,
        'csr_training': csr_training,
        'gov_projects': gov_projects,
    }
    return render(request, 'services.html', context)


def service_it(request):
    services = Service.objects.filter(category='it_consulting')
    return render(request, 'services/it_consulting.html', {'services': services})


def service_bpo(request):
    services = Service.objects.filter(category='bpo_projects')
    return render(request, 'services/bpo_projects.html', {'services': services})


def service_csr(request):
    services = Service.objects.filter(category='csr_training')
    return render(request, 'services/csr_training.html', {'services': services})


def service_gov(request):
    services = Service.objects.filter(category='gov_projects')
    return render(request, 'services/gov_projects.html', {'services': services})


def courses_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    courses = Course.objects.all().order_by('id')
    categories = Course.CATEGORY_CHOICES
    
    context = {
        'courses': courses,
        'categories': categories,
        'query': query,
        'selected_category': category,
    }
    return render(request, 'courses.html', context)


def career_view(request):
    openings = JobOpening.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'career.html', {'openings': openings})


def placements_view(request):
    testimonials = Testimonial.objects.all()[:4]
    return render(request, 'placements.html', {'testimonials': testimonials})


def contact_view(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            
            # Send BPO enquiry email and whatsapp notifications asynchronously using Celery
            from .tasks import send_whatsapp_notification_task, send_bpo_enquiry_email_task
            try:
                send_whatsapp_notification_task.delay(
                    to_phone=enquiry.phone,
                    student_name=enquiry.name,
                    course_name=enquiry.course_interested or "General Training / BPO Solutions",
                    enquiry_type=enquiry.enquiry_type
                )
            except Exception:
                pass  # WhatsApp failure should not block the response

            send_bpo_enquiry_email_task.delay(
                name=enquiry.name,
                email=enquiry.email,
                phone=enquiry.phone,
                enquiry_type=enquiry.enquiry_type,
                message=enquiry.message
            )
            
            messages.success(request, "Your enquiry has been received successfully. We will reach out to you within 24 hours.")
            return redirect('contact')
    else:
        course = request.GET.get('course', '')
        form = EnquiryForm(initial={'course_interested': course})
    return render(request, 'contact.html', {'form': form})


def verify_certificate(request):
    code = request.GET.get('code', '').strip()
    certificate = None
    searched = False
    
    if code:
        searched = True
        try:
            certificate = Certificate.objects.get(certificate_code__iexact=code, is_verified=True)
        except Certificate.DoesNotExist:
            certificate = None
            
    return render(request, 'verification/verify_certificate.html', {
        'certificate': certificate, 
        'code': code,
        'searched': searched
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def submit_job_application(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        qualification = request.POST.get('qualification', '').strip()
        experience = request.POST.get('experience', '').strip()
        resume_file = request.FILES.get('resume')

        if not (job_title and name and email and phone and qualification and experience and resume_file):
            return JsonResponse({'success': False, 'message': 'All fields are required, including resume file upload.'}, status=400)

        # Save to database
        app = JobApplication.objects.create(
            job_title=job_title,
            name=name,
            email=email,
            phone=phone,
            qualification=qualification,
            experience=experience,
            resume=resume_file
        )

        # Send HR email and whatsapp notification asynchronously using Celery
        from .tasks import send_hr_notification_task, send_hr_candidate_email_task
        try:
            send_hr_notification_task.delay(
                name=app.name,
                phone=app.phone,
                job_title=app.job_title
            )
        except Exception:
            pass  # WhatsApp alert failure should not block the response
        
        resume_url = request.build_absolute_uri(app.resume.url) if app.resume else None
        resume_path = app.resume.name if app.resume else None  # e.g. "resumes/filename.pdf"
        send_hr_candidate_email_task.delay(
            name=app.name,
            email=app.email,
            phone=app.phone,
            job_title=app.job_title,
            qualification=app.qualification,
            experience=app.experience,
            resume_url=resume_url,
            resume_path=resume_path
        )

        return JsonResponse({'success': True, 'message': 'Application submitted successfully! Our HR team will review your profile shortly.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid Request Method.'}, status=405)


# --- STUDENT PORTAL ---

def student_register(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to CTRL A IT HUB, {user.first_name}! You are registered and logged in.")
            return redirect('student_dashboard')
    else:
        form = StudentRegisterForm()
    return render(request, 'portal/register.html', {'form': form})


def student_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        form = StudentLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('student_dashboard')
    else:
        form = StudentLoginForm()
    return render(request, 'portal/login.html', {'form': form})


def student_logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def student_dashboard(request):
    try:
        profile = request.user.profile
    except StudentProfile.DoesNotExist:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        messages.error(request, "Student profile does not exist. Please contact administrator.")
        logout(request)
        return redirect('login')
        
    course = profile.enrolled_course
    materials = CourseMaterial.objects.filter(course=course) if course else []
    assignments = Assignment.objects.filter(course=course).order_by('due_date') if course else []
    
    context = {
        'profile': profile,
        'course': course,
        'materials': materials,
        'assignments': assignments,
    }
    return render(request, 'portal/student_dashboard.html', context)


# --- CUSTOM ADMIN PORTAL ---

@user_passes_test(is_staff, login_url='login')
def admin_dashboard(request):
    stats = {
        'students_count': StudentProfile.objects.count(),
        'courses_count': Course.objects.count(),
        'enquiries_pending': Enquiry.objects.filter(is_resolved=False).count(),
        'certificates_count': Certificate.objects.count(),
    }
    
    # Load all objects for management tabs
    banners = HeroBanner.objects.all().order_by('display_order')
    courses = Course.objects.all()
    students = StudentProfile.objects.all().select_related('user', 'enrolled_course')
    certificates = Certificate.objects.all()
    enquiries = Enquiry.objects.all().order_by('-date_submitted')
    materials = CourseMaterial.objects.all().select_related('course')
    assignments = Assignment.objects.all().select_related('course')
    applications = JobApplication.objects.all().order_by('-applied_at')
    openings = JobOpening.objects.all().order_by('-created_at')
    gallery_items = GalleryItem.objects.all().order_by('-created_at')
    
    context = {
        'stats': stats,
        'banners': banners,
        'courses': courses,
        'students': students,
        'certificates': certificates,
        'enquiries': enquiries,
        'materials': materials,
        'assignments': assignments,
        'applications': applications,
        'openings': openings,
        'gallery_items': gallery_items,
    }
    return render(request, 'portal/admin_dashboard.html', context)


@user_passes_test(is_staff, login_url='login')
def admin_banner_add(request):
    if request.method == 'POST':
        form = HeroBannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner added successfully!")
            return redirect('admin_dashboard')
    else:
        form = HeroBannerForm()
    return render(request, 'portal/admin_form.html', {'form': form, 'title': 'Add Hero Banner'})


@user_passes_test(is_staff, login_url='login')
def admin_banner_delete(request, pk):
    banner = get_object_or_404(HeroBanner, pk=pk)
    banner.delete()
    messages.success(request, "Banner deleted successfully!")
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login')
def admin_course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully!")
            return redirect('admin_dashboard')
    else:
        form = CourseForm()
    return render(request, 'portal/admin_form.html', {'form': form, 'title': 'Add New Course'})


@user_passes_test(is_staff, login_url='login')
def admin_course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login')
def admin_student_edit(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Student details updated successfully!")
            return redirect('admin_dashboard')
    else:
        form = StudentProfileUpdateForm(instance=profile)
    return render(request, 'portal/admin_form.html', {'form': form, 'title': f'Edit Student: {profile.user.get_full_name()}'})


@user_passes_test(is_staff, login_url='login')
def admin_student_delete(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    user = profile.user
    user.delete()  # Cascade deletes profile
    messages.success(request, "Student deleted successfully!")
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login')
def admin_certificate_add(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Certificate issued successfully!")
            return redirect('admin_dashboard')
    else:
        form = CertificateForm()
    return render(request, 'portal/admin_form.html', {'form': form, 'title': 'Issue Certificate'})


@user_passes_test(is_staff, login_url='login')
def admin_certificate_delete(request, pk):
    cert = get_object_or_404(Certificate, pk=pk)
    cert.delete()
    messages.success(request, "Certificate deleted successfully!")
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login')
def admin_material_add(request):
    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Course material uploaded successfully!")
            return redirect('admin_dashboard')
    else:
        form = CourseMaterialForm()
    return render(request, 'portal/admin_form.html', {'form': form, 'title': 'Upload Course Material'})


@user_passes_test(is_staff, login_url='login')
def admin_assignment_add(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment posted successfully!")
            return redirect('admin_dashboard')
def student_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        form = StudentLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('student_dashboard')
    else:
        form = StudentLoginForm()
    return render(request, 'portal/login.html', {'form': form})


def student_logout_view(request):
    logout(request)
    request.session.flush()
    messages.info(request, "You have been logged out successfully.")
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required
def student_dashboard(request):
    try:
        profile = request.user.profile
    except StudentProfile.DoesNotExist:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        messages.error(request, "Student profile does not exist. Please contact administrator.")
        logout(request)
        return redirect('login')
        
    course = profile.enrolled_course
    materials = CourseMaterial.objects.filter(course=course) if course else []
    assignments = Assignment.objects.filter(course=course).order_by('due_date') if course else []
    
    context = {
        'profile': profile,
        'course': course,
        'materials': materials,
        'assignments': assignments,
    }
    return render(request, 'portal/student_dashboard.html', context)


# --- CUSTOM ADMIN PORTAL ---

@user_passes_test(is_staff, login_url='login')
def admin_dashboard(request):
    stats = {
        'students_count': StudentProfile.objects.count(),
        'courses_count': Course.objects.count(),
        'enquiries_pending': Enquiry.objects.filter(is_resolved=False).count(),
        'certificates_count': Certificate.objects.count(),
    }
    
    # Load all objects for management tabs
    banners = HeroBanner.objects.all().order_by('display_order')
    courses = Course.objects.all()
    students = StudentProfile.objects.all().select_related('user', 'enrolled_course')
    certificates = Certificate.objects.all()
    enquiries = Enquiry.objects.all().order_by('-date_submitted')
    materials = CourseMaterial.objects.all().select_related('course')
    assignments = Assignment.objects.all().select_related('course')
    applications = JobApplication.objects.all().order_by('-applied_at')
    openings = JobOpening.objects.all().order_by('-created_at')
    gallery_items = GalleryItem.objects.all().order_by('-created_at')
    
    context = {
        'stats': stats,
        'banners': banners,
        'courses': courses,
        'students': students,
        'certificates': certificates,
        'enquiries': enquiries,
        'materials': materials,
        'assignments': assignments,
        'applications': applications,
        'openings': openings,
        'gallery_items': gallery_items,
    }
    return render(request, 'portal/admin_dashboard.html', context)


@user_passes_test(is_staff, login_url='login')
def admin_banner_add(request):
    if request.method == 'POST':
        form = HeroBannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner added successfully!")
            return redirect('admin_dashboard')
    else:
        form = HeroBannerForm()
    return render(request, 'portal/admin_form.html', {'form': form, 'title': 'Add Hero Banner'})


@user_passes_test(is_staff, login_url='login')
def admin_banner_delete(request, pk):
    banner = get_object_or_404(HeroBanner, pk=pk)
    banner.delete()
    messages.success(request, "Banner deleted successfully!")
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login')
def admin_course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully!")
            return redirect('admin_dashboard')
    else:
        form = CourseForm()
    return render(request, 'portal/admin_form.html', {'form': form, 'title': 'Add New Course'})


@user_passes_test(is_staff, login_url='login')
def admin_course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login')
def admin_student_edit(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Student details updated successfully!")
            return redirect('admin_dashboard')
    else:
        form = StudentProfileUpdateForm(instance=profile)
    return render(request, 'portal/admin_form.html', {'form': form, 'title': f'Edit Student: {profile.user.get_full_name()}'})


@user_passes_test(is_staff, login_url='login')
def admin_student_delete(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    user = profile.user
    user.delete()  # Cascade deletes profile
    messages.success(request, "Student deleted successfully!")
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login')
def admin_certificate_add(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Certificate issued successfully!")
            return redirect('admin_dashboard')
    else:
        form = CertificateForm()
    return render(request, 'portal/admin_form.html', {'form': form, 'title': 'Issue Certificate'})


@user_passes_test(is_staff, login_url='login')
def admin_certificate_delete(request, pk):
    cert = get_object_or_404(Certificate, pk=pk)
    cert.delete()
    messages.success(request, "Certificate deleted successfully!")
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login')
def admin_material_add(request):
    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Course material uploaded successfully!")
            return redirect('admin_dashboard')
    else:
        form = CourseMaterialForm()
    return render(request, 'portal/admin_form.html', {'form': form, 'title': 'Upload Course Material'})


@user_passes_test(is_staff, login_url='login')
def admin_assignment_add(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment posted successfully!")
            return redirect('admin_dashboard')
    else:
        form = AssignmentForm()
    return render(request, 'portal/admin_form.html', {'form': form, 'title': 'Post New Assignment'})


@user_passes_test(is_staff, login_url='login')
def admin_enquiry_resolve(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    enquiry.is_resolved = True
    enquiry.save()
    messages.success(request, "Enquiry marked as resolved.")
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login')
def admin_application_delete(request, pk):
    app = get_object_or_404(JobApplication, pk=pk)
    app.delete()
    messages.success(request, "Job application deleted successfully.")
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login')
def admin_opening_add(request):
    if request.method == 'POST':
        form = JobOpeningForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job opening posted successfully!")
            return redirect('admin_dashboard')
    else:
        form = JobOpeningForm()
    return render(request, 'portal/admin_form.html', {'form': form, 'title': 'Post Job Opening'})


@user_passes_test(is_staff, login_url='login')
def admin_opening_delete(request, pk):
    opening = get_object_or_404(JobOpening, pk=pk)
    opening.delete()
    messages.success(request, "Job opening deleted successfully.")
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login')
def admin_gallery_add(request):
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Gallery item added successfully!")
            return redirect('admin_dashboard')
    else:
        form = GalleryItemForm()
    return render(request, 'portal/admin_form.html', {'form': form, 'title': 'Add Gallery Slide'})


@user_passes_test(is_staff, login_url='login')
def admin_gallery_delete(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    item.delete()
    messages.success(request, "Gallery item deleted successfully.")
    return redirect('admin_dashboard')


# --- CUSTOM ROLE-BASED DASHBOARDS & ACCESS CHECKS ---

def is_mis(user):
    if not user.is_authenticated:
        return False
    uname = user.username.lower()
    return user.is_superuser or uname in ['mis', 'bpo'] or user.groups.filter(name__in=['BPO Team', 'MIS Executive']).exists()

def is_hr(user):
    if not user.is_authenticated:
        return False
    uname = user.username.lower()
    return user.is_superuser or uname == 'hr' or user.groups.filter(name='HR Team').exists()

def custom_login_redirect(request):
    if request.user.is_authenticated:
        uname = request.user.username.lower()
        if uname in ['mis', 'bpo'] or request.user.groups.filter(name__in=['BPO Team', 'MIS Executive']).exists():
            return redirect('bpo_dashboard')
        if uname == 'hr' or request.user.groups.filter(name='HR Team').exists():
            return redirect('hr_dashboard')
        if request.user.is_superuser or request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('home')
    else:
        from django.contrib.auth.views import LoginView
        return LoginView.as_view(template_name='admin/login.html', next_page='/login/')(request)


# ─── MIS EXECUTIVE DASHBOARD ────────────────────────────────────────────────

@user_passes_test(is_mis, login_url='/login/')
def bpo_dashboard(request):
    enquiries = Enquiry.objects.all()
    # Search & Filter
    q = request.GET.get('q', '')
    type_filter = request.GET.get('type', '')
    status_filter = request.GET.get('status', '')
    if q:
        enquiries = enquiries.filter(name__icontains=q) | Enquiry.objects.filter(course_interested__icontains=q)
    if type_filter:
        enquiries = enquiries.filter(enquiry_type=type_filter)
    if status_filter == 'resolved':
        enquiries = enquiries.filter(is_resolved=True)
    elif status_filter == 'pending':
        enquiries = enquiries.filter(is_resolved=False)
    # Stats
    total   = Enquiry.objects.count()
    pending  = Enquiry.objects.filter(is_resolved=False).count()
    resolved = Enquiry.objects.filter(is_resolved=True).count()
    ctx = {
        'enquiries': enquiries,
        'total': total, 'pending': pending, 'resolved': resolved,
        'q': q, 'type_filter': type_filter, 'status_filter': status_filter,
    }
    return render(request, 'bpo_dashboard.html', ctx)

@user_passes_test(is_mis, login_url='/login/')
def mis_resolve_enquiry(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    enquiry.is_resolved = not enquiry.is_resolved
    enquiry.save()
    messages.success(request, f"Enquiry marked as {'Resolved' if enquiry.is_resolved else 'Pending'}.")
    return redirect('bpo_dashboard')

@user_passes_test(is_mis, login_url='/login/')
def mis_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="enquiries.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Name', 'Email', 'Phone', 'Course Interested', 'Type', 'Status'])
    for e in Enquiry.objects.all():
        writer.writerow([
            e.date_submitted.strftime('%d-%m-%Y'),
            e.name, e.email, e.phone,
            e.course_interested or '-',
            e.get_enquiry_type_display(),
            'Resolved' if e.is_resolved else 'Pending'
        ])
    return response


# ─── HR DASHBOARD ────────────────────────────────────────────────────────────

@user_passes_test(is_hr, login_url='/login/')
def hr_dashboard(request):
    applications = JobApplication.objects.all()
    # Search & Filter
    q = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    if q:
        applications = applications.filter(name__icontains=q) | JobApplication.objects.filter(job_title__icontains=q)
    if status_filter:
        applications = applications.filter(status=status_filter)
    # Stats
    total       = JobApplication.objects.count()
    pending     = JobApplication.objects.filter(status='pending').count()
    shortlisted = JobApplication.objects.filter(status='shortlisted').count()
    rejected    = JobApplication.objects.filter(status='rejected').count()
    ctx = {
        'applications': applications,
        'total': total, 'pending': pending,
        'shortlisted': shortlisted, 'rejected': rejected,
        'q': q, 'status_filter': status_filter,
    }
    return render(request, 'hr_dashboard.html', ctx)

@user_passes_test(is_hr, login_url='/login/')
def hr_update_status(request, pk):
    if request.method == 'POST':
        app = get_object_or_404(JobApplication, pk=pk)
        new_status = request.POST.get('status', 'pending')
        app.status = new_status
        app.is_reviewed = new_status != 'pending'
        app.save()
        messages.success(request, f"{app.name}'s application marked as {app.get_status_display()}.")
    return redirect('hr_dashboard')

@user_passes_test(is_hr, login_url='/login/')
def hr_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job_applications.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date Applied', 'Name', 'Email', 'Phone', 'Job Title', 'Qualification', 'Experience', 'Status'])
    for a in JobApplication.objects.all():
        writer.writerow([
            a.applied_at.strftime('%d-%m-%Y'),
            a.name, a.email, a.phone,
            a.job_title, a.qualification, a.experience,
            a.get_status_display()
        ])
    return response
