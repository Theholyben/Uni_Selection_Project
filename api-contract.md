# API Contract - Courses

## Base URL
`http://localhost:8000/api/`

## Endpoints

### 1. Create New Course
**POST** `/courses/`

**Request Example:**
```json
{
  "code": "123456",
  "name": "DB Lab",
  "capacity": 12,
  "professor": "Dr. Jaderian",
  "day": "Saturday",
  "time": "8-10",
  "location": "Lab 4", 
  "units": 1
}
```

**Validation Rules:**
* `code`: 2-7 digits, unique, required
* `name`: non-empty, required
* `capacity`: integer, ≥ 0, optional (default: 0)
* `units`: 1, 2, or 3, optional (default: 1)  
* `professor`: optional (can be empty or omitted)
* `day`: optional (can be empty or omitted)
* `time`: optional (can be empty or omitted)
* `location`: optional (can be empty or omitted)

**Response Example (201 Created):**
```json
{
  "id": 1,
  "code": "123456",
  "name": "DB Lab",
  "capacity": 12,
  "professor": "Dr. Jaderian", 
  "day": "Saturday",
  "time": "8-10",
  "location": "Lab 4",
  "units": 1
}
```

**Response Codes:**
* `201 Created`: Course successfully created
* `403 Forbidden`: User is not admin
* `400 Bad Request`: Validation failed

### 2. List All Courses  
**GET** `/courses/`

### 3. Get Course Details
**GET** `/courses/{id}/`

### 4. Update Course
**PUT** `/courses/{id}/`

### 5. Delete Course  
**DELETE** `/courses/{id}/`



## 1. Authentication – JWT

### 1.1 Login & Obtain Tokens
```
POST /token/
Content-Type: application/x-www-form-urlencoded
```
**Request Example:**
```
username=admin&password=123456
```

**Success Response (200 OK):**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxxxxxxxxxxxxxxxxx",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.yyyyyyyyyyyyyyyyyyyyyyyyy"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "No active account found with the given credentials"
}
```

### 1.2 Refresh Access Token
```
POST /token/refresh/
Content-Type: application/json
```
**Request Example:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.newaccesstokenhere"
}
```

**Authentication Header for All Protected Endpoints:**
```
Authorization: Bearer <access_token>
```

**Role-Based Permission:**
- Only users with `role = "ADMIN"` can perform CRUD operations on courses (`IsAdminUser` custom permission)
- All authenticated users can view course list
```
