from django.urls import path
from . import views

urlpatterns = [
    path('api/auth/login/', views.login_view, name='login'),
    path('api/auth/student/login/', views.student_login, name='student-login'),
    path('api/auth/professor/login/', views.professor_login, name='professor-login'),
]

