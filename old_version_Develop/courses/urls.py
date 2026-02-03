from django.urls import path
from . import views

urlpatterns = [
    path('api/courses/', views.course_list, name='course-list'),
]
