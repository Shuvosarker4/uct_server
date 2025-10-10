from rest_framework.viewsets import ModelViewSet
from student.models import Faculty,Student,AcademicFaculty
from student.serializers import AcademicFacultySerializer,FacultySerializer
from .serializers import CreateStudentSerializer,AdminSerializer
from .models import Admin
from rest_framework.viewsets import ModelViewSet

class AdminViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    
class CreateStudentViewSet(ModelViewSet):
    http_method_names = ['post']
    queryset = Student.objects.all()
    serializer_class =CreateStudentSerializer


class AcademicFacultyViewSet(ModelViewSet):
    queryset = AcademicFaculty.objects.all()
    serializer_class = AcademicFacultySerializer 

class FacultyViewSet(ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer  