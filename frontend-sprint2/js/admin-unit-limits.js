const getToken = () => localStorage.getItem('token');

const showMessage = (type, msg) => {
  const success = document.getElementById('unitSuccess');
  const error = document.getElementById('unitError');
  (type === 'success' ? success : error).textContent = msg;
  success.classList.toggle('hidden', type !== 'success');
  error.classList.toggle('hidden', type === 'success');
};

async function loadUnitLimits() {
  const token = getToken();
  if (!token) return;

  try {
    const res = await fetch('http://127.0.0.1:8000/api/unit-limits/', {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (res.status === 403) {
      document.getElementById('notAdminAlert').classList.remove('hidden');
      document.getElementById('adminContent').classList.add('hidden');
      return;
    }

    const { min_units, max_units } = await res.json();
    document.getElementById('minUnits').value = min_units;
    document.getElementById('maxUnits').value = max_units;
  } catch {
    showMessage('error', 'خطا در بارگذاری تنظیمات واحدها');
  }
}

document.getElementById('unitLimitsForm')?.addEventListener('submit', async e => {
  e.preventDefault();
  const token = getToken();
  if (!token) return (window.location.href = 'index.html');

  const min = parseInt(document.getElementById('minUnits').value, 10);
  const max = parseInt(document.getElementById('maxUnits').value, 10);
  const btn = e.target.querySelector('button[type="submit"]');

  btn.textContent = 'در حال ذخیره...'; btn.disabled = true;

  try {
    const res = await fetch('http://127.0.0.1:8000/api/unit-limits/', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ min_units: min, max_units: max })
    });

    res.ok ? showMessage('success', 'با موفقیت ذخیره شد')
           : showMessage('error', (await res.json()).detail || 'خطا در ذخیره');
  } catch {
    showMessage('error', 'خطا در ارتباط با سرور');
  } finally {
    btn.textContent = 'ثبت تغییرات'; btn.disabled = false;
    loadUnitLimits();
  }
});

loadUnitLimits();