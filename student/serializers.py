from rest_framework import serializers
from .models import Faculty, Student,AcademicDepartment,AcademicFaculty,AcademicSemester
from users.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.db import transaction

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
    

class FacultySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    academic_faculty_name = serializers.CharField(source='academic_faculty.name', read_only=True)
    academic_department_name = serializers.CharField(source='academic_department.name', read_only=True)
    academic_department_code = serializers.CharField(source='academic_department.code', read_only=True)
    user = UserCreateSerializer()

    class Meta:
        model = Faculty
        fields = [
            'id',
            'faculty_id',
            'user',
            'email',
            'designation',
            'academic_faculty',
            'academic_faculty_name',
            'academic_department',
            'academic_department_name',
            'academic_department_code',
            'gender',
            'date_of_birth',
            'contact_no',
            'emergency_contact_no',
            'present_address',
            'permanent_address',
            'profile_image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['faculty_id', 'email', 'created_at', 'updated_at']
   
    def create(self, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            user_data['role'] = 'faculty'
            user = User.objects.create_user(**user_data)
            user.is_staff = True
            user.save()
            admin = Faculty.objects.create(user=user, **validated_data)
            return admin