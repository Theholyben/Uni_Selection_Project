from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Course, Enrollment, UnitLimit, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "role", "major"]


class CourseSerializer(serializers.ModelSerializer):
    """
    سریالایزر اصلی درس که با فرانت هم‌نام‌سازی شده است.
    """

    professor = serializers.CharField(source="professor_name", allow_blank=True, required=False)
    schedule = serializers.ListField(
        child=serializers.CharField(), source="schedule_days", required=False
    )
    currentStudents = serializers.IntegerField(source="current_students", read_only=True)
    title = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "title",
            "code",
            "professor",
            "capacity",
            "time",
            "units",
            "location",
            "prerequisite",
            "schedule",
            "currentStudents",
        ]


class UnitLimitSerializer(serializers.ModelSerializer):
    minUnits = serializers.IntegerField(source="min_units")
    maxUnits = serializers.IntegerField(source="max_units")

    class Meta:
        model = UnitLimit
        fields = ["minUnits", "maxUnits"]


class EnrollmentSerializer(serializers.ModelSerializer):
    """
    برای برگرداندن لیست دروس انتخاب‌شده توسط دانشجو
    """

    id = serializers.IntegerField(source="course.id", read_only=True)
    code = serializers.CharField(source="course.code", read_only=True)
    name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "code", "name"]


class RoleLoginSerializer(serializers.Serializer):
    """
    لاگین ساده بر اساس نقش (ادمین / استاد / دانشجو)
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        self.required_role = kwargs.pop("required_role", None)
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("نام کاربری یا رمز عبور نادرست است.")

        if self.required_role and getattr(user, "role", None) != self.required_role:
            raise serializers.ValidationError("شما مجوز ورود با این نقش را ندارید.")

        attrs["user"] = user
        return attrs


