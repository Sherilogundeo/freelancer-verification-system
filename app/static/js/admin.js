// Sidebar navigation
const menuItems = document.querySelectorAll('.sidebar ul li');
const sections = document.querySelectorAll('.section');

menuItems.forEach(item => {
    item.addEventListener('click', () => {
        menuItems.forEach(i => i.classList.remove('active'));
        item.classList.add('active');

        sections.forEach(sec => sec.classList.remove('active'));
        document.getElementById(item.dataset.section).classList.add('active');
    });
});

// Dark mode toggle
const themeToggle = document.getElementById('themeToggle');

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
});

// Freelancers verify
document.querySelectorAll(".verifyBtn").forEach(btn => {
    btn.addEventListener("click", async () => {
        const userId = btn.dataset.userId;

        const res = await fetch("/verify-user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: userId })
        });

        const data = await res.json();
        if (data.success) {
            location.reload(); // reload to update UI
        }
    });
});

// Analytics graphs
const ctx1 = document.getElementById('performanceGraph');
new Chart(ctx1, {
    type: 'line',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        datasets: [{
            label: 'System Performance',
            data: [12, 19, 3, 5, 2]
        }]
    }
});

const ctx2 = document.getElementById('sessionsGraph');
new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        datasets: [{
            label: 'Active Sessions',
            data: [20, 30, 25, 28, 32]
        }]
    }
});

