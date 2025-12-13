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
        course_id = request.data.get('course_id')
        course = Course.objects.get(id=course_id)
        student = request.user
        
        missing_prereqs = course.prerequisites.exclude(id__in=student.enrollments.filter(course__grade__gte=10).values('course_id'))
        if missing_prereqs.exists():
            return Response({"detail": "پیش‌نیازها کامل نشده"}, status=400)
        
        if course.enrollments.count() >= course.capacity:
            return Response({"detail": "ظرفیت کلاس پر شده"}, status=400)
        
        if EnrolledCourse.objects.filter(student=student, course=course).exists():
            return Response({"detail": "این درس قبلاً اخذ شده"}, status=400)
        
        current_units = student.enrollments.aggregate(total=Sum('course__units'))['total'] or 0
        if current_units + course.units > UnitLimit.objects.first().max_units:
            return Response({"detail": "حداکثر واحد مجاز"}, status=400)
        
        enrollment = EnrolledCourse.objects.create(student=student, course=course)
        return Response({"detail": "درس با موفقیت اخذ شد"}, status=201)