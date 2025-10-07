from rest_framework.viewsets import ModelViewSet
from .serializers import StudentSerializer,AcademicDepartmentSerializer,AcademicFacultySerializer,AcademicSemesterSerializer
from .models import Student,AcademicSemester,AcademicDepartment,AcademicFaculty
# Create your views here.

class DepartmentViewSet(ModelViewSet):
    queryset = AcademicDepartment.objects.all()
    serializer_class = AcademicDepartmentSerializer

class SemesterViewSet(ModelViewSet):
    queryset = AcademicSemester.objects.all()
    serializer_class = AcademicSemesterSerializer

class StudentViewSet(ModelViewSet):
    http_method_names = ['get', 'head', 'options']
    queryset = Student.objects.all()
    serializer_class =StudentSerializer
    