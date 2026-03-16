const API_BASE = "http://127.0.0.1:5000";

let currentUser = null;
let categoryChartInstance = null;
let monthlyChartInstance = null;

// Initialization
document.addEventListener("DOMContentLoaded", () => {
    checkAuth();
});

// Auth Handlers
function toggleAuth(view) {
    if (view === 'register') {
        document.getElementById('loginForm').classList.add('d-none');
        document.getElementById('registerForm').classList.remove('d-none');
    } else {
        document.getElementById('registerForm').classList.add('d-none');
        document.getElementById('loginForm').classList.remove('d-none');
    }
}

document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            loginUser(data);
        } else {
            alert(data.message || "Login failed");
        }
    } catch (err) {
        alert("Error connecting to server. Is backend running?");
    }
});

document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("regUsername").value;
    const password = document.getElementById("regPassword").value;

    try {
        const response = await fetch(`${API_BASE}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert("Registration successful! Please login.");
            toggleAuth('login');
            // optionally auto-login here, but we ask them to login for now
            document.getElementById("loginUsername").value = username;
            document.getElementById("loginPassword").value = password;
        } else {
            alert(data.message || "Registration failed");
        }
    } catch (err) {
        alert("Error connecting to server.");
    }
});

function loginUser(userData) {
    localStorage.setItem('expenseUser', JSON.stringify(userData));
    checkAuth();
}

function logout() {
    localStorage.removeItem('expenseUser');
    checkAuth();
}

function checkAuth() {
    const storedUser = localStorage.getItem('expenseUser');
    if (storedUser) {
        currentUser = JSON.parse(storedUser);
        document.getElementById('authView').classList.add('d-none');
        document.getElementById('dashboardView').classList.remove('d-none');
        document.getElementById('welcomeUser').innerText = `Welcome, ${currentUser.username}`;
        
        const profilePicEl = document.getElementById('navProfilePic');
        if (profilePicEl) {
            profilePicEl.src = currentUser.profile_pic ? `uploads/${currentUser.profile_pic}` : `uploads/default.png`;
        }
        
        // Load data on login
        loadExpenses();
        refreshDashboard();
    } else {
        currentUser = null;
        document.getElementById('dashboardView').classList.add('d-none');
        document.getElementById('authView').classList.remove('d-none');
    }
}

// Profile Picture Upload Handler
async function uploadProfilePic(event) {
    const file = event.target.files[0];
    if (!file || !currentUser) return;
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', currentUser.user_id);
    
    try {
        const response = await fetch(`${API_BASE}/upload-profile-pic`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        if (response.ok) {
            // Update local storage and UI
            currentUser.profile_pic = data.profile_pic;
            localStorage.setItem('expenseUser', JSON.stringify(currentUser));
            document.getElementById('navProfilePic').src = `uploads/${data.profile_pic}`;
        } else {
            alert(data.message || "Failed to upload profile picture.");
        }
    } catch (err) {
        alert("Error saving profile picture.");
    }
}

// Category Toggle Handler
function toggleCustomCategory() {
    const select = document.getElementById("category");
    const customInput = document.getElementById("customCategory");
    if (select.value === "Other") {
        customInput.classList.remove("d-none");
        customInput.required = true;
    } else {
        customInput.classList.add("d-none");
        customInput.required = false;
        customInput.value = "";
    }
}

// Expense Handlers
document.getElementById("expenseForm").addEventListener("submit", async function(e){
    e.preventDefault();
    
    if (!currentUser) return;

    const categorySelect = document.getElementById("category").value;
    const categoryCustom = document.getElementById("customCategory").value;
    const finalCategory = categorySelect === "Other" ? categoryCustom : categorySelect;
    
    if (!finalCategory) {
        alert("Please select or enter a category");
        return;
    }

    const amount = document.getElementById("amount").value;
    const date = document.getElementById("date").value;
    const payment_mode = document.getElementById("payment_mode").value;

    try {
        await fetch(`${API_BASE}/add-expense`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                category: finalCategory,
                amount: parseFloat(amount),
                date,
                payment_mode,
                user_id: currentUser.user_id
            })
        });

        // Clear form and hide custom category input
        document.getElementById("expenseForm").reset();
        document.getElementById("customCategory").classList.add("d-none");
        
        // Refresh views
        loadExpenses();
        refreshDashboard();
        
    } catch (err) {
        alert("Error adding expense");
    }
});

async function loadExpenses(){
    if (!currentUser) return;
    
    try {
        const response = await fetch(`${API_BASE}/expenses?user_id=${currentUser.user_id}`);
        const data = await response.json();
        
        const list = document.getElementById("expenseList");
        list.innerHTML = "";
        
        if (data.length === 0) {
            list.innerHTML = `<li class="list-group-item text-center text-muted">No expenses found. Add some!</li>`;
            return;
        }

        // Sort by date DESC, take top 20 for the recent list
        const sortedData = data.sort((a,b) => new Date(b.date) - new Date(a.date)).slice(0, 20);

        sortedData.forEach(exp => {
            const li = document.createElement("li");
            li.className = "list-group-item";
            
            li.innerHTML = `
                <div class="expense-item-row">
                    <span class="expense-category">${exp.category}</span>
                    <span class="expense-amount">Rs ${parseFloat(exp.amount).toFixed(2)}</span>
                </div>
                <div class="d-flex justify-content-between mt-1 text-muted small">
                    <span>${exp.date}</span>
                    <span>${exp.payment_mode}</span>
                </div>
            `;
            list.appendChild(li);
        });
    } catch (err) {
        console.error("Failed to load expenses", err);
    }
}

// Dashboard Charts
async function refreshDashboard() {
    if (!currentUser) return;
    
    try {
        const monthFilter = document.getElementById('dashboardMonthFilter').value;
        let url = `${API_BASE}/dashboard-data?user_id=${currentUser.user_id}`;
        if (monthFilter) {
            url += `&month=${monthFilter}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        // Update Total
        if (monthFilter) {
            document.querySelector('.stat-card h6').innerText = `Total Spend (${monthFilter})`;
        } else {
            document.querySelector('.stat-card h6').innerText = `Total Spend (Last 30 Days)`;
        }
        renderCategoryChart(data.category_data);
        renderMonthlyChart(data.monthly_data);
        
    } catch (err) {
        console.error("Failed to fetch dashboard data", err);
    }
}

function renderCategoryChart(catData) {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    
    if (categoryChartInstance) {
        categoryChartInstance.destroy();
    }
    
    if (catData.labels.length === 0) return;

    // Generate dynamic colors
    const bgColors = [
        'rgba(59, 130, 246, 0.8)', // Blue
        'rgba(16, 185, 129, 0.8)', // Emerald
        'rgba(245, 158, 11, 0.8)', // Amber
        'rgba(239, 68, 68, 0.8)',  // Red
        'rgba(139, 92, 246, 0.8)', // Violet
        'rgba(14, 165, 233, 0.8)', // Sky
        'rgba(244, 63, 94, 0.8)'   // Rose
    ];
    
    const borders = bgColors.map(c => c.replace('0.8', '1'));

    categoryChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: catData.labels,
            datasets: [{
                data: catData.values,
                backgroundColor: bgColors.slice(0, catData.labels.length),
                borderColor: borders.slice(0, catData.labels.length),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#e2e8f0', font: { family: 'Inter' } }
                }
            }
        }
    });
}

function renderMonthlyChart(monthData) {
    const ctx = document.getElementById('monthlyChart').getContext('2d');
    
    if (monthlyChartInstance) {
        monthlyChartInstance.destroy();
    }
    
    if (monthData.labels.length === 0) return;

    monthlyChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: monthData.labels,
            datasets: [{
                label: '30-Day Trend',
                data: monthData.values,
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(139, 92, 246, 1)',
                fill: true,
                tension: 0.4 // curve
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}