// Students List JavaScript
let students = [];
let currentView = 'table';

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadStudents();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Edit form submission
    document.getElementById('editStudentForm').addEventListener('submit', function(e) {
        e.preventDefault();
        updateStudent();
    });

    // Delete confirmation
    document.getElementById('confirmDeleteStudentBtn').addEventListener('click', function() {
        deleteStudent();
    });

    // Modal close events
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            closeAllModals();
        });
    });

    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            closeAllModals();
        }
    });
}

// Load students from the server
async function loadStudents() {
    try {
        const response = await fetch('/api/students');
        if (response.ok) {
            students = await response.json();
            renderStudents();
        } else {
            showNotification('Failed to load students', 'error');
        }
    } catch (error) {
        console.error('Error loading students:', error);
        showNotification('Error loading students', 'error');
    }
}

// Render students in current view
function renderStudents() {
    if (currentView === 'table') {
        renderTableView();
    } else {
        renderCardView();
    }
}

// Render table view
function renderTableView() {
    const tbody = document.querySelector('#studentsTable tbody');
    tbody.innerHTML = '';

    if (students.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 40px;">
                    <div class="empty-state">
                        <i class="fas fa-users" style="font-size: 3rem; color: #ccc; margin-bottom: 20px;"></i>
                        <h3>No students found</h3>
                        <p>Add students from the dashboard</p>
                    </div>
                </td>
            </tr>
        `;
        return;
    }

    students.forEach(student => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><span class="student-roll-number">${student.roll_number}</span></td>
            <td><span class="student-name">${student.name}</span></td>
            <td><span class="student-dob">${formatDate(student.dob)}</span></td>
            <td><span class="student-class">${student.class}</span></td>
            <td class="student-actions">
                <button class="btn btn-secondary btn-sm" onclick="editStudent('${student.id}')" title="Edit">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-danger btn-sm" onclick="confirmDeleteStudent('${student.id}', '${student.name}')" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Render card view
function renderCardView() {
    const grid = document.getElementById('studentsGrid');
    grid.innerHTML = '';

    if (students.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 40px;">
                <div class="empty-state">
                    <i class="fas fa-users" style="font-size: 3rem; color: #ccc; margin-bottom: 20px;"></i>
                    <h3>No students found</h3>
                    <p>Add students from the dashboard</p>
                </div>
            </div>
        `;
        return;
    }

    students.forEach(student => {
        const card = document.createElement('div');
        card.className = 'student-card';
        card.innerHTML = `
            <div class="student-card-header">
                <div class="student-info">
                    <h3>${student.name}</h3>
                </div>
                <span class="student-roll-number-badge">${student.roll_number}</span>
            </div>
            <div class="student-details">
                <div class="student-detail-item">
                    <span class="student-detail-label">Date of Birth:</span>
                    <span class="student-detail-value">${formatDate(student.dob)}</span>
                </div>
                <div class="student-detail-item">
                    <span class="student-detail-label">Class/Course:</span>
                    <span class="student-detail-value">${student.class}</span>
                </div>
            </div>
            <div class="student-actions-card">
                <button class="btn btn-secondary btn-sm" onclick="editStudent('${student.id}')" title="Edit">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button class="btn btn-danger btn-sm" onclick="confirmDeleteStudent('${student.id}', '${student.name}')" title="Delete">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Switch to table view
function switchToTableView() {
    currentView = 'table';
    document.getElementById('tableViewBtn').classList.add('active');
    document.getElementById('cardViewBtn').classList.remove('active');
    document.getElementById('tableView').style.display = 'block';
    document.getElementById('cardView').style.display = 'none';
    renderStudents();
}

// Switch to card view
function switchToCardView() {
    currentView = 'card';
    document.getElementById('cardViewBtn').classList.add('active');
    document.getElementById('tableViewBtn').classList.remove('active');
    document.getElementById('cardView').style.display = 'block';
    document.getElementById('tableView').style.display = 'none';
    renderStudents();
}

// Edit student
function editStudent(studentId) {
    const student = students.find(s => s.id === studentId);
    if (!student) return;

    document.getElementById('editStudentId').value = student.id;
    document.getElementById('editStudentName').value = student.name;
    document.getElementById('editStudentDob').value = student.dob;
    document.getElementById('editStudentClass').value = student.class;
    document.getElementById('editStudentRollNumber').value = student.roll_number;

    document.getElementById('editStudentModal').style.display = 'block';
}

// Update student
async function updateStudent() {
    const studentId = document.getElementById('editStudentId').value;
    const formData = new FormData(document.getElementById('editStudentForm'));
    
    try {
        const response = await fetch(`/api/students/${studentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: formData.get('name'),
                dob: formData.get('dob'),
                class: formData.get('class')
            })
        });

        if (response.ok) {
            showNotification('Student updated successfully', 'success');
            closeEditStudentModal();
            loadStudents();
        } else {
            const error = await response.json();
            showNotification(error.message || 'Failed to update student', 'error');
        }
    } catch (error) {
        console.error('Error updating student:', error);
        showNotification('Error updating student', 'error');
    }
}

// Confirm delete student
function confirmDeleteStudent(studentId, studentName) {
    document.getElementById('deleteStudentName').textContent = studentName;
    document.getElementById('confirmDeleteStudentBtn').onclick = () => deleteStudent(studentId);
    document.getElementById('deleteStudentModal').style.display = 'block';
}

// Delete student
async function deleteStudent(studentId) {
    try {
        const response = await fetch(`/api/students/${studentId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showNotification('Student deleted successfully', 'success');
            closeDeleteStudentModal();
            loadStudents();
        } else {
            const error = await response.json();
            showNotification(error.message || 'Failed to delete student', 'error');
        }
    } catch (error) {
        console.error('Error deleting student:', error);
        showNotification('Error deleting student', 'error');
    }
}

// Close edit student modal
function closeEditStudentModal() {
    document.getElementById('editStudentModal').style.display = 'none';
    document.getElementById('editStudentForm').reset();
}

// Close delete student modal
function closeDeleteStudentModal() {
    document.getElementById('deleteStudentModal').style.display = 'none';
}

// Close all modals
function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type} show`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
} 