document.getElementById('logoutBtn')?.addEventListener('click', () => {
  localStorage.clear();
  location.href = 'index.html';
});

const user = JSON.parse(localStorage.getItem('user') || '{}');
const token = localStorage.getItem('token');

if (!token || !user || !user.role) {
  location.href = 'index.html';
}

const role = user.role;

if (role === 'admin') {
  document.getElementById('adminSection')?.classList.remove('hidden');
} else if (role === 'professor') {
  document.getElementById('professorSection')?.classList.remove('hidden');
} else if (role === 'student') {
  document.getElementById('studentSection')?.classList.remove('hidden');
} else {
  alert("نقش کاربر نامعتبر است");
  localStorage.clear();
  location.href = 'index.html';
}