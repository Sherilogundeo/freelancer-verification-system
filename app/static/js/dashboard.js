// DASHBOARD JS - Full Functionality

// TAB SWITCHING
const tabButtons = document.querySelectorAll('.side-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    tabButtons.forEach(b => b.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.tab).classList.add('active');
  });
});
//byme
window.addEventListener('DOMContentLoaded', () => {
  const savedName = localStorage.getItem('loggedFreelancerName');
  if(savedName){
    document.getElementById('displayName').textContent = savedName;
  }
});


// PROFILE EDIT
const editBtn = document.getElementById('editProfileBtn');
const saveBtn = document.getElementById('saveProfileBtn');
const cancelBtn = document.getElementById('cancelEditBtn');
const editBox = document.getElementById('profileEdit');

editBtn.onclick = () => { editBox.classList.remove('hidden'); };
cancelBtn.onclick = () => { editBox.classList.add('hidden'); };
saveBtn.onclick = () => {
  document.getElementById('displayName').textContent = document.getElementById('nameInput').value;
  document.getElementById('displayEmail').textContent = document.getElementById('emailInput').value;
  document.getElementById('displayPhone').textContent = document.getElementById('phoneInput').value;
  editBox.classList.add('hidden');
};
//edit by sheril/
// Load profile info from localStorage
window.addEventListener('DOMContentLoaded', () => {
  const savedName = localStorage.getItem('loggedFreelancerName');
  const savedEmail = localStorage.getItem('loggedEmail');
  const savedPhone = localStorage.getItem('loggedPhone');
  const savedPhoto = localStorage.getItem('loggedFreelancerPhoto');

  if(savedName) document.getElementById('displayName').textContent = savedName;
  if(savedEmail) document.getElementById('displayEmail').textContent = savedEmail;
  if(savedPhone) document.getElementById('displayPhone').textContent = savedPhone;
  if(savedPhoto) document.getElementById('displayPhoto').src = savedPhoto;
});


// PROFILE PHOTO UPLOAD
const photoInput = document.getElementById('photoInput');
photoInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if(file){
    const reader = new FileReader();
    reader.onload = e => {
      document.getElementById('displayPhoto').src = e.target.result;
    };
    reader.readAsDataURL(file);
    submitProfile(file)
  }
});

// PROJECTS
// const addProjectBtn = document.getElementById('addProjectBtn');
// addProjectBtn.onclick = () => {
//   const title = document.getElementById('projectTitle').value;
//   const desc = document.getElementById('projectDesc').value;
//   if(!title || !desc) return alert('Please fill all fields');
//   const li = document.createElement('li');
//   li.innerHTML = `<strong>${title}</strong>: ${desc}`;
//   document.getElementById('projectList').appendChild(li);
//   document.getElementById('projectTitle').value='';
//   document.getElementById('projectDesc').value='';
// };
document.getElementById("addProjectForm").addEventListener("submit", async function(e) {
    e.preventDefault();  // prevent page reload

    const form = e.target;
    const formData = new FormData(form);

    // Send AJAX POST to Flask
    const res = await fetch("/add-project", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    // Show result without reloading page
    const li = document.createElement('li');
    li.innerHTML = `<strong>${data.project_details.title}</strong>: ${data.project_details.description}`;
    document.getElementById('projectList').appendChild(li);
    document.getElementById('projectTitle').value='';
    document.getElementById('projectDesc').value='';
});

// VERIFICATION
const submitVerificationBtn = document.getElementById('submitVerificationBtn');
submitVerificationBtn.onclick = () => {
  document.getElementById('verificationStatus').textContent='Pending';
  alert('Verification submitted. Waiting for admin approval.');
};

// SETTINGS - DARK MODE
const darkModeToggle = document.getElementById('darkModeToggle');
darkModeToggle.addEventListener('change', () => {
  const body = document.querySelector('body');
  const main = document.querySelector('.main');
  if(darkModeToggle.checked){
    body.classList.add('dark')
    main.classList.add('dark')
  } else {
    if (body.classList.contains('dark')) {
      body.classList.remove('dark')
      main.classList.remove('dark')
    }
  }
});

// PROFILE PIC SUBMIT
async function submitProfile(file) {
    var formData = new FormData();
    formData.append("file", file);

    // Send AJAX POST to Flask
    const res = await fetch("/upload_profile", {
        method: "POST",
        body: formData
    });

    const response = await res.json();

    console.log(response);
    if (response.messages) {
        response.messages.forEach(function(message) {
            alert(message);
        });
    }
}
