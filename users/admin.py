from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from .models import Admin 

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name',
         'last_name', 'role', 'status','is_deleted','needs_password_change')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = (
        'user_email', 
        'designation', 
        'management_department', 
        'is_deleted',
        'created_at'
    )
    search_fields = ('user__email', 'designation', 'contact_no')
    list_filter = ('gender', 'designation', 'management_department', 'is_deleted')
    fieldsets = (
        ('User and Identity', {
            'fields': ('user', 'designation', 'gender', 'date_of_birth', 'profile_image'),
        }),
        ('Contact Information', {
            'fields': ('contact_no', 'emergency_contact_no'),
        }),
        ('Address', {
            'fields': ('present_address', 'permanent_address'),
        }),
        ('Organizational Details', {
            'fields': ('management_department', 'is_deleted'),
        }),
    )

    @admin.display(description='User Email')
    def user_email(self, obj):
        return obj.user.email
    # Filter queryset to only show staff users
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user__is_staff=True)

admin.site.register(User, CustomUserAdmin)