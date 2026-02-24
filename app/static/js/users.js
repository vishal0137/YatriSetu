// Users Management JavaScript

let allUsers = [];
let filteredUsers = [];
let currentPage = 1;
const itemsPerPage = 10;

document.addEventListener('DOMContentLoaded', function() {
    loadUsers();
    loadStats();
});

async function loadUsers() {
    try {
        const response = await fetch('/admin/api/users/all');
        const result = await response.json();
        
        if (result.success) {
            allUsers = result.data;
            filteredUsers = [...allUsers];
            currentPage = 1;
            displayUsers();
            if (result.data.length === 0) {
                showAlert('No users found. Please import database.', 'info');
            }
        } else {
            showAlert('Failed to load users: ' + result.error, 'danger');
        }
    } catch (error) {
        showAlert('Database connection error.', 'danger');
        displayNoData();
    }
}

async function loadStats() {
    try {
        const response = await fetch('/admin/api/users/stats');
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('totalUsers').textContent = result.data.total;
            document.getElementById('activeUsers').textContent = result.data.active;
            document.getElementById('adminUsers').textContent = result.data.admins;
            document.getElementById('passengerUsers').textContent = result.data.passengers;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function displayUsers() {
    const tbody = document.getElementById('usersTable');
    tbody.innerHTML = '';
    
    if (filteredUsers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No users found</td></tr>';
        updatePagination(0);
        return;
    }
    
    // Calculate pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedUsers = filteredUsers.slice(startIndex, endIndex);
    
    paginatedUsers.forEach(user => {
        const joinDate = user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A';
        const row = `
            <tr>
                <td><strong>${user.full_name}</strong></td>
                <td>${user.email}</td>
                <td>${user.phone || 'N/A'}</td>
                <td><span class="badge bg-primary">${user.role}</span></td>
                <td><span class="badge bg-${user.is_active ? 'success' : 'danger'}">${user.is_active ? 'Active' : 'Inactive'}</span></td>
                <td>${joinDate}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="viewUser(${user.id})" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-warning" onclick="editUser(${user.id})" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
    
    updatePagination(filteredUsers.length);
}

function updatePagination(totalItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const paginationContainer = document.getElementById('paginationContainer');
    
    if (!paginationContainer || totalPages <= 1) {
        if (paginationContainer) paginationContainer.innerHTML = '';
        return;
    }
    
    let paginationHTML = `
        <nav aria-label="Page navigation">
            <ul class="pagination justify-content-center mb-0">
                <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                    <a class="page-link" href="#" onclick="changePage(${currentPage - 1}); return false;">
                        <i class="fas fa-chevron-left"></i>
                    </a>
                </li>
    `;
    
    // Show page numbers
    const maxVisiblePages = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
    
    if (endPage - startPage < maxVisiblePages - 1) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
    
    if (startPage > 1) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="changePage(1); return false;">1</a>
            </li>
        `;
        if (startPage > 2) {
            paginationHTML += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        paginationHTML += `
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <a class="page-link" href="#" onclick="changePage(${i}); return false;">${i}</a>
            </li>
        `;
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            paginationHTML += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
        }
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="changePage(${totalPages}); return false;">${totalPages}</a>
            </li>
        `;
    }
    
    paginationHTML += `
                <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                    <a class="page-link" href="#" onclick="changePage(${currentPage + 1}); return false;">
                        <i class="fas fa-chevron-right"></i>
                    </a>
                </li>
            </ul>
        </nav>
        <div class="text-center mt-2 text-muted small">
            Showing ${((currentPage - 1) * itemsPerPage) + 1} to ${Math.min(currentPage * itemsPerPage, totalItems)} of ${totalItems} entries
        </div>
    `;
    
    paginationContainer.innerHTML = paginationHTML;
}

function changePage(page) {
    const totalPages = Math.ceil(filteredUsers.length / itemsPerPage);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    displayUsers();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function displayNoData() {
    const tbody = document.getElementById('usersTable');
    tbody.innerHTML = `
        <tr>
            <td colspan="7" class="text-center">
                <div class="py-4">
                    <i class="fas fa-database fa-3x text-muted mb-3"></i>
                    <p class="text-muted">No database connection</p>
                </div>
            </td>
        </tr>
    `;
    updatePagination(0);
}

function filterUsers() {
    const roleFilter = document.getElementById('roleFilter').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value.toLowerCase();
    const searchFilter = document.getElementById('searchFilter').value.toLowerCase();
    
    filteredUsers = allUsers.filter(user => {
        const matchesRole = !roleFilter || user.role.toLowerCase().includes(roleFilter);
        const matchesStatus = !statusFilter || (user.is_active && statusFilter === 'active') || (!user.is_active && statusFilter === 'inactive');
        const matchesSearch = !searchFilter || 
            user.full_name.toLowerCase().includes(searchFilter) || 
            user.email.toLowerCase().includes(searchFilter);
        
        return matchesRole && matchesStatus && matchesSearch;
    });
    
    currentPage = 1;
    displayUsers();
}

function clearFilters() {
    document.getElementById('roleFilter').value = '';
    document.getElementById('statusFilter').value = '';
    document.getElementById('searchFilter').value = '';
    filteredUsers = [...allUsers];
    currentPage = 1;
    displayUsers();
}

function refreshUsers() {
    loadUsers();
    loadStats();
}

function exportUsers() {
    showInfoPanel(
        'Export Users',
        'Export functionality is coming soon! You will be able to export user data in CSV and Excel formats.',
        'info',
        4000
    );
}

function addUser() {
    showInfoPanel(
        'Add New User',
        'User creation form is coming soon! You will be able to add new users with role assignments.',
        'info',
        4000
    );
}

function viewUser(id) {
    const user = allUsers.find(u => u.id === id);
    if (user) {
        const userData = {
            'Full Name': user.full_name,
            'Email': user.email,
            'Phone': user.phone || 'Not provided',
            'Role': user.role.toUpperCase(),
            'Status': user.is_active ? 'Active' : 'Inactive',
            'Joined Date': user.created_at ? new Date(user.created_at).toLocaleDateString('en-IN', {
                dateStyle: 'full'
            }) : 'N/A',
            'User ID': '#' + user.id
        };
        
        const actions = [
            {
                label: 'Close',
                icon: 'fa-times',
                primary: false,
                onclick: 'closeDetailsModal()'
            },
            {
                label: 'Edit User',
                icon: 'fa-edit',
                primary: true,
                onclick: `editUser(${id})`
            }
        ];
        
        showDetailsModal('User Details', userData, actions);
    }
}

function editUser(id) {
    closeDetailsModal();
    showInfoPanel(
        'Edit User',
        'User editing form is coming soon! You will be able to update user information and permissions.',
        'info',
        4000
    );
}
