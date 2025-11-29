from rest_framework import serializers
from .models import Course


def validate_prerequisites(value):
    ids = [course.id for course in value]

    if None in ids:
        raise serializers.ValidationError("Invalid prerequisite course.")

    existing = Course.objects.filter(id__in=ids).count()

    if existing != len(ids):
        raise serializers.ValidationError("One or more prerequisite courses do not exist.")

    return value


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate_code(self, value):
        if not value.strip():
            raise serializers.ValidationError("Course code cannot be empty.")

        if not value.isdigit():
            raise serializers.ValidationError("Course code must be a number")

        if len(value) < 2 or len(value) > 7:
            raise serializers.ValidationError("Course code must be between 1 and 8 digits")

        if Course.objects.filter(code=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Course code must be unique.")

        return value

    def validate_capacity(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Capacity must be an integer")
        if value < 0:
            raise serializers.ValidationError("Capacity cannot be negative")
        return value

    def validate_units(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Units must be an integer")
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("Units must be 1, 2 or 3")
        return value

    def validate(self, attrs):
        return attrs
