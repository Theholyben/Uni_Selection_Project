const getToken = () => localStorage.getItem('token');

function showMessage(type, msg) {
  const ok = document.getElementById('addSuccess');
  const err = document.getElementById('addError');
  (type === 'success' ? ok : err).textContent = msg;
  ok.classList.toggle('hidden', type !== 'success');
  err.classList.toggle('hidden', type === 'success');
}

async function loadPrerequisites() {
  const token = getToken();
  if (!token) return;

  const res = await fetch('/api/prerequisites/', {
    headers: { Authorization: `Bearer ${token}` }
  });

  if (res.status === 403) {
    document.getElementById('notAdminAlert').classList.remove('hidden');
    document.getElementById('adminContent').classList.add('hidden');
    return;
  }

  document.getElementById('adminContent').classList.remove('hidden');

  const data = await res.json();
  const tbody = document.getElementById('prereqTableBody');
  const empty = document.getElementById('emptyMessage');

  tbody.innerHTML = '';
  empty.classList.toggle('hidden', data.length !== 0);

  data.forEach(p => {
    tbody.innerHTML += `
      <tr>
        <td class="px-6 py-4">${p.course}</td>
        <td class="px-6 py-4">${p.prerequisite}</td>
        <td class="px-6 py-4 text-right">
          <button data-id="${p.id}" class="deleteBtn text-red-600">حذف</button>
        </td>
      </tr>`;
  });
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

    const res = await fetch('/api/prerequisites/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(body)
    });

    res.ok
      ? (showMessage('success', 'ثبت شد'), e.target.reset(), loadPrerequisites())
      : showMessage('error', (await res.json()).detail || 'خطا');
  });

document.getElementById('prereqTableBody')
  .addEventListener('click', async e => {
    if (!e.target.classList.contains('deleteBtn')) return;
    const token = getToken();

    await fetch(`/api/prerequisites/${e.target.dataset.id}/`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    });

    loadPrerequisites();
  });

loadPrerequisites();
