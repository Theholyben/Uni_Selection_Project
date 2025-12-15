from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField(default=0)
    professor = models.CharField(max_length=150, blank=True)
    day = models.CharField(max_length=100, blank=True)
    time = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    units = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.code} - {self.name}"



class Prerequisite(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_prerequisites')
    prerequisite = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='required_for')
    
    class Meta:
        unique_together = ('course', 'prerequisite')

class EnrolledCourse(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'course')


class UnitLimit(models.Model):
    min_units = models.PositiveIntegerField(default=12)
    max_units = models.PositiveIntegerField(default=20)
    
    def __str__(self):
        return f"حداقل {self.min_units} - حداکثر {self.max_units} واحد"        