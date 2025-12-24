document.getElementById('loginForm').addEventListener('submit', function(e) {
  e.preventDefault();

  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();

  // Get all users (including those registered via register.js)
  const storedUsers = JSON.parse(localStorage.getItem('users')) || [];

  // Include admin manually
  const allUsers = [
    ...storedUsers,
    { email: 'admin@example.com', password: 'admin123', role: 'admin' }
  ];

  const user = allUsers.find(u => u.email === email && u.password === password);

  if (user) {
    localStorage.setItem('loggedInUser', JSON.stringify(user));

    if (user.role === 'admin') {
      window.location.href = 'admin.html';
    } else {
      window.location.href = 'dashboard.html';
    }
  } else {
    alert('Invalid email or password!');
  }
});
//editby me
// Example after successful login
const username = document.getElementById('usernameInput').value; // get username from login form
localStorage.setItem('loggedFreelancerName', username);

// Then redirect to dashboard
window.location.href = 'dashboard.html';




