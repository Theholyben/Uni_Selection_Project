from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet
from .views import EnrollmentViewSet
from .views import ProfessorCourseViewSet
from rest_framework_nested.routers import NestedDefaultRouter
from .views import CourseViewSet, EnrollmentViewSet, ProfessorCourseViewSet

router = DefaultRouter()

router.register(r'courses', CourseViewSet, basename='course')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')  
router.register(r'my-courses', ProfessorCourseViewSet, basename='my-courses')

courses_router = NestedDefaultRouter(router, r'courses', lookup='course')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
]