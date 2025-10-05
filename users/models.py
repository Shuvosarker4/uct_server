from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} - {self.status}"