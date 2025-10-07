from rest_framework import serializers
from .models import Student,AcademicDepartment,AcademicFaculty,AcademicSemester
from users.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class AcademicFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicFaculty
        fields = [
            'id', 
            'name', 
            'is_deleted', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class AcademicFacultySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicFaculty
        fields = ['id', 'name']
class AcademicDepartmentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicDepartment
        fields = ['id', 'name']
class AcademicSemesterSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSemester
        fields = ['id', 'name']


class AcademicDepartmentSerializer(serializers.ModelSerializer):
    academic_faculty_name = serializers.StringRelatedField(
        source='academic_faculty', 
        read_only=True
    )
 
    class Meta:
        model = AcademicDepartment
        fields = [
            'id', 
            'name', 
            'code', 
            'academic_faculty', 
            'academic_faculty_name',
            'is_deleted', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'academic_faculty_name']


class AcademicSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSemester
        fields = [
            'id', 
            'name', 
            'year', 
            'start_month', 
            'end_month', 
            'is_deleted', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class StudentSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()
    academic_department = AcademicDepartmentSimpleSerializer()
    admission_semester = AcademicSemesterSimpleSerializer()
    class Meta:
        model= Student
        fields = [
            'id',
            'student_id',
            'user', 
            'academic_department',
            'admission_semester', 
            'gender',
            'date_of_birth',
            'contact_no',
            'emergency_contact_no',
            'present_address',
            'permanent_address',
            'guardian_number',
            'profile_image',
            'is_deleted',
            'created_at',
            'updated_at',
        ]
    read_only_fields = ['student_id', 'created_at', 'updated_at']
    