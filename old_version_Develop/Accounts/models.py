from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'ADMIN'),
        ('STUDENT', 'STUSENT'),
        ('PROFESSOR', 'PROFESSOR'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='STUDENT',        
    )

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_student(self):
        return self.role == 'STUDENT'

    def is_professor(self):
        return self.role == 'PROFESSOR'

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"