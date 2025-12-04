from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField(default=0)
    professor = models.CharField(max_length=150, blank=True)
    day = models.CharField(max_length=100, blank=True)
    time = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
