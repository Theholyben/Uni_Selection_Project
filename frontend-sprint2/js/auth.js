document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  const errorMsg = document.getElementById('errorMsg');

  try {
    const res = await fetch('http://127.0.0.1:8000/api/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (res.ok && data.access) {
      localStorage.setItem('token', data.access);
      localStorage.setItem('refresh', data.refresh || '');
      localStorage.setItem('user', JSON.stringify(data.user || {}));

      if (username === 'admin') {
        window.location.href = '../frontend-sprint1/index.html'; 
      } else {
        window.location.href = 'dashboard.html'; 
      }
    } else {
      errorMsg.textContent = data.detail || 'نام کاربری یا رمز اشتباه است';
      errorMsg.classList.remove('hidden');
    }
  } catch (err) {
    errorMsg.textContent = 'بک‌اند هنوز آماده نیست ';
    errorMsg.classList.remove('hidden');
  }
});