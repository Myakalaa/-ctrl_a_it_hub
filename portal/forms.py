from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    Enquiry, StudentProfile, Course, HeroBanner, 
    Certificate, Assignment, CourseMaterial, GalleryItem,
    JobOpening
)

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'course_interested', 'message', 'enquiry_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Mobile Number'}),
            'course_interested': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Course Name (Optional)'}),
            'message': forms.Textarea(attrs={'class': 'form-input textarea', 'placeholder': 'Write your message or enquiry details here...', 'rows': 4}),
            'enquiry_type': forms.Select(attrs={'class': 'form-input'}),
        }


class StudentRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Mobile Number'}))
    roll_number = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Roll Number (e.g., CTA2026001)'}))
    enrolled_course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True, empty_label="Select Course", widget=forms.Select(attrs={'class': 'form-input'}))

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                roll_number=self.cleaned_data['roll_number'],
                phone=self.cleaned_data['phone'],
                enrolled_course=self.cleaned_data['enrolled_course']
            )
        return user


class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))


class HeroBannerForm(forms.ModelForm):
    class Meta:
        model = HeroBanner
        fields = ['title', 'subtitle', 'image', 'video', 'is_active', 'display_order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['category', 'title', 'description', 'syllabus', 'image', 'duration', 'price', 'is_featured']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'syllabus': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Syllabus details, e.g., Module 1\nModule 2'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'duration': forms.TextInput(attrs={'class': 'form-input'}),
            'price': forms.TextInput(attrs={'class': 'form-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['student_name', 'course_name', 'certificate_code', 'issue_date', 'certificate_file', 'is_verified']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-input'}),
            'course_name': forms.TextInput(attrs={'class': 'form-input'}),
            'certificate_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'CTA-2026-XXXX'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'certificate_file': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class StudentProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = StudentProfile
        fields = ['roll_number', 'phone', 'enrolled_course', 'attendance_percentage', 'status']
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'enrolled_course': forms.Select(attrs={'class': 'form-input'}),
            'attendance_percentage': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'file', 'due_date']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'due_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }


class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['course', 'title', 'file']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['title', 'category', 'description', 'media_type', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Interactive Workshop'}),
            'category': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Hands on Future'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Describe the session/photo...'}),
            'media_type': forms.Select(attrs={'class': 'form-input'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }


class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = ['title', 'department', 'location', 'experience', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Tally & Advanced Excel Trainer'}),
            'department': forms.Select(attrs={'class': 'form-input'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. ECIL X Road, Hyderabad'}),
            'experience': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 2+ Years'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Write job requirements and description here...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input-checkbox'}),
        }
