# سیستم مدیریت انتخاب واحد دانشگاهی

یک سیستم کامل مدیریت انتخاب واحد دانشگاهی با سه نقش کاربری: مدیر، استاد و دانشجو. این پروژه با استفاده از Django REST Framework در بک‌اند و HTML/CSS/JavaScript در فرانت‌اند پیاده‌سازی شده است.

## 📋 فهرست مطالب

- [ویژگی‌ها](#ویژگی‌ها)
- [تکنولوژی‌های استفاده شده](#تکنولوژی‌های-استفاده-شده)
- [نصب و راه‌اندازی](#نصب-و-راه‌اندازی)
- [ساختار پروژه](#ساختار-پروژه)
- [نحوه استفاده](#نحوه-استفاده)
- [API Endpoints](#api-endpoints)
- [اطلاعات ورود](#اطلاعات-ورود)

## ✨ ویژگی‌ها

### 👨‍💼 پنل مدیر
- مدیریت کامل دروس (افزودن، ویرایش، حذف)
- تنظیم حداقل و حداکثر واحد مجاز برای دانشجویان
- مشاهده لیست تمام دروس

### 👨‍🏫 پنل استاد
- مشاهده دروس ارائه شده توسط استاد
- مشاهده لیست دانشجویان هر درس
- حذف دانشجو از درس
- دانلود فایل PDF با اطلاعات کامل درس و لیست دانشجویان

### 👨‍🎓 پنل دانشجو
- مشاهده لیست دروس ارائه شده
- حذف و اضافه دروس (ثبت‌نام/حذف واحد)
- مشاهده برنامه هفتگی
- جستجوی درس با کد یا ID

### 🔐 سیستم احراز هویت
- احراز هویت با JWT Token
- سه نقش کاربری جداگانه (مدیر، استاد، دانشجو)
- کنترل دسترسی بر اساس نقش

### 📊 ویژگی‌های اضافی
- کنترل ظرفیت کلاس
- کنترل پیش‌نیاز دروس
- کنترل سقف واحد مجاز
- جلوگیری از ثبت‌نام تکراری
- برنامه هفتگی خودکار

## 🛠 تکنولوژی‌های استفاده شده

### Backend
- **Django 5.2.10** - فریم‌ورک اصلی
- **Django REST Framework 3.16.1** - برای ساخت API
- **djangorestframework-simplejwt 5.5.1** - احراز هویت JWT
- **django-cors-headers 4.9.0** - مدیریت CORS
- **reportlab 4.4.9** - تولید فایل PDF
- **SQLite** - پایگاه داده

### Frontend
- **HTML5** - ساختار صفحات
- **CSS3** - استایل‌دهی و طراحی
- **JavaScript (Vanilla)** - منطق فرانت‌اند
- **Font Awesome** - آیکون‌ها

## 📦 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.8 یا بالاتر
- pip (مدیر بسته Python)

### مراحل نصب

1. **کلون یا دانلود پروژه**
   ```bash
   cd final/Front_1(1)
   ```

2. **ایجاد محیط مجازی (اختیاری اما توصیه می‌شود)**
   ```bash
   python -m venv venv
   
   # در Windows
   venv\Scripts\activate
   
   # در Linux/Mac
   source venv/bin/activate
   ```

3. **نصب وابستگی‌ها**
   
   **روش 1: استفاده از requirements.txt (توصیه می‌شود)**
   ```bash
   pip install -r requirements.txt
   ```
   
   **روش 2: نصب دستی**
   ```bash
   pip install django==5.2.10
   pip install djangorestframework==3.16.1
   pip install djangorestframework-simplejwt==5.5.1
   pip install django-cors-headers==4.9.0
   pip install reportlab==4.4.9
   ```

4. **اجرای migrations**
   ```bash
   python manage.py migrate
   ```

5. **ایجاد کاربران نمونه و داده‌های اولیه**
   ```bash
   python create_users.py
   ```

6. **اجرای سرور Django**
   ```bash
   python manage.py runserver
   ```

7. **باز کردن صفحات HTML**
   - فایل‌های HTML در پوشه `Front_1` قرار دارند
   - می‌توانید آن‌ها را مستقیماً در مرورگر باز کنید
   - یا از یک سرور محلی استفاده کنید (مثلاً Live Server در VS Code)

## 📁 ساختار پروژه

```
final/Front_1(1)/
│
├── backend/                 # تنظیمات اصلی Django
│   ├── settings.py          # تنظیمات پروژه
│   ├── urls.py             # URL routing اصلی
│   └── ...
│
├── core/                   # اپلیکیشن اصلی
│   ├── models.py           # مدل‌های دیتابیس
│   ├── views.py            # View های API
│   ├── serializers.py      # سریالایزرها
│   ├── urls.py             # URL routing اپلیکیشن
│   ├── permissions.py      # کنترل دسترسی
│   └── migrations/         # فایل‌های migration
│
├── Front_1/                # فایل‌های فرانت‌اند
│   ├── login.html          # صفحه ورود
│   ├── admin-dashboard.html        # داشبورد مدیر
│   ├── courses-management.html     # مدیریت دروس (مدیر)
│   ├── units-management.html       # مدیریت واحدها (مدیر)
│   ├── professor-dashboard.html     # داشبورد استاد
│   ├── professor-remove-student.html # مدیریت دانشجویان (استاد)
│   ├── student-dashboard.html       # داشبورد دانشجو
│   ├── courses-list.html            # لیست دروس (دانشجو)
│   ├── delete-add-course.html       # حذف و اضافه (دانشجو)
│   ├── weekly-schedule.html        # برنامه هفتگی (دانشجو)
│   └── api.js              # فایل JavaScript مشترک برای API
│
├── create_users.py         # اسکریپت ایجاد کاربران و داده‌های نمونه
├── manage.py              # فایل مدیریت Django
├── db.sqlite3             # پایگاه داده SQLite
└── README.md              # این فایل
```

## 🚀 نحوه استفاده

### 1. ورود به سیستم

صفحه `login.html` را در مرورگر باز کنید و با یکی از حساب‌های زیر وارد شوید:

#### مدیر
- **Username:** `admin`
- **Password:** `admin123`

#### استاد
- **Username:** `professor`
- **Password:** `professor123`

#### دانشجو
- **Username:** `student` (یا `student1` تا `student7`)
- **Password:** `student123`

### 2. استفاده از پنل مدیر

- **مدیریت دروس:** افزودن، ویرایش و حذف دروس
- **مدیریت واحدها:** تنظیم حداقل و حداکثر واحد مجاز

### 3. استفاده از پنل استاد

- **مشاهده دروس:** مشاهده لیست دروس ارائه شده
- **مدیریت دانشجویان:** مشاهده و حذف دانشجویان هر درس
- **دانلود PDF:** دریافت فایل PDF با اطلاعات کامل درس

### 4. استفاده از پنل دانشجو

- **مشاهده دروس:** مشاهده لیست دروس ارائه شده
- **حذف و اضافه:** ثبت‌نام یا حذف واحد
- **برنامه هفتگی:** مشاهده برنامه کلاسی هفتگی

## 🔌 API Endpoints

### احراز هویت
- `POST /api/auth/admin/login/` - ورود مدیر
- `POST /api/auth/student/login/` - ورود دانشجو
- `POST /api/auth/professor/login/` - ورود استاد

### مدیر
- `GET /api/admin/courses` - لیست دروس
- `POST /api/admin/courses` - افزودن درس
- `PUT /api/admin/courses/<id>` - ویرایش درس
- `DELETE /api/admin/courses/<id>` - حذف درس
- `GET /api/admin/unit-limits` - دریافت حدود واحد
- `POST /api/admin/unit-limits` - تنظیم حدود واحد

### دانشجو
- `GET /api/courses` - لیست دروس ارائه شده
- `GET /api/student/courses` - دروس ثبت‌نام شده
- `POST /api/student/courses` - ثبت‌نام در درس
- `DELETE /api/student/courses/<course_id>` - حذف درس
- `GET /api/student/schedule` - برنامه هفتگی

### استاد
- `GET /api/professor/courses` - دروس ارائه شده
- `GET /api/professor/courses/<course_id>/students` - لیست دانشجویان
- `DELETE /api/professor/courses/<course_id>/students/<student_id>` - حذف دانشجو
- `GET /api/professor/courses/<course_id>/pdf` - دانلود PDF

## 👥 اطلاعات ورود

### کاربران پیش‌فرض

پس از اجرای `create_users.py`، کاربران زیر ایجاد می‌شوند:

#### مدیر
- **Username:** `admin`
- **Password:** `admin123`

#### استاد
- **Username:** `professor`
- **Password:** `professor123`
- **نام:** دکتر رضایی
- **دروس:** 4 درس نمونه (برنامه‌نویسی پیشرفته، پایگاه داده، هوش مصنوعی، شبکه‌های کامپیوتری)

#### دانشجویان (8 نفر)
- **Username:** `student`, `student1`, `student2`, ..., `student7`
- **Password:** `student123` (برای همه)
- **ثبت‌نام:** دانشجویان در دروس مختلف ثبت‌نام شده‌اند

## 📚 داده‌های نمونه

پس از اجرای `create_users.py`:

- **4 درس** برای استاد ایجاد می‌شود
- **8 دانشجو** ایجاد می‌شود
- **18 ثبت‌نام** در دروس مختلف انجام می‌شود

### دروس نمونه
1. **برنامه‌نویسی پیشرفته (CS301)** - 5 دانشجو
2. **پایگاه داده (CS302)** - 4 دانشجو
3. **هوش مصنوعی (CS401)** - 3 دانشجو
4. **شبکه‌های کامپیوتری (CS303)** - 6 دانشجو

## 🔧 تنظیمات

### تغییر آدرس API

در فایل `Front_1/api.js`:
```javascript
const API_BASE = 'http://127.0.0.1:8000';
```

### تغییر تنظیمات Django

در فایل `backend/settings.py` می‌توانید:
- تنظیمات CORS را تغییر دهید
- تنظیمات JWT را تغییر دهید
- پایگاه داده را تغییر دهید

## 🐛 عیب‌یابی

### مشکل: CORS Error
- مطمئن شوید که `django-cors-headers` نصب شده است
- در `settings.py` بررسی کنید که `CORS_ALLOW_ALL_ORIGINS = True` باشد

### مشکل: 404 Not Found
- مطمئن شوید که سرور Django در حال اجرا است
- بررسی کنید که URL درست است

### مشکل: Authentication Failed
- بررسی کنید که توکن در localStorage ذخیره شده است
- دوباره وارد شوید

## 📝 نکات مهم

1. **امنیت:** این پروژه برای محیط توسعه است. برای production باید تنظیمات امنیتی را تغییر دهید.

2. **پایگاه داده:** از SQLite استفاده می‌شود که برای production مناسب نیست.

3. **Static Files:** فایل‌های استاتیک باید در production به درستی تنظیم شوند.

4. **CORS:** در production باید CORS را محدود کنید.

## 📄 مجوز

این پروژه برای استفاده آموزشی و توسعه ایجاد شده است.

## 👨‍💻 توسعه‌دهنده

برای سوالات و پیشنهادات، لطفاً با توسعه‌دهنده تماس بگیرید.

---

**نکته:** این پروژه یک سیستم کامل مدیریت انتخاب واحد است که می‌تواند به عنوان پایه برای پروژه‌های بزرگ‌تر استفاده شود.

