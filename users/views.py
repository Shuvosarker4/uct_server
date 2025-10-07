from rest_framework.viewsets import ModelViewSet
from student.models import Student,AcademicFaculty
from student.serializers import AcademicFacultySerializer
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


class FacultyViewSet(ModelViewSet):
    queryset = AcademicFaculty.objects.all()
    serializer_class = AcademicFacultySerializer  