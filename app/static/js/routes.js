// Routes Management JavaScript

let allRoutes = [];
let filteredRoutes = [];
let currentPage = 1;
const itemsPerPage = 10;

document.addEventListener('DOMContentLoaded', function() {
    loadRoutes();
    loadStats();
});

async function loadRoutes() {
    try {
        const response = await fetch('/admin/api/routes/all');
        const result = await response.json();
        
        if (result.success) {
            allRoutes = result.data;
            filteredRoutes = [...allRoutes];
            currentPage = 1;
            displayRoutes();
            if (result.data.length === 0) {
                showAlert('No routes found. Please import database.', 'info');
            }
        } else {
            showAlert('Failed to load routes: ' + result.error, 'danger');
        }
    } catch (error) {
        showAlert('Database connection error.', 'danger');
        displayNoData();
    }
}

async function loadStats() {
    try {
        const response = await fetch('/admin/api/routes/stats');
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('totalRoutes').textContent = result.data.total;
            document.getElementById('activeRoutes').textContent = result.data.active;
            document.getElementById('totalDistance').textContent = result.data.total_distance + ' km';
            document.getElementById('avgFare').textContent = '₹' + result.data.avg_fare;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function displayRoutes() {
    const tbody = document.getElementById('routesTable');
    tbody.innerHTML = '';
    
    if (filteredRoutes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No routes found</td></tr>';
        updatePagination(0);
        return;
    }
    
    // Calculate pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedRoutes = filteredRoutes.slice(startIndex, endIndex);
    
    paginatedRoutes.forEach(route => {
        const row = `
            <tr>
                <td><strong>${route.route_number}</strong></td>
                <td>${route.route_name}</td>
                <td>${route.start_location}</td>
                <td>${route.end_location}</td>
                <td>${route.distance_km} km</td>
                <td>₹${route.fare}</td>
                <td><span class="badge bg-${route.is_active ? 'success' : 'danger'}">${route.is_active ? 'Active' : 'Inactive'}</span></td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="viewRoute(${route.id})" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-warning" onclick="editRoute(${route.id})" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
    
    updatePagination(filteredRoutes.length);
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
    const totalPages = Math.ceil(filteredRoutes.length / itemsPerPage);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    displayRoutes();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function displayNoData() {
    const tbody = document.getElementById('routesTable');
    tbody.innerHTML = `
        <tr>
            <td colspan="8" class="text-center">
                <div class="py-4">
                    <i class="fas fa-database fa-3x text-muted mb-3"></i>
                    <p class="text-muted">No database connection</p>
                </div>
            </td>
        </tr>
    `;
    updatePagination(0);
}

function filterRoutes() {
    const statusFilter = document.getElementById('statusFilter').value.toLowerCase();
    const searchFilter = document.getElementById('searchFilter').value.toLowerCase();
    
    filteredRoutes = allRoutes.filter(route => {
        const matchesStatus = !statusFilter || (route.is_active && statusFilter === 'active') || (!route.is_active && statusFilter === 'inactive');
        const matchesSearch = !searchFilter || 
            route.route_number.toLowerCase().includes(searchFilter) || 
            route.route_name.toLowerCase().includes(searchFilter);
        
        return matchesStatus && matchesSearch;
    });
    
    currentPage = 1;
    displayRoutes();
}

function clearFilters() {
    document.getElementById('statusFilter').value = '';
    document.getElementById('searchFilter').value = '';
    filteredRoutes = [...allRoutes];
    currentPage = 1;
    displayRoutes();
}

function refreshRoutes() {
    loadRoutes();
    loadStats();
}

function exportRoutes() {
    showInfoPanel(
        'Export Routes',
        'Export functionality is coming soon! You will be able to export route data in CSV and Excel formats.',
        'info',
        4000
    );
}

function addRoute() {
    showInfoPanel(
        'Add New Route',
        'Route creation form is coming soon! You will be able to add new routes with stops and fare details.',
        'info',
        4000
    );
}

function viewRoute(id) {
    const route = allRoutes.find(r => r.id === id);
    if (route) {
        const routeData = {
            'Route Number': route.route_number,
            'Route Name': route.route_name,
            'Start Location': route.start_location,
            'End Location': route.end_location,
            'Distance': route.distance_km + ' km',
            'Fare': '₹' + route.fare,
            'Status': route.is_active ? 'Active' : 'Inactive',
            'Route ID': '#' + route.id
        };
        
        const actions = [
            {
                label: 'Close',
                icon: 'fa-times',
                primary: false,
                onclick: 'closeDetailsModal()'
            },
            {
                label: 'Edit Route',
                icon: 'fa-edit',
                primary: true,
                onclick: `editRoute(${id})`
            }
        ];
        
        showDetailsModal('Route Details', routeData, actions);
    }
}

function editRoute(id) {
    closeDetailsModal();
    showInfoPanel(
        'Edit Route',
        'Route editing form is coming soon! You will be able to update route information and fare.',
        'info',
        4000
    );
}
