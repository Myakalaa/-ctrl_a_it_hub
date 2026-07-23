from django.db import models
from django.contrib.auth.models import User

class HeroBanner(models.Model):
    title = models.CharField(max_length=200, help_text="Main heading on the banner")
    subtitle = models.CharField(max_length=500, blank=True, help_text="Subheading or tagline")
    image = models.ImageField(upload_to='banners/images/', blank=True, null=True, help_text="Upload banner image")
    video = models.FileField(upload_to='banners/videos/', blank=True, null=True, help_text="Upload banner video (MP4 format recommended)")
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0, help_text="Order in which banner appears (lower numbers first)")

    class Meta:
        ordering = ['display_order', '-id']

    def __str__(self):
        return self.title


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('it_consulting', 'IT Consulting & Academic Projects'),
        ('bpo_projects', 'BPO Projects & Support'),
        ('csr_training', 'CSR Training & Skill Development'),
        ('gov_projects', 'Government Training Projects'),
    ]
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, default='fas fa-laptop-code', help_text="FontAwesome icon class (e.g., fas fa-database)")

    def __str__(self):
        return f"{self.get_category_display()} - {self.title}"


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming Courses'),
        ('web_technologies', 'Web Technologies'),
        ('database_sap', 'Database & SAP'),
        ('testing_analytics', 'Testing & Analytics'),
        ('professional', 'Professional Training'),
    ]
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    syllabus = models.TextField(blank=True, help_text="Course syllabus details (line separated or rich text)")
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    duration = models.CharField(max_length=50, default='3 Months')
    price = models.CharField(max_length=50, default='Rs. 15,000', help_text="Price or Contact for details")
    is_featured = models.BooleanField(default=False, help_text="Display on Home page featured courses")
    updated_at = models.DateTimeField(auto_now=True, help_text="Auto-updated when course is saved")

    def __str__(self):
        return self.title


class StudentProfile(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active Student'),
        ('completed', 'Completed'),
        ('placed', 'Placed'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    roll_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15)
    enrolled_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='materials/')

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Certificate(models.Model):
    student_name = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    certificate_code = models.CharField(max_length=50, unique=True, help_text="Unique verification code (e.g., CTA-2026-0001)")
    issue_date = models.DateField()
    certificate_file = models.FileField(upload_to='certificates/')
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student_name} - {self.certificate_code}"


class Enquiry(models.Model):
    ENQUIRY_TYPE_CHOICES = [
        ('general', 'General / Quick Enquiry'),
        ('student', 'Student Admission/Course Enquiry'),
        ('corporate', 'Corporate Training/BPO Enquiry'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course_interested = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    enquiry_type = models.CharField(max_length=20, choices=ENQUIRY_TYPE_CHOICES, default='general')
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Enquiries"
        ordering = ['-date_submitted']

    def __str__(self):
        return f"{self.name} - {self.get_enquiry_type_display()} ({self.date_submitted.date()})"


class Testimonial(models.Model):
    student_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.IntegerField(default=5, help_text="Rating between 1 and 5")
    student_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    def __str__(self):
        return f"{self.student_name} - {self.course_name}"


class PartnerLogo(models.Model):
    name = models.CharField(max_length=100)
    logo_image = models.ImageField(upload_to='partners/')

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    title = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100, default='General')
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    file = models.FileField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Gallery Item {self.id}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending',     'Pending Review'),
        ('reviewing',   'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected',    'Rejected'),
    ]
    job_title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    qualification = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.name} - {self.job_title}"


class JobOpening(models.Model):
    DEPARTMENT_CHOICES = [
        ('technical', 'Technical Training'),
        ('operations', 'Operations & Outreach'),
        ('admin', 'Administration'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=150)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='technical')
    location = models.CharField(max_length=100, default='ECIL X Road, Hyderabad')
    experience = models.CharField(max_length=50, default='2+ Years')
    description = models.TextField(help_text="Detailed job description and responsibilities")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


