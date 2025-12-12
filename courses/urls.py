from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'my-courses', ProfessorCourseViewSet, basename='my-courses')

urlpatterns = [
    path('', include(router.urls)),
]