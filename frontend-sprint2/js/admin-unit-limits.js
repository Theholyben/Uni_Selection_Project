function getToken() {
  return localStorage.getItem('token');
}

function showMessage(type, msg) {
  const success = document.getElementById('unitSuccess');
  const error = document.getElementById('unitError');
  if (type === 'success') {
    success.textContent = msg;
    success.classList.remove('hidden');
    error.classList.add('hidden');
  } else {
    error.textContent = msg;
    error.classList.remove('hidden');
    success.classList.add('hidden');
  }
}


async function loadUnitLimits() {
  const token = getToken();
  if (!token) return;

  try {
    const res = await fetch('/api/unit-limits/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();


    document.getElementById('minUnits').value = data.min_units;
    document.getElementById('maxUnits').value = data.max_units;
  } catch {
    showMessage('error', 'خطا در بارگذاری تنظیمات واحدها');
  }
}


document.getElementById('unitLimitsForm')
  .addEventListener('submit', async (e) => {
    e.preventDefault();
    const token = getToken();
    if (!token) {
      alert('لطفاً ابتدا وارد سیستم شوید');
      window.location.href = 'index.html';
      return;
    }

    const min = document.getElementById('minUnits').value;
    const max = document.getElementById('maxUnits').value;

    const btn = e.target.querySelector('button[type="submit"]');
    btn.textContent = 'در حال ذخیره...';
    btn.disabled = true;

    try {
      const res = await fetch('/api/unit-limits/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ min_units: min, max_units: max })
      });

      if (res.ok) {
        showMessage('success', ' با موفقیت ذخیره شد');
      } else {
        const err = await res.json();
        showMessage('error', err.detail || 'خطا در ذخیره ');
      }
    } catch {
      showMessage('error', 'خطا در ارتباط با سرور');
    } finally {
      btn.textContent = 'ثبت تغییرات';
      btn.disabled = false;
    }
});


loadUnitLimits();