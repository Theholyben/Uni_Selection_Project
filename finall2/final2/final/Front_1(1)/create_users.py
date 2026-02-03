#!/usr/bin/env python
"""اسکریپت ایجاد کاربران نمونه برای تست"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import User, Course, Enrollment

# حذف کاربران قبلی (اگر وجود دارند)
User.objects.filter(username__in=['admin', 'student', 'professor']).delete()
# حذف دانشجویان نمونه قبلی
User.objects.filter(role='STUDENT', username__startswith='student').delete()

# حذف دروس قبلی استاد (اگر وجود دارند)
Course.objects.filter(professor_name__icontains='رضایی').delete()

# ایجاد مدیر
admin = User.objects.create_user(
    username='admin',
    password='admin123',
    role='ADMIN',
    email='admin@university.ir',
    first_name='مدیر',
    last_name='سیستم'
)
admin.is_staff = True
admin.is_superuser = True
admin.save()
print(f'✓ مدیر ساخته شد: username=admin, password=admin123')

# ایجاد دانشجویان نمونه
students_data = [
    {
        'username': 'student',
        'password': 'student123',
        'first_name': 'علی',
        'last_name': 'احمدی',
        'email': 'student@university.ir',
        'major': 'مهندسی کامپیوتر'
    },
    {
        'username': 'student1',
        'password': 'student123',
        'first_name': 'محمد',
        'last_name': 'کریمی',
        'email': 'student1@university.ir',
        'major': 'مهندسی کامپیوتر'
    },
    {
        'username': 'student2',
        'password': 'student123',
        'first_name': 'فاطمه',
        'last_name': 'محمدی',
        'email': 'student2@university.ir',
        'major': 'مهندسی نرم‌افزار'
    },
    {
        'username': 'student3',
        'password': 'student123',
        'first_name': 'حسین',
        'last_name': 'رضایی',
        'email': 'student3@university.ir',
        'major': 'مهندسی کامپیوتر'
    },
    {
        'username': 'student4',
        'password': 'student123',
        'first_name': 'زهرا',
        'last_name': 'حسینی',
        'email': 'student4@university.ir',
        'major': 'مهندسی نرم‌افزار'
    },
    {
        'username': 'student5',
        'password': 'student123',
        'first_name': 'امیر',
        'last_name': 'نوری',
        'email': 'student5@university.ir',
        'major': 'مهندسی کامپیوتر'
    },
    {
        'username': 'student6',
        'password': 'student123',
        'first_name': 'سارا',
        'last_name': 'احمدی',
        'email': 'student6@university.ir',
        'major': 'مهندسی نرم‌افزار'
    },
    {
        'username': 'student7',
        'password': 'student123',
        'first_name': 'رضا',
        'last_name': 'موسوی',
        'email': 'student7@university.ir',
        'major': 'مهندسی کامپیوتر'
    }
]

students = []
for student_data in students_data:
    student = User.objects.create_user(
        username=student_data['username'],
        password=student_data['password'],
        role='STUDENT',
        email=student_data['email'],
        first_name=student_data['first_name'],
        last_name=student_data['last_name'],
        major=student_data.get('major', '')
    )
    students.append(student)
    print(f'✓ دانشجو ساخته شد: {student_data["first_name"]} {student_data["last_name"]} ({student_data["username"]})')

# ایجاد استاد
professor = User.objects.create_user(
    username='professor',
    password='professor123',
    role='PROFESSOR',
    email='professor@university.ir',
    first_name='دکتر',
    last_name='رضایی'
)
print(f'✓ استاد ساخته شد: username=professor, password=professor123')

# ایجاد دروس نمونه برای استاد
professor_name = f"{professor.first_name} {professor.last_name}".strip()

courses_data = [
    {
        'name': 'برنامه‌نویسی پیشرفته',
        'code': 'CS301',
        'professor_name': professor_name,
        'capacity': 40,
        'time': '08:00-10:00',
        'units': 3,
        'location': 'سالن 101',
        'prerequisite': '',
        'schedule_days': ['شنبه', 'دوشنبه']
    },
    {
        'name': 'پایگاه داده',
        'code': 'CS302',
        'professor_name': professor_name,
        'capacity': 35,
        'time': '10:00-12:00',
        'units': 3,
        'location': 'سالن 205',
        'prerequisite': 'CS201',
        'schedule_days': ['یکشنبه', 'سه‌شنبه']
    },
    {
        'name': 'هوش مصنوعی',
        'code': 'CS401',
        'professor_name': professor_name,
        'capacity': 30,
        'time': '14:00-16:00',
        'units': 3,
        'location': 'آمفی‌تئاتر مرکزی',
        'prerequisite': 'CS301',
        'schedule_days': ['شنبه', 'چهارشنبه']
    },
    {
        'name': 'شبکه‌های کامپیوتری',
        'code': 'CS303',
        'professor_name': professor_name,
        'capacity': 45,
        'time': '16:00-18:00',
        'units': 3,
        'location': 'سالن 302',
        'prerequisite': '',
        'schedule_days': ['دوشنبه', 'چهارشنبه']
    }
]

# ایجاد دروس و ثبت‌نام دانشجویان
courses = []
for course_data in courses_data:
    course = Course.objects.create(**course_data)
    courses.append(course)
    print(f'✓ درس "{course.name}" ({course.code}) برای استاد ایجاد شد')

# حذف ثبت‌نام‌های قبلی
Enrollment.objects.all().delete()

# ثبت‌نام دانشجویان در دروس
# CS301 - برنامه‌نویسی پیشرفته: 5 دانشجو
enrollments_cs301 = [
    (students[0], courses[0]),  # علی احمدی
    (students[1], courses[0]),  # محمد کریمی
    (students[2], courses[0]),  # فاطمه محمدی
    (students[3], courses[0]),  # حسین رضایی
    (students[4], courses[0]),  # زهرا حسینی
]

# CS302 - پایگاه داده: 4 دانشجو
enrollments_cs302 = [
    (students[0], courses[1]),  # علی احمدی
    (students[1], courses[1]),  # محمد کریمی
    (students[5], courses[1]),  # امیر نوری
    (students[6], courses[1]),  # سارا احمدی
]

# CS401 - هوش مصنوعی: 3 دانشجو
enrollments_cs401 = [
    (students[0], courses[2]),  # علی احمدی
    (students[2], courses[2]),  # فاطمه محمدی
    (students[3], courses[2]),  # حسین رضایی
]

# CS303 - شبکه‌های کامپیوتری: 6 دانشجو
enrollments_cs303 = [
    (students[1], courses[3]),  # محمد کریمی
    (students[2], courses[3]),  # فاطمه محمدی
    (students[4], courses[3]),  # زهرا حسینی
    (students[5], courses[3]),  # امیر نوری
    (students[6], courses[3]),  # سارا احمدی
    (students[7], courses[3]),  # رضا موسوی
]

all_enrollments = enrollments_cs301 + enrollments_cs302 + enrollments_cs401 + enrollments_cs303

for student, course in all_enrollments:
    Enrollment.objects.get_or_create(student=student, course=course)

print(f'\n✓ {len(all_enrollments)} ثبت‌نام انجام شد:')
print(f'   - برنامه‌نویسی پیشرفته (CS301): {len(enrollments_cs301)} دانشجو')
print(f'   - پایگاه داده (CS302): {len(enrollments_cs302)} دانشجو')
print(f'   - هوش مصنوعی (CS401): {len(enrollments_cs401)} دانشجو')
print(f'   - شبکه‌های کامپیوتری (CS303): {len(enrollments_cs303)} دانشجو')

print('\n✅ همه کاربران، دروس و ثبت‌نام‌ها با موفقیت ساخته شدند!')
print('\n📝 اطلاعات ورود:')
print('   مدیر:    admin / admin123')
print('   دانشجو:  student / student123 (یا student1 تا student7)')
print('   استاد:   professor / professor123')
print(f'\n📚 تعداد دروس ایجاد شده برای استاد: {len(courses_data)}')
print(f'👥 تعداد دانشجویان نمونه: {len(students)}')
