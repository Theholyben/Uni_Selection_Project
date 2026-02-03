from collections import defaultdict

from django.db.models import Sum
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Course, Enrollment, UnitLimit, User
from .permissions import IsAdminUserRole, IsProfessorUserRole, IsStudentUserRole
from .serializers import (
    CourseSerializer,
    EnrollmentSerializer,
    RoleLoginSerializer,
    UnitLimitSerializer,
    UserSerializer,
)


# ---------- احراز هویت ----------


def _build_jwt_response(user: User) -> Response:
    refresh = RefreshToken.for_user(user)
    data = {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": UserSerializer(user).data,
    }
    return Response(data, status=status.HTTP_200_OK)


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RoleLoginSerializer(
            data=request.data, required_role=User.Roles.ADMIN
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return _build_jwt_response(user)


class StudentLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RoleLoginSerializer(
            data=request.data, required_role=User.Roles.STUDENT
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return _build_jwt_response(user)


class ProfessorLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RoleLoginSerializer(
            data=request.data, required_role=User.Roles.PROFESSOR
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return _build_jwt_response(user)


# ---------- مدیریت دروس توسط مدیر ----------


class AdminCourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all().order_by("code")
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]


class AdminCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    lookup_field = "id"


class AdminUnitLimitView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get(self, request):
        obj = UnitLimit.objects.first()
        if not obj:
            obj = UnitLimit.objects.create()
        data = UnitLimitSerializer(obj).data
        return Response(data)

    def post(self, request):
        obj = UnitLimit.objects.first()
        if not obj:
            obj = UnitLimit.objects.create()
        serializer = UnitLimitSerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ---------- لیست دروس برای همه دانشجویان ----------


class CourseListView(generics.ListAPIView):
    """
    /api/courses
    لیست همه دروس برای نمایش به دانشجو (و قابل استفاده برای جستجو در فرانت)
    """

    queryset = Course.objects.all().order_by("code")
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


# ---------- انتخاب واحد دانشجو ----------


class StudentCourseListCreateView(APIView):
    """
    GET /api/student/courses       -> لیست دروس انتخاب‌شده
    POST /api/student/courses      -> افزودن درس جدید با { "courseId": 1 }
    """

    permission_classes = [IsAuthenticated, IsStudentUserRole]

    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user).select_related(
            "course"
        )
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    def post(self, request):
        course_id = request.data.get("courseId")
        course_code = request.data.get("courseCode")
        
        # اگر courseId ارسال شده، از آن استفاده کن (می‌تواند عدد یا رشته باشد)
        # اگر courseCode ارسال شده، از آن استفاده کن
        identifier = course_id or course_code
        
        if not identifier:
            return Response(
                {"message": "courseId یا courseCode الزامی است"}, status=status.HTTP_400_BAD_REQUEST
            )

        # تلاش برای یافتن درس: ابتدا به عنوان ID (اگر عدد باشد)، سپس به عنوان code
        course = None
        
        # اگر عدد است، ابتدا به عنوان ID جستجو کن
        if isinstance(identifier, (int, str)) and str(identifier).strip().isdigit():
            try:
                course = Course.objects.get(id=int(identifier))
            except (Course.DoesNotExist, ValueError, TypeError):
                # اگر با ID پیدا نشد، ادامه می‌دهیم تا با code جستجو کنیم
                pass
        
        # اگر پیدا نشد یا عدد نبود، به عنوان code جستجو کن
        if not course:
            try:
                course = Course.objects.get(code=str(identifier).strip())
            except Course.DoesNotExist:
                return Response(
                    {"message": "درس مورد نظر یافت نشد"}, status=status.HTTP_404_NOT_FOUND
                )

        student = request.user

        # تکراری نبودن
        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response(
                {"message": "این درس قبلاً انتخاب شده است"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # کنترل ظرفیت
        if course.current_students >= course.capacity:
            return Response(
                {"message": "ظرفیت درس تکمیل شده است"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # کنترل سقف واحد
        limit = UnitLimit.objects.first()
        if limit:
            current_units = (
                Enrollment.objects.filter(student=student)
                .aggregate(total=Sum("course__units"))
                .get("total")
                or 0
            )
            if current_units + course.units > limit.max_units:
                return Response(
                    {
                        "message": "تعداد واحدهای انتخاب‌شده از حداکثر مجاز بیشتر می‌شود",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # کنترل ساده پیش‌نیاز: اگر کدی در فیلد prerequisite ثبت شده،
        # دانشجو باید درسی با همان کد را قبلاً اخذ کرده باشد.
        if course.prerequisite:
            has_prereq = Enrollment.objects.filter(
                student=student, course__code=course.prerequisite
            ).exists()
            if not has_prereq:
                return Response(
                    {"message": "پیش‌نیاز این درس را پاس نکرده‌اید"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        Enrollment.objects.create(student=student, course=course)
        return Response(
            {"message": "درس با موفقیت اضافه شد"}, status=status.HTTP_201_CREATED
        )


class StudentCourseDeleteView(APIView):
    """
    DELETE /api/student/courses/<course_id>
    """

    permission_classes = [IsAuthenticated, IsStudentUserRole]

    def delete(self, request, course_id: int):
        student = request.user
        try:
            enrollment = Enrollment.objects.get(student=student, course_id=course_id)
        except Enrollment.DoesNotExist:
            return Response(
                {"message": "این درس برای شما ثبت نشده است"},
                status=status.HTTP_404_NOT_FOUND,
            )

        enrollment.delete()
        return Response({"message": "درس با موفقیت حذف شد"})


# ---------- برنامه هفتگی دانشجو ----------


class StudentScheduleView(APIView):
    """
    /api/student/schedule
    خروجی مطابق ساختار مورد انتظار weekly-schedule.html
    """

    permission_classes = [IsAuthenticated, IsStudentUserRole]

    DAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه"]

    def get(self, request):
        enrollments = (
            Enrollment.objects.filter(student=request.user)
            .select_related("course")
            .order_by("course__time")
        )

        if not enrollments.exists():
            return Response(
                {
                    "timeSlots": [],
                    "scheduleGrid": [],
                }
            )

        # لیست همه بازه‌های زمانی موجود
        time_slots = sorted(
            {
                e.course.time or "نامشخص"
                for e in enrollments
                if (e.course.schedule_days or [])
            }
        )

        # ساخت grid: [day_index][time_index] -> {"courses": [...]}
        # ابتدا یک ساختار خالی می‌سازیم
        schedule_grid = [
            [{"courses": []} for _ in range(len(time_slots))]
            for _ in range(len(self.DAYS))
        ]

        time_index_map = {t: idx for idx, t in enumerate(time_slots)}
        day_index_map = {d: idx for idx, d in enumerate(self.DAYS)}

        for enrollment in enrollments:
            course = enrollment.course
            time_label = course.time or "نامشخص"
            t_idx = time_index_map.get(time_label)
            if t_idx is None:
                continue

            for day in course.schedule_days or []:
                d_idx = day_index_map.get(day)
                if d_idx is None:
                    continue

                course_data = {
                    "code": course.code,
                    "title": course.name,
                    "units": course.units,
                    "professor": course.professor_name or "نامشخص",
                    "location": course.location or "نامشخص",
                    "scheduleTimes": [time_label],
                }
                schedule_grid[d_idx][t_idx]["courses"].append(course_data)

        return Response(
            {
                "timeSlots": time_slots,
                "scheduleGrid": schedule_grid,
            }
        )


# ---------- بخش استاد ----------


class ProfessorCoursesView(APIView):
    """
    GET /api/professor/courses
    لیست دروس ارائه شده توسط استاد
    """

    permission_classes = [IsAuthenticated, IsProfessorUserRole]

    def get(self, request):
        professor_name = (
            f"{request.user.first_name} {request.user.last_name}".strip()
            or request.user.username
        )
        courses = Course.objects.filter(professor_name=professor_name)

        data_courses = []
        for course in courses:
            # تبدیل schedule_days و time به ساختار مورد انتظار
            schedule_items = []
            if course.schedule_days:
                time_label = course.time or ""
                start_time = ""
                end_time = ""
                if "-" in time_label:
                    parts = time_label.split("-")
                    start_time = parts[0].strip()
                    end_time = parts[1].strip() if len(parts) > 1 else ""
                for day in course.schedule_days:
                    schedule_items.append(
                        {"day": day, "startTime": start_time, "endTime": end_time}
                    )

            data_courses.append(
                {
                    "id": course.id,
                    "name": course.name,
                    "location": course.location or "نامشخص",
                    "capacity": course.capacity,
                    "enrolledCount": course.current_students,
                    "schedule": schedule_items,
                }
            )

        return Response(
            {
                "semester": "نیمسال اول ۱۴۰۴",
                "courses": data_courses,
            }
        )


class ProfessorCourseStudentsView(APIView):
    """
    GET    /api/professor/courses/<course_id>/students
    DELETE /api/professor/courses/<course_id>/students/<student_id>
    """

    permission_classes = [IsAuthenticated, IsProfessorUserRole]

    def get(self, request, course_id: int):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"message": "درس یافت نشد"}, status=status.HTTP_404_NOT_FOUND
            )

        enrollments = Enrollment.objects.filter(course=course).select_related("student")
        students_data = []
        for e in enrollments:
            s = e.student
            full_name = (s.get_full_name() or s.username).strip()
            students_data.append(
                {
                    "id": s.id,
                    "fullName": full_name,
                    "major": s.major or "نامشخص",
                }
            )

        return Response(students_data)

    def delete(self, request, course_id: int, student_id: int):
        try:
            enrollment = Enrollment.objects.get(
                course_id=course_id, student_id=student_id
            )
        except Enrollment.DoesNotExist:
            return Response(
                {"message": "این دانشجو در این درس ثبت‌نام نشده است"},
                status=status.HTTP_404_NOT_FOUND,
            )

        enrollment.delete()
        return Response({"message": "دانشجو با موفقیت حذف شد"})


class ProfessorCoursePdfView(APIView):
    """
    GET /api/professor/courses/<course_id>/pdf
    ایجاد فایل PDF با اطلاعات کامل درس و لیست دانشجویان
    """

    permission_classes = [IsAuthenticated, IsProfessorUserRole]

    def get(self, request, course_id: int):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"message": "درس یافت نشد"}, status=status.HTTP_404_NOT_FOUND
            )

        # دریافت لیست دانشجویان
        enrollments = Enrollment.objects.filter(course=course).select_related("student")
        students = []
        for e in enrollments:
            s = e.student
            full_name = (s.get_full_name() or s.username).strip()
            students.append({
                "id": s.id,
                "fullName": full_name,
                "major": s.major or "نامشخص",
                "username": s.username
            })

        # ایجاد PDF
        from io import BytesIO
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from django.http import HttpResponse

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        
        # استایل‌ها
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1d4ed8'),
            spaceAfter=30,
            alignment=1,  # center
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=12,
            spaceBefore=20,
        )
        normal_style = styles['Normal']
        normal_style.fontSize = 11
        normal_style.leading = 16

        # محتوای PDF
        story = []

        # عنوان
        story.append(Paragraph("اطلاعات درس", title_style))
        story.append(Spacer(1, 0.5*cm))

        # اطلاعات درس
        course_info_data = [
            ['کد درس:', course.code],
            ['نام درس:', course.name],
            ['استاد:', course.professor_name or 'نامشخص'],
            ['واحد:', str(course.units)],
            ['ظرفیت کل:', str(course.capacity)],
            ['تعداد ثبت‌نام شده:', str(course.current_students)],
            ['ظرفیت باقیمانده:', str(course.capacity - course.current_students)],
            ['مکان برگزاری:', course.location or 'نامشخص'],
            ['زمان برگزاری:', course.time or 'نامشخص'],
        ]

        # روزهای برگزاری
        if course.schedule_days:
            schedule_text = '، '.join(course.schedule_days)
            course_info_data.append(['روزهای برگزاری:', schedule_text])
        else:
            course_info_data.append(['روزهای برگزاری:', 'تعیین نشده'])

        # پیش‌نیاز
        if course.prerequisite:
            course_info_data.append(['پیش‌نیاز:', course.prerequisite])
        else:
            course_info_data.append(['پیش‌نیاز:', 'ندارد'])

        # جدول اطلاعات درس
        course_table = Table(course_info_data, colWidths=[5*cm, 10*cm])
        course_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f9ff')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(course_table)
        story.append(Spacer(1, 1*cm))

        # لیست دانشجویان
        if students:
            story.append(Paragraph("لیست دانشجویان ثبت‌نام شده", heading_style))
            
            # هدر جدول دانشجویان
            students_header = [['ردیف', 'نام و نام خانوادگی', 'شماره دانشجویی', 'رشته تحصیلی']]
            
            # داده‌های دانشجویان
            students_data = []
            for idx, student in enumerate(students, 1):
                students_data.append([
                    str(idx),
                    student['fullName'],
                    student['username'],
                    student['major']
                ])
            
            students_table_data = students_header + students_data
            students_table = Table(students_table_data, colWidths=[1.5*cm, 6*cm, 4*cm, 3.5*cm], repeatRows=1)
            students_table.setStyle(TableStyle([
                # هدر
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                # بدنه
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1e293b')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                # ردیف‌های زوج
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ]))
            story.append(students_table)
        else:
            story.append(Paragraph("لیست دانشجویان ثبت‌نام شده", heading_style))
            story.append(Paragraph("هنوز دانشجویی در این درس ثبت‌نام نکرده است.", normal_style))

        story.append(Spacer(1, 1*cm))
        
        # پاورقی
        from datetime import datetime
        footer_text = f"تاریخ تولید: {datetime.now().strftime('%Y/%m/%d %H:%M')}"
        story.append(Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=normal_style,
            fontSize=9,
            textColor=colors.HexColor('#64748b'),
            alignment=1,  # center
        )))

        # ساخت PDF
        doc.build(story)
        buffer.seek(0)

        # پاسخ HTTP
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        # نام فایل با کد درس
        filename = f"course-{course.code}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
