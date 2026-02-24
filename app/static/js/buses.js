// Buses Management JavaScript

let allBuses = [];
let filteredBuses = [];
let currentPage = 1;
const itemsPerPage = 10;

document.addEventListener('DOMContentLoaded', function() {
    loadBuses();
    loadStats();
});

async function loadBuses() {
    try {
        const response = await fetch('/admin/api/buses/all');
        const result = await response.json();
        
        if (result.success) {
            allBuses = result.data;
            filteredBuses = [...allBuses];
            currentPage = 1;
            displayBuses();
            if (result.data.length === 0) {
                showAlert('No buses found. Please import database.', 'info');
            }
        } else {
            showAlert('Failed to load buses: ' + result.error, 'danger');
        }
    } catch (error) {
        showAlert('Database connection error.', 'danger');
        displayNoData();
    }
}

async function loadStats() {
    try {
        const response = await fetch('/admin/api/buses/stats');
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('totalBuses').textContent = result.data.total;
            document.getElementById('activeBuses').textContent = result.data.active;
            document.getElementById('acBuses').textContent = result.data.ac_buses;
            document.getElementById('avgCapacity').textContent = result.data.avg_capacity;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function displayBuses() {
    const tbody = document.getElementById('busesTable');
    tbody.innerHTML = '';
    
    if (filteredBuses.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No buses found</td></tr>';
        updatePagination(0);
        return;
    }
    
    // Calculate pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedBuses = filteredBuses.slice(startIndex, endIndex);
    
    paginatedBuses.forEach(bus => {
        const row = `
            <tr>
                <td><strong>${bus.bus_number}</strong></td>
                <td>${bus.registration_number}</td>
                <td><span class="badge bg-info">${bus.bus_type}</span></td>
                <td>${bus.capacity} seats</td>
                <td><span class="badge bg-${bus.is_active ? 'success' : 'danger'}">${bus.is_active ? 'Active' : 'Inactive'}</span></td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="viewBus(${bus.id})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-warning" onclick="editBus(${bus.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
    
    updatePagination(filteredBuses.length);
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
    const totalPages = Math.ceil(filteredBuses.length / itemsPerPage);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    displayBuses();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function displayNoData() {
    const tbody = document.getElementById('busesTable');
    tbody.innerHTML = `
        <tr>
            <td colspan="6" class="text-center">
                <div class="py-4">
                    <i class="fas fa-database fa-3x text-muted mb-3"></i>
                    <p class="text-muted">No database connection</p>
                </div>
            </td>
        </tr>
    `;
    updatePagination(0);
}

function addBus() {
    showInfoPanel(
        'Add New Bus',
        'Bus registration form is coming soon! You will be able to add new buses to the fleet with complete details.',
        'info',
        4000
    );
}

function viewBus(id) {
    const bus = allBuses.find(b => b.id === id);
    if (bus) {
        const busData = {
            'Bus Number': bus.bus_number,
            'Registration Number': bus.registration_number,
            'Bus Type': bus.bus_type,
            'Capacity': bus.capacity + ' seats',
            'Status': bus.is_active ? 'Active' : 'Inactive',
            'Bus ID': '#' + bus.id
        };
        
        const actions = [
            {
                label: 'Close',
                icon: 'fa-times',
                primary: false,
                onclick: 'closeDetailsModal()'
            },
            {
                label: 'Edit Bus',
                icon: 'fa-edit',
                primary: true,
                onclick: `editBus(${id})`
            }
        ];
        
        showDetailsModal('Bus Details', busData, actions);
    }
}

function editBus(id) {
    closeDetailsModal();
    showInfoPanel(
        'Edit Bus',
        'Bus editing form is coming soon! You will be able to update bus information and status.',
        'info',
        4000
    );
}
