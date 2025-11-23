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

    # FIELD-LEVEL VALIDATIONS
    def validate_code(self, value):
        if not value.strip():
            raise serializers.ValidationError("Course code cannot be empty.")

        # unique check
        if Course.objects.filter(code=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Course code must be unique.")

        return value

    # OBJECT-LEVEL VALIDATION

    def validate(self, attrs):
        min_units = attrs.get("min_units")
        max_units = attrs.get("max_units")

        if min_units is None or max_units is None:
            raise serializers.ValidationError("min_units and max_units fields are required.")

        if min_units > max_units:
            raise serializers.ValidationError({
                "min_units": "Minimum units cannot be greater than maximum units."
            })

        return attrs
