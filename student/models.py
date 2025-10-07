from django.db import models
from django.conf import settings
from django.utils import timezone

class AcademicFaculty(models.Model):
    name = models.CharField(max_length=200, unique=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class AcademicDepartment(models.Model):
    DEPARTMENT_CHOICES = (
        ("Computer Science & Engineering", "Computer Science & Engineering"),
        ("Bachelor of Business Administration", "Bachelor of Business Administration"),
    )
    
    CODES = (
        ("CSE", "Computer Science & Engineering"),
        ("BBA", "Bachelor of Business Administration"),
    )
    
    name = models.CharField(max_length=200, choices=DEPARTMENT_CHOICES)
    code = models.CharField(max_length=10, unique=True, choices=CODES)
    academic_faculty = models.ForeignKey(
        AcademicFaculty, 
        on_delete=models.PROTECT, 
        related_name='departments'
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['academic_faculty', 'name']
        unique_together = ['name', 'academic_faculty']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class AcademicSemester(models.Model):
    SEMESTER_NAME_CHOICES = (
        ("Spring", "Spring"),
        ("Summer", "Summer"),
        ("Fall", "Fall"),
    )
    
    MONTH_CHOICES = (
        ("January", "January"),
        ("February", "February"),
        ("March", "March"),
        ("April", "April"),
        ("May", "May"),
        ("June", "June"),
        ("July", "July"),
        ("August", "August"),
        ("September", "September"),
        ("October", "October"),
        ("November", "November"),
        ("December", "December"),
    )
    
    name = models.CharField(max_length=20, choices=SEMESTER_NAME_CHOICES)
    year = models.IntegerField()
    start_month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    end_month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', 'name']
        unique_together = ['name', 'year']
    
    def __str__(self):
        return f"{self.name} {self.year}"
    
class Student(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )
    
    student_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    academic_department = models.ForeignKey(
        AcademicDepartment,
        on_delete=models.PROTECT,
        related_name='students'
    )
    admission_semester = models.ForeignKey(
        AcademicSemester,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admitted_students'
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    contact_no = models.CharField(max_length=20)
    emergency_contact_no = models.CharField(max_length=20)
    present_address = models.TextField()
    permanent_address = models.TextField()
    guardian_number = models.CharField(max_length=20)
    profile_image = models.ImageField(
        upload_to='students/profiles/',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['academic_department', 'student_id']),
            models.Index(fields=['admission_semester']),
            models.Index(fields=['is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.student_id} - {self.academic_department}"
    
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            if self.admission_semester:
                year = self.admission_semester.year
            else:
                year = timezone.now().year
            
            dept_code = self.academic_department.code
            prefix = f'{year}-{dept_code}-'
            
            last_student = Student.objects.filter(
                student_id__startswith=prefix,
                academic_department=self.academic_department
            ).order_by('-student_id').first()
            
            if last_student and last_student.student_id:
                last_sequence = int(last_student.student_id.split('-')[-1])
                new_sequence = last_sequence + 1
            else:
                new_sequence = 1
            
            self.student_id = f'{year}-{dept_code}-{new_sequence:03d}'
        
        super().save(*args, **kwargs)