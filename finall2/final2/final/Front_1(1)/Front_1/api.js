// فایل مشترک برای ارتباط فرانت با بک‌اند با استفاده از fetch
// آدرس اصلی بک‌اند
const API_BASE = 'http://127.0.0.1:8000';

function getAccessToken() {
  return localStorage.getItem('access_token') || localStorage.getItem('token') || '';
}

// درخواست عمومی به API که به صورت خودکار هدر Authorization را اضافه می‌کند
async function apiFetch(path, options = {}) {
  const url = path.startsWith('http') ? path : API_BASE + path;
  const token = getAccessToken();

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  if (token && !headers.Authorization) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    method: options.method || 'GET',
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    // اگر بدنه JSON نبود
  }

  if (!response.ok) {
    // اگر توکن نامعتبر یا منقضی شده، کاربر را به صفحه لاگین هدایت کن
    if (response.status === 401 && typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_role');
      localStorage.removeItem('user_id');
      localStorage.removeItem('username');
      window.location.href = 'login.html';
    }

    const message =
      (data && (data.detail || data.message)) ||
      `خطا در ارتباط با سرور (کد ${response.status})`;
    const error = new Error(message);
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data;
}

// ---------------- احراز هویت (لاگین) ----------------

const AuthAPI = {
  /**
   * تلاش برای لاگین به عنوان مدیر / دانشجو / استاد
   * در صورت موفقیت:
   *  - توکن‌ها در localStorage ذخیره می‌شوند
   *  - نقش کاربر برگردانده می‌شود
   */
  async login(username, password) {
    const endpoints = [
      '/api/auth/admin/login/',
      '/api/auth/student/login/',
      '/api/auth/professor/login/',
      '/api/token/',
    ];

    let lastError = null;

    for (const endpoint of endpoints) {
      try {
        const data = await apiFetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: { username, password },
        });

        const token =
          data.access_token || data.token || data.access || null;

        if (!token) {
          lastError = new Error('توکن معتبر از سرور دریافت نشد');
          continue;
        }

        const userData = data.user || data;
        let role = 'student';

        if (userData && userData.role) {
          role = String(userData.role).toLowerCase(); // ADMIN -> admin
        } else {
          if (endpoint.includes('admin')) role = 'admin';
          else if (endpoint.includes('professor')) role = 'professor';
          else if (endpoint.includes('student')) role = 'student';
        }

        // ذخیره توکن‌ها و اطلاعات کاربر
        localStorage.setItem('token', token);
        localStorage.setItem('access_token', token);
        if (data.refresh) {
          localStorage.setItem('refresh_token', data.refresh);
        }
        localStorage.setItem('user_role', role);
        if (userData) {
          if (userData.id !== undefined) {
            localStorage.setItem('user_id', String(userData.id));
          }
          if (userData.username) {
            localStorage.setItem('username', userData.username);
          }
        }

        return { token, role, user: userData };
      } catch (err) {
        lastError = err;
        continue;
      }
    }

    throw lastError || new Error('نام کاربری یا رمز عبور اشتباه است');
  },
};

// ---------------- نمونه‌های آماده برای استفاده در صفحات دیگر ----------------

const AdminAPI = {
  getCourses() {
    return apiFetch('/api/admin/courses');
  },
  createCourse(courseData) {
    return apiFetch('/api/admin/courses', {
      method: 'POST',
      body: courseData,
    });
  },
  updateCourse(id, courseData) {
    return apiFetch(`/api/admin/courses/${id}`, {
      method: 'PUT',
      body: courseData,
    });
  },
  deleteCourse(id) {
    return apiFetch(`/api/admin/courses/${id}`, {
      method: 'DELETE',
    });
  },
  getUnitLimits() {
    return apiFetch('/api/admin/unit-limits');
  },
  setUnitLimits(minUnits, maxUnits) {
    return apiFetch('/api/admin/unit-limits', {
      method: 'POST',
      body: { minUnits, maxUnits },
    });
  },
};

const StudentAPI = {
  getAllCourses() {
    return apiFetch('/api/courses');
  },
  getMyCourses() {
    return apiFetch('/api/student/courses');
  },
  addCourse(courseId) {
    return apiFetch('/api/student/courses', {
      method: 'POST',
      body: { courseId },
    });
  },
  removeCourse(courseId) {
    return apiFetch(`/api/student/courses/${courseId}`, {
      method: 'DELETE',
    });
  },
  getSchedule() {
    return apiFetch('/api/student/schedule');
  },
};

const ProfessorAPI = {
  getCourses() {
    return apiFetch('/api/professor/courses');
  },
  getCourseStudents(courseId) {
    return apiFetch(`/api/professor/courses/${courseId}/students`);
  },
  removeStudent(courseId, studentId) {
    return apiFetch(`/api/professor/courses/${courseId}/students/${studentId}`, {
      method: 'DELETE',
    });
  },
  downloadCoursePdf(courseId) {
    const token = getAccessToken();
    const url = `${API_BASE}/api/professor/courses/${courseId}/pdf`;
    return fetch(url, {
      method: 'GET',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
  },
};


