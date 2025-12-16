document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  const errorMsg = document.getElementById('errorMsg');

  try {
    const res = await fetch('http://127.0.0.1:8000/api/token/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username, password })
    });

    const data = await res.json();

    if (res.ok && data.access) {
      localStorage.setItem('token', data.access);
      localStorage.setItem('refresh', data.refresh || '');

      const userRes = await fetch('http://127.0.0.1:8000/api/users/me/', {
        headers: {
          'Authorization': `Bearer ${data.access}`
        }
      });

      const userData = await userRes.json();
      localStorage.setItem('user', JSON.stringify(userData));

      const role = userData.role;
      if (role === 'ADMIN') {
        window.location.href = '../frontend-sprint1/index.html';
      } else {
        window.location.href = 'dashboard.html';
      }
    } else {
      errorMsg.textContent = data.detail || 'نام کاربری یا رمز اشتباه است';
      errorMsg.classList.remove('hidden');
    }
  } catch (err) {
    errorMsg.textContent = 'بک‌اند هنوز آماده نیست';
    errorMsg.classList.remove('hidden');
  }
});