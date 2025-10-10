from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from .models import Admin
from student.models import Faculty

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
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = [
        'faculty_id',
        'get_full_name',
        'get_email',
        'designation',
        'get_department',
        'contact_no',
        'is_deleted'
    ]
    
    list_filter = [
        'designation',
        'academic_department',
        'academic_faculty',
        'gender',
        'is_deleted',
        'created_at'
    ]
    
    search_fields = [
        'faculty_id',
        'user__first_name',
        'user__last_name',
        'user__email',
        'contact_no'
    ]
    
    readonly_fields = ['faculty_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Faculty Information', {
            'fields': ('faculty_id', 'designation')
        }),
        ('Academic Information', {
            'fields': ('academic_faculty', 'academic_department')
        }),
        ('Personal Information', {
            'fields': ('gender', 'date_of_birth', 'profile_image')
        }),
        ('Contact Information', {
            'fields': ('contact_no', 'emergency_contact_no')
        }),
        ('Address Information', {
            'fields': ('present_address', 'permanent_address')
        }),
        ('Status & Timestamps', {
            'fields': ('is_deleted', 'created_at', 'updated_at')
        }),
    )
    
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 20
    
    # Custom methods for list_display
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'user__first_name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'
    
    def get_department(self, obj):
        return obj.academic_department.code
    get_department.short_description = 'Department'
    get_department.admin_order_field = 'academic_department__code'

    
admin.site.register(User, CustomUserAdmin)