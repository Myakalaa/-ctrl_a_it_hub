from django.urls import path
from . import views

urlpatterns = [
    # Client Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/it-consulting/', views.service_it, name='service_it'),
    path('services/bpo-projects/', views.service_bpo, name='service_bpo'),
    path('services/csr-skill-development/', views.service_csr, name='service_csr'),
    path('services/government-training/', views.service_gov, name='service_gov'),
    path('courses/', views.courses_view, name='courses'),
    path('career/', views.career_view, name='career'),
    path('placements/', views.placements_view, name='placements'),
    path('contact/', views.contact_view, name='contact'),
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
    path('submit-job-application/', views.submit_job_application, name='submit_job_application'),

    # Student Authentication
    path('register/', views.student_register, name='register'),
    path('login/', views.student_login, name='login'),
    path('logout/', views.student_logout_view, name='logout'),

    # Dashboards
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Custom Admin Content Management
    path('admin-dashboard/banner/add/', views.admin_banner_add, name='admin_banner_add'),
    path('admin-dashboard/banner/delete/<int:pk>/', views.admin_banner_delete, name='admin_banner_delete'),
    
    path('admin-dashboard/course/add/', views.admin_course_add, name='admin_course_add'),
    path('admin-dashboard/course/delete/<int:pk>/', views.admin_course_delete, name='admin_course_delete'),
    
    path('admin-dashboard/student/edit/<int:pk>/', views.admin_student_edit, name='admin_student_edit'),
    path('admin-dashboard/student/delete/<int:pk>/', views.admin_student_delete, name='admin_student_delete'),
    
    path('admin-dashboard/certificate/add/', views.admin_certificate_add, name='admin_certificate_add'),
    path('admin-dashboard/certificate/delete/<int:pk>/', views.admin_certificate_delete, name='admin_certificate_delete'),
    
    path('admin-dashboard/material/add/', views.admin_material_add, name='admin_material_add'),
    path('admin-dashboard/assignment/add/', views.admin_assignment_add, name='admin_assignment_add'),
    
    path('admin-dashboard/enquiry/resolve/<int:pk>/', views.admin_enquiry_resolve, name='admin_enquiry_resolve'),
    path('admin-dashboard/application/delete/<int:pk>/', views.admin_application_delete, name='admin_application_delete'),
    path('admin-dashboard/opening/add/', views.admin_opening_add, name='admin_opening_add'),
    path('admin-dashboard/opening/delete/<int:pk>/', views.admin_opening_delete, name='admin_opening_delete'),
    path('admin-dashboard/gallery/add/', views.admin_gallery_add, name='admin_gallery_add'),
    path('admin-dashboard/gallery/delete/<int:pk>/', views.admin_gallery_delete, name='admin_gallery_delete'),
    
    # Custom Role-Based Dashboards
    path('bpo-dashboard/', views.bpo_dashboard, name='bpo_dashboard'),
    path('bpo-dashboard/resolve/<int:pk>/', views.mis_resolve_enquiry, name='mis_resolve_enquiry'),
    path('bpo-dashboard/export/', views.mis_export_csv, name='mis_export_csv'),
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('hr-dashboard/status/<int:pk>/', views.hr_update_status, name='hr_update_status'),
    path('hr-dashboard/export/', views.hr_export_csv, name='hr_export_csv'),
]
