// Admin Login Script
document.getElementById('adminLoginForm').addEventListener('submit', function(e) {
  e.preventDefault();

  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();

  // Example admin credentials (replace with backend later)
  const adminCredentials = {
    email: 'sherileidah@gmail.com',
    password: '5240',
    role: 'admin'
  };

  if (email === adminCredentials.email && password === adminCredentials.password) {
    // Save login session
    localStorage.setItem('loggedInUser', JSON.stringify(adminCredentials));

    // Redirect to Admin Dashboard
    window.location.href = 'admin.html';
  } else {
    alert('Invalid admin email or password!');
  }
});
