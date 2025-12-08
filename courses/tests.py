from rest_framework.test import APITestCase
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer


class CourseSerializerTest(APITestCase):
    def test_code_less_than_2_digits(self):
        data = {
            "code": "1",
            "name": "DB Lab",
            "capacity": 12,
            "professor": "Dr. Jaderian",
            "day": "Saturday",
            "time": "8-10",
            "location": "Lab 4",
            "units": 1
        }
        serializer = CourseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("code", serializer.errors)

    def test_code_more_than_7_digits(self):
        data = {
            "code": "12345678",
            "name": "DB Lab",
            "capacity": 12,
            "professor": "Dr. Jaderian",
            "day": "Saturday",
            "time": "8-10",
            "location": "Lab 4",
            "units": 1
        }
        serializer = CourseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("code", serializer.errors)

    def test_negative_capacity(self):
        data = {
            "code": "123456",
            "name": "DB Lab",
            "capacity": -12,
            "professor": "Dr. Jaderian",
            "day": "Saturday",
            "time": "8-10",
            "location": "Lab 4",
            "units": 1
        }
        serializer = CourseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("capacity", serializer.errors)

    def test_invalid_units(self):
        data = {
            "code": "123456",
            "name": "DB Lab",
            "capacity": 12,
            "professor": "Dr. Jaderian",
            "day": "Saturday",
            "time": "8-10",
            "location": "Lab 4",
            "units": 4
        }
        serializer = CourseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("units", serializer.errors)

    def test_duplicate_code(self):
        Course.objects.create(
            code="123456",
            name="Math",
            capacity=20,
            professor="Dr. Araghi",
            day="Monday , Wednesday",
            time="10-12",
            location="Class 203",
            units=3
        )

        data = {
            "code": "123456",
            "name": "DB Lab",
            "capacity": 12,
            "professor": "Dr. Jaderian",
            "day": "Saturday",
            "time": "8-10",
            "location": "Lab 4",
            "units": 1
        }
        serializer = CourseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("code", serializer.errors)


class CourseAPITest(APITestCase):
    def test_create_course_api(self):
        data = {
            "code": "123456",
            "name": "DB Lab",
            "capacity": 12,
            "professor": "Dr. Jaderian",
            "day": "Saturday",
            "time": "8-10",
            "location": "Lab 4",
            "units": 1
        }
        response = self.client.post('/api/courses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
