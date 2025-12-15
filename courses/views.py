from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from .models import Course
from .serializers import CourseSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets



class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]




class EnrollmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EnrolledCourse.objects.filter(student=self.request.user)

@action(detail=False, methods=['get'])
def schedule(self, request):
        enrollments = self.get_queryset()
        schedule = {}
        
        for enrollment in enrollments:
            course = enrollment.course
            day = course.day or "نامشخص"
            time = course.time or "نامشخص"
            name = course.name
            
            if day not in schedule:
                schedule[day] = []
            schedule[day].append(f"{name} ({time})")
        
        ordered_days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]
        ordered_schedule = {day: schedule.get(day, []) for day in ordered_days if day in schedule}
        
        return Response(ordered_schedule)


def create(self, request):
 def parse_time(time_str):
    if '-' in time_str:
        start_str = time_str.split('-')[0].strip()
        return int(start_str.replace(':', '')) if ':' in start_str else int(start_str) * 100
    return 0

 def has_time_conflict(student, new_course):
    new_day = new_course.day
    new_time = new_course.time  
    new_start = parse_time(new_time)
    
    enrolled_courses = EnrolledCourse.objects.filter(student=student).select_related('course')
    
    for enrolled in enrolled_courses:
        existing = enrolled.course
        if existing.day == new_day:
            existing_start = parse_time(existing.time)
            if abs(existing_start - new_start) < 200:  
                return True, existing
    return False, None

# استفاده
 has_conflict, conflicting_course = has_time_conflict(student, course)
 if has_conflict:
    return Response({
        "detail": f"تداخل زمانی با درس '{conflicting_course.name}' در روز {new_day} ساعت {conflicting_course.time}"
    }, status=400)

class ProfessorCourseViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Course.objects.filter(professor=self.request.user.username)
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        course = self.get_object()
        students = course.enrollments.select_related('student')
        serializer = UserSerializer([e.student for e in students], many=True)
        return Response(serializer.data)