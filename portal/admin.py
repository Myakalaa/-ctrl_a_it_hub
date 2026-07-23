from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from django.utils import timezone
import csv
from .models import (
    HeroBanner, Service, Course, StudentProfile, 
    Assignment, CourseMaterial, Certificate, 
    Enquiry, Testimonial, PartnerLogo, GalleryItem,
    JobApplication, JobOpening
)

# ===== ADMIN SITE BRANDING =====
admin.site.site_header = "CTRL A IT HUB — Admin Portal"
admin.site.site_title = "CTRL A IT HUB Admin"
admin.site.index_title = "Welcome to the Management Dashboard"


# ===== SHARED CSV EXPORT ACTION =====
def export_as_csv(modeladmin, request, queryset):
    """Universal CSV export action available across all admin panels."""
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.model_name}_export_{timezone.now().strftime("%Y%m%d")}.csv'
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
export_as_csv.short_description = "Export Selected as CSV"


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'is_active', 'display_order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'display_order')
    search_fields = ('title', 'subtitle')
    list_per_page = 20
    ordering = ('display_order',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    list_per_page = 25


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration', 'price', 'is_featured', 'updated_at')
    list_filter = ('category', 'is_featured')
    list_editable = ('is_featured',)
    search_fields = ('title', 'description')
    readonly_fields = ('updated_at',)
    list_per_page = 20
    actions = [export_as_csv]


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'roll_number', 'phone', 'enrolled_course', 'attendance_colored', 'status_badge')
    list_filter = ('status', 'enrolled_course')
    search_fields = ('user__first_name', 'user__last_name', 'roll_number', 'phone')
    list_per_page = 30
    actions = [export_as_csv]

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Student Name'

    def attendance_colored(self, obj):
        pct = float(obj.attendance_percentage)
        if pct >= 75:
            color = '#28a745'
        elif pct >= 50:
            color = '#ffc107'
        else:
            color = '#dc3545'
        return format_html('<span style="color:{};font-weight:700;">{:.1f}%</span>', color, pct)
    attendance_colored.short_description = 'Attendance'

    def status_badge(self, obj):
        colors = {'active': '#007bff', 'completed': '#28a745', 'placed': '#f7941d'}
        color = colors.get(obj.status, '#6c757d')
        return format_html('<span style="background:{};color:#fff;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:700;">{}</span>', color, obj.get_status_display())
    status_badge.short_description = 'Status'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date')
    list_filter = ('course', 'due_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'
    list_per_page = 25


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    list_filter = ('course',)
    search_fields = ('title',)
    list_per_page = 25


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course_name', 'certificate_code', 'issue_date', 'verified_badge')
    list_filter = ('issue_date', 'is_verified')
    search_fields = ('student_name', 'course_name', 'certificate_code')
    date_hierarchy = 'issue_date'
    list_per_page = 30
    actions = [export_as_csv]

    def verified_badge(self, obj):
        if obj.is_verified:
            return format_html('<span style="background:#28a745;color:#fff;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:700;">✓ Verified</span>')
        return format_html('<span style="background:#dc3545;color:#fff;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:700;">✗ Not Verified</span>')
    verified_badge.short_description = 'Verification Status'


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'enquiry_type', 'course_interested', 'date_submitted', 'resolved_badge', 'is_resolved')
    list_filter = ('enquiry_type', 'is_resolved', 'date_submitted')
    list_editable = ('is_resolved',)
    search_fields = ('name', 'email', 'phone', 'message', 'course_interested')
    readonly_fields = ('date_submitted',)
    date_hierarchy = 'date_submitted'
    list_per_page = 30
    actions = [export_as_csv]
    ordering = ('-date_submitted',)

    def resolved_badge(self, obj):
        if obj.is_resolved:
            return format_html('<span style="background:#28a745;color:#fff;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:700;">✓ Resolved</span>')
        return format_html('<span style="background:#ffc107;color:#000;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:700;">⏳ Pending</span>')
    resolved_badge.short_description = 'Status'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course_name', 'star_rating')
    list_filter = ('rating',)
    search_fields = ('student_name', 'course_name', 'review')
    list_per_page = 20

    def star_rating(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color:#f7941d;font-size:1rem;">{}</span>', stars)
    star_rating.short_description = 'Rating'


admin.site.register(PartnerLogo)


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'media_type', 'created_at')
    list_filter = ('category', 'media_type', 'created_at')
    search_fields = ('title', 'category', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 20


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'phone', 'email', 'qualification', 'experience', 'applied_at', 'reviewed_badge', 'is_reviewed', 'resume_link')
    list_filter = ('job_title', 'is_reviewed', 'applied_at')
    list_editable = ('is_reviewed',)
    search_fields = ('name', 'email', 'phone', 'qualification', 'experience')
    readonly_fields = ('applied_at',)
    date_hierarchy = 'applied_at'
    list_per_page = 25
    actions = [export_as_csv]
    ordering = ('-applied_at',)

    def reviewed_badge(self, obj):
        if obj.is_reviewed:
            return format_html('<span style="background:#28a745;color:#fff;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:700;">✓ Reviewed</span>')
        return format_html('<span style="background:#dc3545;color:#fff;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:700;">New</span>')
    reviewed_badge.short_description = 'Review Status'

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank" style="color:#0056b3;font-weight:600;">📄 Download Resume</a>', obj.resume.url)
        return '—'
    resume_link.short_description = 'Resume'


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'experience', 'active_badge', 'is_active', 'created_at')
    list_filter = ('department', 'is_active', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 20

    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background:#28a745;color:#fff;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:700;">🟢 Active</span>')
        return format_html('<span style="background:#6c757d;color:#fff;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:700;">⭕ Closed</span>')
    active_badge.short_description = 'Status'
