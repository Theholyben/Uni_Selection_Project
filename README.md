
# University Course Registration System    
**Software Engineering – Eng. Omid Adibfar**

A modern RESTful API with JWT authentication and role-based access control for university course registration.

---

## Sprint 1 Features (100% Completed)

- Custom User Model with `role` (ADMIN / STUDENT / PROFESSOR)  
- JWT Authentication (`djangorestframework-simplejwt`)  
- Admin login with access & refresh tokens  
- Full course CRUD (only accessible by ADMIN)  
- Course listing for all authenticated users  
- Complete API documentation in `api-contract.md`  
- Git Flow with `main`, `develop`, `feature/*` branches  
- Fully tested with Postman  

---

## How to Run Locally

```bash
git clone https://github.com/Theholyben/Uni_Selection_Project.git
cd Uni_Selection_Project

python -m venv venv
venv\Scripts\activate        # Windows

pip install django djangorestframework djangorestframework-simplejwt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser     # username: admin, password: 123456

# Set role to ADMIN in admin panel → http://127.0.0.1:8000/admin/
python manage.py runserver
```

**API Base URL:** `http://127.0.0.1:8000/api/`

---

## All API Requests – Sprint 1 (Tested with Postman)

### 1. Authentication Endpoints

#### 1.1 Login & Get Tokens
```
POST http://127.0.0.1:8000/api/token/
Content-Type: application/x-www-form-urlencoded

username=admin&password=123456
```
**Success (200):**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxx",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.yyyy"
}
```

#### 1.2 Refresh Token
```
POST http://127.0.0.1:8000/api/token/refresh/
```
```json
{ "refresh": "eyJhbGciOiJIUzI1NiIs..." }
→ { "access": "new-token..." }
```

---

### 2. Course Management (All Endpoints – Sprint 1)

> **All requests below require header:**
```
Authorization: Bearer <access_token>
```

| Method | Endpoint                  | Description                  | Required Role     | Status Code |
|--------|---------------------------|------------------------------|-------------------|-------------|
| GET    | `/courses/`               | List all courses             | Any logged-in user| 200         |
| POST   | `/courses/`               | Create new course            | ADMIN only        | 201         |
| GET    | `/courses/{id}/`          | Get course details           | Any logged-in user| 200         |
| PUT    | `/courses/{id}/`          | Update course (full)         | ADMIN only        | 200         |
| PATCH  | `/courses/{id}/`          | Update course (partial)      | ADMIN only        | 200         |
| DELETE | `/courses/{id}/`          | Delete course                | ADMIN only        | 204         |

#### 2.1 Create Course (Admin Only)
```
POST http://127.0.0.1:8000/api/courses/
```
```json
{
  "code": "123456",
  "name": "Database Lab",
  "capacity": 12,
  "professor": "Dr. Jaderian",
  "day": "Saturday",
  "time": "8-10",
  "location": "Lab 4",
  "units": 1
}
```
**201 Created** → Course created  
**403 Forbidden** → Not admin  
**400 Bad Request** → Validation error

#### 2.2 List All Courses
```
GET http://127.0.0.1:8000/api/courses/
```

#### 2.3 Get Course Details
```
GET http://127.0.0.1:8000/api/courses/1/
```

#### 2.4 Update Course (Full)
```
PUT http://127.0.0.1:8000/api/courses/1/
```
Same body as create

#### 2.5 Update Course (Partial)
```
PATCH http://127.0.0.1:8000/api/courses/1/
```
```json
{ "capacity": 20 }
```

#### 2.6 Delete Course
```
DELETE http://127.0.0.1:8000/api/courses/1/
```
**204 No Content**


## Team & Documentation
- Full API spec: [api-contract.md](api-contract.md)  
- Tested with Postman  

**Sprint 1 – 100% Completed**  
Ready for demo and submission

---
**Eng. Omid Adibfar – Software Engineering – Fall 2025**
```