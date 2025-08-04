// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global variables
let students = [];
let currentStudentId = null;

// DOM Elements
const studentForm = document.getElementById('studentForm');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const refreshBtn = document.getElementById('refreshBtn');
const studentsList = document.getElementById('studentsList');
const studentCount = document.getElementById('studentCount');
const editModal = document.getElementById('editModal');
const deleteModal = document.getElementById('deleteModal');
const editForm = document.getElementById('editForm');
const notification = document.getElementById('notification');

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    loadStudents();
    
    // Form submission
    studentForm.addEventListener('submit', handleAddStudent);
    
    // Search functionality
    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    
    // Refresh button
    refreshBtn.addEventListener('click', loadStudents);
    
    // Edit form submission
    editForm.addEventListener('submit', handleUpdateStudent);
    
    // Modal close events
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            closeModal();
            closeDeleteModal();
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
    });
});

// API Functions
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
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

// Load all students
async function loadStudents() {
    try {
        showLoading();
        students = await fetchAPI('/students');
        displayStudents(students);
        updateStudentCount();
    } catch (error) {
        showNotification(error.message, 'error');
        displayEmptyState();
    }
}

// Add new student
async function handleAddStudent(e) {
    e.preventDefault();
    
    const formData = new FormData(studentForm);
    const studentData = {
        name: formData.get('name').trim(),
        age: parseInt(formData.get('age')),
        class: formData.get('class').trim()
    };
    
    try {
        const newStudent = await fetchAPI('/students', {
            method: 'POST',
            body: JSON.stringify(studentData)
        });
        
        students.unshift(newStudent);
        displayStudents(students);
        updateStudentCount();
        studentForm.reset();
        showNotification('Student added successfully!', 'success');
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

// Update student
async function handleUpdateStudent(e) {
    e.preventDefault();
    
    const formData = new FormData(editForm);
    const studentData = {
        name: formData.get('name').trim(),
        age: parseInt(formData.get('age')),
        class: formData.get('class').trim()
    };
    
    try {
        const updatedStudent = await fetchAPI(`/students/${currentStudentId}`, {
            method: 'PUT',
            body: JSON.stringify(studentData)
        });
        
        // Update the student in the local array
        const index = students.findIndex(s => s.id === currentStudentId);
        if (index !== -1) {
            students[index] = updatedStudent;
        }
        
        displayStudents(students);
        closeModal();
        showNotification('Student updated successfully!', 'success');
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

// Delete student
async function handleDeleteStudent(studentId) {
    try {
        await fetchAPI(`/students/${studentId}`, {
            method: 'DELETE'
        });
        
        students = students.filter(s => s.id !== studentId);
        displayStudents(students);
        updateStudentCount();
        closeDeleteModal();
        showNotification('Student deleted successfully!', 'success');
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

// Search students
async function handleSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        loadStudents();
        return;
    }
    
    try {
        showLoading();
        const searchResults = await fetchAPI(`/students/search?q=${encodeURIComponent(query)}`);
        displayStudents(searchResults);
        updateStudentCount(searchResults.length);
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

// Display functions
function displayStudents(studentsToShow) {
    if (studentsToShow.length === 0) {
        displayEmptyState();
        return;
    }
    
    studentsList.innerHTML = studentsToShow.map(student => `
        <div class="student-card">
            <div class="student-header">
                <div class="student-info">
                    <h3>${escapeHtml(student.name)}</h3>
                    <p>Roll Number: ${student.roll_number}</p>
                </div>
                <div class="student-actions">
                    <button class="btn btn-secondary btn-sm" onclick="editStudent(${student.id})">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="confirmDelete(${student.id}, '${escapeHtml(student.name)}')">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
            <div class="student-details">
                <div class="detail-item">
                    <span class="detail-label">Age</span>
                    <span class="detail-value">${student.age ? `${student.age} years` : 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Class</span>
                    <span class="detail-value">${escapeHtml(student.class)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Created</span>
                    <span class="detail-value">${formatDate(student.created_at)}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function displayEmptyState() {
    studentsList.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-user-graduate"></i>
            <h3>No students found</h3>
            <p>Add your first student using the form on the left</p>
        </div>
    `;
}

function showLoading() {
    studentsList.innerHTML = '<div class="loading">Loading students...</div>';
}

function updateStudentCount(count = null) {
    const total = count !== null ? count : students.length;
    studentCount.textContent = `${total} student${total !== 1 ? 's' : ''}`;
}

// Modal functions
function editStudent(studentId) {
    const student = students.find(s => s.id === studentId);
    if (!student) return;
    
    currentStudentId = studentId;
    
    // Populate form
    document.getElementById('editId').value = student.id;
    document.getElementById('editName').value = student.name;
    document.getElementById('editAge').value = student.age;
    document.getElementById('editClass').value = student.class;
    document.getElementById('editRollNumber').value = student.roll_number;
    
    editModal.style.display = 'block';
}

function closeModal() {
    editModal.style.display = 'none';
    currentStudentId = null;
    editForm.reset();
}

function confirmDelete(studentId, studentName) {
    currentStudentId = studentId;
    document.getElementById('deleteStudentName').textContent = studentName;
    deleteModal.style.display = 'block';
}

function closeDeleteModal() {
    deleteModal.style.display = 'none';
    currentStudentId = null;
}

// Global functions for onclick handlers
window.editStudent = editStudent;
window.confirmDelete = confirmDelete;

// Delete confirmation button
document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
    if (currentStudentId) {
        handleDeleteStudent(currentStudentId);
    }
});

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showNotification(message, type = 'info') {
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
} 