document.getElementById('registerForm').addEventListener('submit', function(e) {
  e.preventDefault();

  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();

  if (!name || !email || !password) {
    alert('Please fill all fields');
    return;
  }

  // Retrieve existing users (if any)
  let users = JSON.parse(localStorage.getItem('users')) || [];

  // Check if email already exists
  if (users.some(u => u.email === email)) {
    alert('Email already registered!');
    return;
  }

  // Create new freelancer user
  const newUser = {
    name,
    email,
    password,
    role: 'freelancer'
  };

  // Save to local storage
  users.push(newUser);
  localStorage.setItem('users', JSON.stringify(users));

  // Also set as logged in immediately
  localStorage.setItem('loggedInUser', JSON.stringify(newUser));

  // Redirect to freelancer dashboard
  window.location.href = 'dashboard.html';
});
