from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
from django.conf import settings
from student.models import AcademicDepartment,Student
from django.core.exceptions import ValidationError
from django.db import transaction
# Create your models here.

class User(AbstractUser):
    ROLES = (
        ("admin", "Admin"),
        ("faculty", "Faculty"),
        ("student", "Student"),
    )
    STATUS = (
        ("active", "Active"),
        ("blocked", "Blocked"),
    )

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20,choices=ROLES)
    status = models.CharField(max_length=20, choices=STATUS,default="active")
    is_deleted = models.BooleanField(default=False)
    needs_password_change = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                try:
                    old_user = User.objects.get(pk=self.pk)
                    if old_user.role == 'admin' and self.role != 'admin':
                        has_student_profile = Student.objects.filter(user_id=self.pk).exists()
                        if has_student_profile:
                            self.is_staff = False
                        else:
                            raise ValidationError(
                                "Admin cannot be changed to student/faculty unless a student profile exists."
                            )

                    elif old_user.role != 'admin' and self.role == 'admin':
                        self.is_staff = True
                        if not Admin.objects.filter(user_id=self.pk).exists():
                            Admin.objects.create(
                                user=self,
                                designation='Administrator',
                                gender='male',
                                contact_no='',
                                emergency_contact_no='',
                                present_address='',
                                permanent_address='',
                                management_department_id=1,
                            )

                    else:
                        self.is_staff = (self.role == 'admin')

                except User.DoesNotExist:
                    self.is_staff = (self.role == 'admin')
            else:
                self.is_staff = (self.role == 'admin')

            super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.email} - {self.status}"
    
class Admin(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_profile'
    )

    designation = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    contact_no = models.CharField(max_length=20)
    emergency_contact_no = models.CharField(max_length=20)
    present_address = models.TextField()
    permanent_address = models.TextField()
    profile_image = models.ImageField(
        upload_to='admin/profiles/',
        blank=True,
        null=True
    )
    management_department = models.ForeignKey(
        AcademicDepartment, 
        on_delete=models.PROTECT,
        related_name='admins'
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} ({self.designation})"