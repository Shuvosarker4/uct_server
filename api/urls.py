
from django.urls import path,include
from rest_framework_nested import routers
from student.views import StudentViewSet,DepartmentViewSet,SemesterViewSet
from users.views import FacultyViewSet,AdminViewSet
from users.views import CreateStudentViewSet
router = routers.DefaultRouter()
router.register('students',StudentViewSet,basename='students')
router.register('users/create-student',CreateStudentViewSet,basename='create-students')
router.register('users/create-faculty',FacultyViewSet,basename='faculties')
router.register('users/create-admin',AdminViewSet,basename='admins')
router.register('users/create-department',DepartmentViewSet,basename='departments')
router.register('users/create-semester',SemesterViewSet,basename='semesters')

urlpatterns = [
   path('',include(router.urls)),
]