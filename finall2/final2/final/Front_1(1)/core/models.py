from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    کاربر سامانه با سه نقش اصلی: مدیر، استاد و دانشجو
    """

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "مدیر"
        PROFESSOR = "PROFESSOR", "استاد"
        STUDENT = "STUDENT", "دانشجو"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.STUDENT,
    )

    # فیلدهای اختیاری برای نمایش بهتر اطلاعات دانشجو
    major = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:  # type: ignore[override]
        return f"{self.username} ({self.get_role_display()})"


class Course(models.Model):
    """
    اطلاعات درس و ارائه آن در یک نیمسال
    """

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)

    # در فرانت فقط نام استاد به صورت متن ارسال می‌شود
    professor_name = models.CharField(max_length=255, blank=True)

    capacity = models.PositiveIntegerField(default=30)
    time = models.CharField(max_length=100, blank=True)
    units = models.PositiveIntegerField(default=3)
    location = models.CharField(max_length=255, blank=True)

    # پیش‌نیاز به صورت متن (مثلاً کد یا نام درس) نگه‌داری می‌شود
    prerequisite = models.CharField(max_length=255, blank=True)

    # روزهای برگزاری (لیستی از رشته‌ها مثل: ["شنبه", "دوشنبه"])
    schedule_days = models.JSONField(default=list, blank=True)

    def __str__(self) -> str:  # type: ignore[override]
        return f"{self.code} - {self.name}"

    @property
    def current_students(self) -> int:
        """تعداد دانشجویان ثبت‌نام‌شده در این درس"""
        return self.enrollments.count()


class UnitLimit(models.Model):
    """
    حداقل و حداکثر واحد مجاز برای هر دانشجو در یک بازه زمانی (نیمسال)
    در این پروژه فقط یک رکورد استفاده می‌کنیم.
    """

    min_units = models.PositiveIntegerField(default=12)
    max_units = models.PositiveIntegerField(default=20)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # type: ignore[override]
        return f"حد واحدها: {self.min_units} - {self.max_units}"


class Enrollment(models.Model):
    """
    انتخاب واحد: اتصال دانشجو به درس
    """

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self) -> str:  # type: ignore[override]
        return f"{self.student.username} -> {self.course.code}"
