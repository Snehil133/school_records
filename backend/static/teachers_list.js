document.addEventListener('DOMContentLoaded', function() {
    loadTeachers();
});

async function loadTeachers() {
    try {
        const response = await fetch('/api/teachers', { credentials: 'include' });
        if (!response.ok) throw new Error('Failed to load teachers');
        const teachers = await response.json();
        renderTeachersTable(teachers);
        renderTeachersCards(teachers);
    } catch (error) {
        console.error('Error loading teachers:', error);
        const tbody = document.querySelector('#teachersTable tbody');
        if (tbody) tbody.innerHTML = `<tr><td colspan="5">Failed to load teachers</td></tr>`;
        const grid = document.querySelector('#teachersGrid');
        if (grid) grid.innerHTML = '<div style="text-align: center; color: #666; padding: 40px;">Failed to load teachers</div>';
    }
}

function renderTeachersTable(teachers) {
    const tbody = document.querySelector('#teachersTable tbody');
    if (!tbody) return;
    if (!teachers || teachers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5">No teachers found</td></tr>`;
        return;
    }
    tbody.innerHTML = teachers.map(teacher => {
        // Format password history properly
        const historyItems = (teacher.password_history || []).map(h => 
            `<div class="password-history-item">
                <span class="password-history-hash" title="${h.password}">${h.password.substring(0, 20)}...</span>
                <span class="password-history-date">${formatDate(h.changed_at)}</span>
            </div>`
        ).join('');
        
        return `
            <tr>
                <td><span class="teacher-username">${escapeHtml(teacher.username)}</span></td>
                <td><span class="teacher-name">${escapeHtml(teacher.name || 'N/A')}</span></td>
                <td><span class="password-hash" title="${teacher.password}">${teacher.password.substring(0, 20)}...</span></td>
                <td class="password-history">${historyItems || '<span style="color: #999; font-style: italic;">No password history</span>'}</td>
                <td class="teacher-actions">
                    <button class="btn btn-secondary btn-sm" onclick="editTeacher('${teacher.username}', '${escapeHtml(teacher.name || '')}')">
                        <i class="fas fa-edit"></i> Edit Name
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

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

// Teacher edit functionality
let currentEditTeacher = null;

function editTeacher(username, currentName) {
    currentEditTeacher = username;
    document.getElementById('editTeacherUsername').value = username;
    document.getElementById('editTeacherName').value = currentName;
    document.getElementById('editTeacherModal').style.display = 'block';
}

function closeEditTeacherModal() {
    document.getElementById('editTeacherModal').style.display = 'none';
    currentEditTeacher = null;
    document.getElementById('editTeacherForm').reset();
}

// Handle edit teacher form submission
document.addEventListener('DOMContentLoaded', function() {
    const editTeacherForm = document.getElementById('editTeacherForm');
    if (editTeacherForm) {
        editTeacherForm.addEventListener('submit', handleEditTeacher);
    }
});

async function handleEditTeacher(e) {
    e.preventDefault();
    
    const formData = new FormData(editTeacherForm);
    const teacherData = {
        name: formData.get('name').trim()
    };
    
    if (!teacherData.name) {
        alert('Name is required');
        return;
    }
    
    try {
        const response = await fetch(`/api/teachers/${currentEditTeacher}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(teacherData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to update teacher');
        }
        
        const result = await response.json();
        closeEditTeacherModal();
        loadTeachers(); // Reload the teachers list
        alert('Teacher name updated successfully!');
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Card view rendering
function renderTeachersCards(teachers) {
    const grid = document.querySelector('#teachersGrid');
    if (!grid) return;
    if (!teachers || teachers.length === 0) {
        grid.innerHTML = '<div style="text-align: center; color: #666; padding: 40px;">No teachers found</div>';
        return;
    }
    
    grid.innerHTML = teachers.map(teacher => {
        const historyItems = (teacher.password_history || []).map(h => 
            `<div class="password-history-item">
                <span class="password-history-hash">${h.password}</span>
                <span class="password-history-date">${formatDate(h.changed_at)}</span>
            </div>`
        ).join('');
        
        return `
            <div class="teacher-card">
                <div class="teacher-card-header">
                    <div class="teacher-info">
                        <h3>${escapeHtml(teacher.name || 'N/A')}</h3>
                        <span class="teacher-username-badge">${escapeHtml(teacher.username)}</span>
                    </div>
                    <span class="teacher-role-badge">Teacher</span>
                </div>
                <div class="teacher-details">
                    <div class="teacher-detail-item">
                        <span class="teacher-detail-label">Current Password:</span>
                        <span class="teacher-detail-value password-hash" title="${teacher.password}">${teacher.password.substring(0, 20)}...</span>
                    </div>
                    <div class="teacher-detail-item">
                        <span class="teacher-detail-label">Password History:</span>
                        <div class="password-history">
                            ${historyItems || '<span style="color: #999; font-style: italic;">No password history</span>'}
                        </div>
                    </div>
                </div>
                <div class="teacher-actions-card">
                    <button class="btn btn-secondary btn-sm" onclick="editTeacher('${teacher.username}', '${escapeHtml(teacher.name || '')}')">
                        <i class="fas fa-edit"></i> Edit Name
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// View switching functions
function switchToTableView() {
    document.getElementById('tableView').style.display = 'block';
    document.getElementById('cardView').style.display = 'none';
    document.getElementById('tableViewBtn').classList.add('active');
    document.getElementById('tableViewBtn').classList.remove('btn-outline');
    document.getElementById('tableViewBtn').classList.add('btn-secondary');
    document.getElementById('cardViewBtn').classList.remove('active');
    document.getElementById('cardViewBtn').classList.remove('btn-secondary');
    document.getElementById('cardViewBtn').classList.add('btn-outline');
}

function switchToCardView() {
    document.getElementById('tableView').style.display = 'none';
    document.getElementById('cardView').style.display = 'block';
    document.getElementById('cardViewBtn').classList.add('active');
    document.getElementById('cardViewBtn').classList.remove('btn-outline');
    document.getElementById('cardViewBtn').classList.add('btn-secondary');
    document.getElementById('tableViewBtn').classList.remove('active');
    document.getElementById('tableViewBtn').classList.remove('btn-secondary');
    document.getElementById('tableViewBtn').classList.add('btn-outline');
}

// Global functions for onclick handlers
window.editTeacher = editTeacher;
window.closeEditTeacherModal = closeEditTeacherModal;
window.switchToTableView = switchToTableView;
window.switchToCardView = switchToCardView; 