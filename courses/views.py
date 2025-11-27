from rest_framework.viewsets import ModelViewSet
#from rest_framework.permissions import IsAdminUser
from .models import Course
from .serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    #permission_classes = [IsAdminUser]
