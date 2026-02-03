from django.urls import path

from .views import (
    AdminCourseDetailView,
    AdminCourseListCreateView,
    AdminLoginView,
    AdminUnitLimitView,
    CourseListView,
    ProfessorCoursePdfView,
    ProfessorCourseStudentsView,
    ProfessorCoursesView,
    ProfessorLoginView,
    StudentCourseDeleteView,
    StudentCourseListCreateView,
    StudentLoginView,
    StudentScheduleView,
)

urlpatterns = [
    # احراز هویت
    path("auth/admin/login/", AdminLoginView.as_view(), name="admin-login"),
    path("auth/student/login/", StudentLoginView.as_view(), name="student-login"),
    path("auth/professor/login/", ProfessorLoginView.as_view(), name="professor-login"),
    # مدیر - دروس
    path("admin/courses", AdminCourseListCreateView.as_view(), name="admin-courses"),
    path(
        "admin/courses/<int:id>",
        AdminCourseDetailView.as_view(),
        name="admin-course-detail",
    ),
    # مدیر - حدود واحد
    path(
        "admin/unit-limits",
        AdminUnitLimitView.as_view(),
        name="admin-unit-limits",
    ),
    # لیست عمومی دروس برای دانشجو
    path("courses", CourseListView.as_view(), name="courses-list"),
    # انتخاب واحد دانشجو
    path(
        "student/courses",
        StudentCourseListCreateView.as_view(),
        name="student-courses",
    ),
    path(
        "student/courses/<int:course_id>",
        StudentCourseDeleteView.as_view(),
        name="student-course-delete",
    ),
    path(
        "student/schedule",
        StudentScheduleView.as_view(),
        name="student-schedule",
    ),
    # استاد
    path(
        "professor/courses",
        ProfessorCoursesView.as_view(),
        name="professor-courses",
    ),
    path(
        "professor/courses/<int:course_id>/students",
        ProfessorCourseStudentsView.as_view(),
        name="professor-course-students",
    ),
    path(
        "professor/courses/<int:course_id>/students/<int:student_id>",
        ProfessorCourseStudentsView.as_view(),
        name="professor-course-student-delete",
    ),
    path(
        "professor/courses/<int:course_id>/pdf",
        ProfessorCoursePdfView.as_view(),
        name="professor-course-pdf",
    ),
]


