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



class EnrollmentBusinessLogicTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        # کاربران
        self.admin = User.objects.create_user(username='admin', password='123', role='ADMIN')
        self.student = User.objects.create_user(username='student', password='123', role='STUDENT')
        self.prof = User.objects.create_user(username='prof', password='123', role='PROFESSOR')
        
        # درس‌ها
        self.prereq = Course.objects.create(code="PR", name="پیش‌نیاز", units=3, capacity=30, professor="دکتر الف", day="شنبه", time="۸-۱۰")
        self.main = Course.objects.create(code="MAIN", name="درس اصلی", units=3, capacity=2, professor="دکتر ب", day="شنبه", time="۱۰-۱۲")
        self.conflict = Course.objects.create(code="CONF", name="تداخلی", units=3, capacity=30, professor="دکتر ج", day="شنبه", time="۱۱-۱۳")
        self.full = Course.objects.create(code="FULL", name="پر", units=3, capacity=1, professor="دکتر د", day="یکشنبه", time="۸-۱۰")
        
        # پیش‌نیاز
        Prerequisite.objects.create(course=self.main, prerequisite_course=self.prereq)

    def test_prerequisite_required(self):
        self.client.force_authenticate(self.student)
        response = self.client.post('/api/enrollments/', {'course_id': self.main.id})
        self.assertEqual(response.status_code, 400)
        self.assertIn('پیش‌نیاز', response.data['detail'])

    def test_capacity_full(self):
        EnrolledCourse.objects.create(student=self.student, course=self.full)
        another = User.objects.create_user(username='s2', password='123', role='STUDENT')
        self.client.force_authenticate(another)
        response = self.client.post('/api/enrollments/', {'course_id': self.full.id})
        self.assertEqual(response.status_code, 400)
        self.assertIn('ظرفیت', response.data['detail'])

    def test_time_conflict(self):
        self.client.force_authenticate(self.student)
        self.client.post('/api/enrollments/', {'course_id': self.main.id})
        response = self.client.post('/api/enrollments/', {'course_id': self.conflict.id})
        self.assertEqual(response.status_code, 400)
        self.assertIn('تداخل زمانی', response.data['detail'])

    def test_duplicate_enrollment(self):
        self.client.force_authenticate(self.student)
        self.client.post('/api/enrollments/', {'course_id': self.main.id})
        response = self.client.post('/api/enrollments/', {'course_id': self.main.id})
        self.assertEqual(response.status_code, 400)
        self.assertIn('قبلاً اخذ شده', response.data['detail'])

    def test_max_unit_limit(self):
        heavy = Course.objects.create(code="HEAVY", name="سنگین", units=18, capacity=30, professor="دکتر ه", day="دوشنبه", time="۸-۱۰")
        self.client.force_authenticate(self.student)
        self.client.post('/api/enrollments/', {'course_id': heavy.id})
        response = self.client.post('/api/enrollments/', {'course_id': self.main.id})  # 18+3=21 > 20
        self.assertEqual(response.status_code, 400)
        self.assertIn('حداکثر واحد', response.data['detail'])

    def test_professor_sees_students(self):
        EnrolledCourse.objects.create(student=self.student, course=self.main)
        self.main.professor = self.prof.username
        self.main.save()
        self.client.force_authenticate(self.prof)
        response = self.client.get(f'/api/my-courses/{self.main.id}/students/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_admin_add_prerequisite(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(f'/api/courses/{self.main.id}/prerequisites/', {'prerequisite_course_id': self.prereq.id})
        self.assertEqual(response.status_code, 201)

    def test_student_cannot_add_prerequisite(self):
        self.client.force_authenticate(self.student)
        response = self.client.post(f'/api/courses/{self.main.id}/prerequisites/', {'prerequisite_course_id': self.prereq.id})
        self.assertEqual(response.status_code, 403)