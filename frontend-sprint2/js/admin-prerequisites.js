import { apiFetch } from './api.js';

const getToken = () => localStorage.getItem('token');
const courseSelect = document.getElementById('courseSelect');
const prereqSelect = document.getElementById('prereqSelect');

function showMessage(type, msg) {
  const ok = document.getElementById('addSuccess');
  const err = document.getElementById('addError');
  (type === 'success' ? ok : err).textContent = msg;
  ok.classList.toggle('hidden', type !== 'success');
  err.classList.toggle('hidden', type === 'success');
}

async function loadPrerequisites() {
  try {
    const data = await apiFetch('/prerequisites/');
    const tbody = document.getElementById('prereqTableBody');
    const empty = document.getElementById('emptyMessage');

    tbody.innerHTML = '';
    empty.classList.toggle('hidden', data.length !== 0);

    data.forEach(p => {
      tbody.innerHTML += `
        <tr>
          <td class="px-6 py-4">${p.course || '—'}</td>
          <td class="px-6 py-4">${p.prerequisite || '—'}</td>
          <td class="px-6 py-4 text-right">
            <button data-id="${p.id}" class="deleteBtn text-red-600">حذف</button>
          </td>
        </tr>`;
    });
  } catch (err) {
    console.error(err);
    document.getElementById('notAdminAlert').classList.remove('hidden');
    document.getElementById('adminContent').classList.add('hidden');
  }
}

document.getElementById('addPrereqForm')
  .addEventListener('submit', async e => {
    e.preventDefault();
    const token = getToken();
    if (!token) return alert('لطفاً وارد شوید');

    const body = {
      course_id: courseSelect.value,
      prerequisite_id: prereqSelect.value
    };

    const res = await fetch('http://127.0.0.1:8000/api/prerequisites/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(body)
    });

    if (res.ok) {
      showMessage('success', 'ثبت شد');
      e.target.reset();
      loadPrerequisites();
    } else {
      const errData = await res.json();
      showMessage('error', errData.detail || 'خطا');
    }
  });

document.getElementById('prereqTableBody')
  .addEventListener('click', async e => {
    if (!e.target.classList.contains('deleteBtn')) return;
    const token = getToken();

    const res = await fetch(`http://127.0.0.1:8000/api/prerequisites/${e.target.dataset.id}/`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    });

    if (res.ok) {
      loadPrerequisites();
    } else {
      showMessage('error', 'خطا در حذف پیش‌نیاز');
    }
  });

loadPrerequisites();