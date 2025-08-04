// API Configuration
const API_BASE_URL = '/api';

// Global variables
let currentUser = null;

// DOM Elements
const studentForm = document.getElementById('studentForm');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const editModal = document.getElementById('editModal');
const deleteModal = document.getElementById('deleteModal');
const attendanceModal = document.getElementById('attendanceModal');
const editForm = document.getElementById('editForm');
const notification = document.getElementById('notification');
const logoutBtn = document.getElementById('logoutBtn');
const userName = document.getElementById('userName');

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    
    // Form submission
    studentForm.addEventListener('submit', handleAddStudent);
    
    // Search functionality
    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    
    // Edit form submission
    editForm.addEventListener('submit', handleUpdateStudent);
    
    // Logout button
    logoutBtn.addEventListener('click', handleLogout);
    
    // Modal close events
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            closeModal();
            closeDeleteModal();
            closeAttendanceModal();
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === editModal) {
            closeModal();
        }
        if (e.target === deleteModal) {
            closeDeleteModal();
        }
        if (e.target === attendanceModal) {
            closeAttendanceModal();
        }
    });
});

// Authentication
async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE_URL}/user`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            window.location.href = '/login';
            return;
        }
        
        currentUser = await response.json();
        userName.textContent = currentUser.name;
        
    } catch (error) {
        console.error('Auth check failed:', error);
        window.location.href = '/login';
    }
}

async function handleLogout() {
    try {
        await fetch('/logout', {
            method: 'GET',
            credentials: 'include'
        });
        window.location.href = '/login';
    } catch (error) {
        showNotification('Logout failed', 'error');
    }
}

// API Functions
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'include',
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Something went wrong');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Student Management Functions
async function handleAddStudent(e) {
    e.preventDefault();
    
    const formData = new FormData(studentForm);
    const studentData = {
        name: formData.get('name'),
        dob: formData.get('dob'),
        class: formData.get('class')
    };
    
    try {
        await fetchAPI('/students', {
            method: 'POST',
            body: JSON.stringify(studentData)
        });
        
        showNotification('Student added successfully!', 'success');
        studentForm.reset();
        
        // Redirect to students list page to see the new student
        window.location.href = '/students_list';
        
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

async function handleUpdateStudent(e) {
    e.preventDefault();
    
    const formData = new FormData(editForm);
    const studentData = {
        name: formData.get('name'),
        dob: formData.get('dob'),
        class: formData.get('class')
    };
    
    try {
        await fetchAPI(`/students/${currentStudentId}`, {
            method: 'PUT',
            body: JSON.stringify(studentData)
        });
        
        showNotification('Student updated successfully!', 'success');
        closeModal();
        
        // Redirect to students list page to see the updated student
        window.location.href = '/students_list';
        
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

async function handleSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        showNotification('Please enter a search term', 'info');
        return;
    }
    
    try {
        const students = await fetchAPI(`/students/search?q=${encodeURIComponent(query)}`);
        
        if (students.length === 0) {
            showNotification('No students found matching your search', 'info');
        } else {
            // Redirect to students list page with search results
            window.location.href = `/students_list?search=${encodeURIComponent(query)}`;
        }
        
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

// Modal Functions
function editStudent(studentId) {
    // This function is kept for compatibility but redirects to students list
    window.location.href = `/students_list?edit=${studentId}`;
}

function closeModal() {
    editModal.style.display = 'none';
    editForm.reset();
}

function confirmDelete(studentId, studentName) {
    // This function is kept for compatibility but redirects to students list
    window.location.href = `/students_list?delete=${studentId}`;
}

function closeDeleteModal() {
    deleteModal.style.display = 'none';
}

async function viewAttendance(studentId) {
    // This function is kept for compatibility but redirects to students list
    window.location.href = `/students_list?attendance=${studentId}`;
}

function closeAttendanceModal() {
    attendanceModal.style.display = 'none';
}

// Utility Functions
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type} show`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
} 