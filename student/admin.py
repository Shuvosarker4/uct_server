from django.contrib import admin
from .models import AcademicFaculty, AcademicDepartment, AcademicSemester, Student


@admin.register(AcademicFaculty)
class AcademicFacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_deleted", "created_at", "updated_at")
    list_filter = ("is_deleted",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)


@admin.register(AcademicDepartment)
class AcademicDepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "academic_faculty", "is_deleted", "created_at", "updated_at")
    list_filter = ("academic_faculty", "is_deleted")
    search_fields = ("name", "code", "academic_faculty__name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("academic_faculty__name", "name")


@admin.register(AcademicSemester)
class AcademicSemesterAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "start_month", "end_month", "is_deleted", "created_at", "updated_at")
    list_filter = ("year", "name", "is_deleted")
    search_fields = ("name", "year")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-year", "name")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "user",
        "academic_department",
        "admission_semester",
        "gender",
        "contact_no",
        "is_deleted",
        "created_at",
    )
    list_filter = ("academic_department", "admission_semester", "gender", "is_deleted")
    search_fields = (
        "student_id",
        "user__username",
        "user__email",
        "academic_department__name",
        "academic_department__code",
    )
    readonly_fields = ("student_id", "created_at", "updated_at")
    ordering = ("-created_at",)

