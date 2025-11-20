from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField(default=0)
    professor = models.CharField(max_length=150)
    day = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    min_units = models.PositiveIntegerField(default=1)
    max_units = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"{self.code} - {self.name}"
