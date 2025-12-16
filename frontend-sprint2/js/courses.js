import { apiFetch } from './api.js';

let allCourses = [];

async function loadCourses() {
  const loading = document.getElementById('loading');
  const noResult = document.getElementById('noResult');

  if (loading) loading.classList.remove('hidden');

  try {
    allCourses = await apiFetch('/courses/');
    renderCourses(allCourses);
    if (noResult) noResult.classList.add('hidden');
  } catch (err) {
    console.error(err);
    if (noResult) {
      noResult.textContent = 'خطا در دریافت دروس (سمت سرور)';
      noResult.classList.remove('hidden');
    }
  } finally {
    if (loading) loading.classList.add('hidden');
  }
}

function renderCourses(courses) {
  const grid = document.getElementById('coursesGrid');
  if (!grid) return;

  if (courses.length === 0) {
    grid.innerHTML = '<p class="text-center text-gray-500 col-span-full py-12">متاسفانه درسی یافت نشد</p>';
    return;
  }

  grid.innerHTML = courses.map(course => `
    <div class="bg-white p-6 rounded-xl shadow hover:shadow-2xl transition">
      <h3 class="text-xl font-bold text-purple-700 mb-2">${course.name || 'نامشخص'}</h3>
      <p class="text-gray-600">کد: ${course.code || '—'}</p>
      <p class="text-gray-600">استاد: ${course.professor || 'نامشخص'}</p>
      <p class="text-gray-600">ظرفیت: ${course.capacity ?? '—'}</p>
      <p class="text-sm text-gray-500 mt-4">
        زمان برگزاری: ${course.day || '—'} ${course.time || '—'}
      </p>
      <p class="text-sm text-gray-500">محل برگزاری: ${course.location || '—'}</p>
      <a href="course-detail.html?id=${course.id}" 
         class="block mt-6 bg-purple-600 text-white py-2 rounded text-center hover:bg-purple-700 transition">
        مشاهده جزئیات
      </a>
    </div>
  `).join('');
}

function filterCourses() {
  const search = document.getElementById('searchInput')?.value.toLowerCase() || '';
  const filtered = allCourses.filter(course => {
    return (course.name?.toLowerCase().includes(search) || false) ||
           (course.professor?.toLowerCase().includes(search) || false);
  });
  renderCourses(filtered);
}

document.getElementById('searchInput')?.addEventListener('input', filterCourses);

loadCourses();