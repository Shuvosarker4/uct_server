from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from student.models import Student
from .models import Admin
from django.contrib.auth import get_user_model
from django.db import transaction


User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    password = serializers.CharField(write_only=True, required=False,style={'input_type': 'password'})
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','email','password','first_name','last_name','role']

        read_only_fields = ['role', 'created_at', 'updated_at']

    def validate(self, attrs):
        password = attrs.get('password') or 'testUser'
        attrs['password'] = password
        return attrs

class CreateStudentSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()
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
            'created_at',
            'updated_at',
        ]
    read_only_fields = ['student_id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        with transaction.atomic():
            print(validated_data)
            user_data = validated_data.pop('user')
            user_data['role'] = 'student'
            user = User.objects.create_user(**user_data)
            user.save()
            student = Student.objects.create(user=user, **validated_data)
            return student



class AdminSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    management_department_name = serializers.StringRelatedField(
        source='management_department', 
        read_only=True
    )
    
    class Meta:
        model = Admin
        fields = [
            'id', 
            'user',  
            'user_name', 
            'designation',
            'gender',
            'date_of_birth',
            'contact_no',
            'emergency_contact_no',
            'present_address',
            'permanent_address',
            'profile_image',
            'management_department',
            'management_department_name',
            'is_deleted',
            'created_at',
            'updated_at',
        ]
        
        read_only_fields = [
            'id', 
            'user_name', 
            'management_department_name',
            'created_at', 
            'updated_at'
        ]

    def create(self, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            user_data['role'] = 'admin'
            user = User.objects.create_user(**user_data)
            user.is_staff = True
            user.save()
            admin = Admin.objects.create(user=user, **validated_data)
            return admin

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name ='CustomUser'
        fields = ['id','email','first_name','last_name','role']