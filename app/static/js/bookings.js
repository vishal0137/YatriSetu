// Bookings Management JavaScript

let allBookings = [];
let filteredBookings = [];
let currentPage = 1;
const itemsPerPage = 10;

document.addEventListener('DOMContentLoaded', function() {
    loadBookings();
    loadStats();
});

async function loadBookings() {
    try {
        const response = await fetch('/admin/api/bookings/all');
        const result = await response.json();
        
        if (result.success) {
            allBookings = result.data;
            filteredBookings = [...allBookings];
            currentPage = 1;
            displayBookings();
            if (result.data.length === 0) {
                showAlert('No bookings found. Please import database.', 'info');
            }
        } else {
            showAlert('Failed to load bookings: ' + result.error, 'danger');
        }
    } catch (error) {
        showAlert('Database connection error.', 'danger');
        displayNoData();
    }
}

async function loadStats() {
    try {
        const response = await fetch('/admin/api/bookings/stats');
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('totalBookings').textContent = result.data.total.toLocaleString();
            document.getElementById('confirmedBookings').textContent = result.data.confirmed.toLocaleString();
            document.getElementById('pendingBookings').textContent = result.data.pending.toLocaleString();
            document.getElementById('cancelledBookings').textContent = result.data.cancelled.toLocaleString();
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function displayBookings() {
    const tbody = document.getElementById('bookingsTable');
    tbody.innerHTML = '';
    
    if (filteredBookings.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No bookings found</td></tr>';
        updatePagination(0);
        return;
    }
    
    // Calculate pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedBookings = filteredBookings.slice(startIndex, endIndex);
    
    paginatedBookings.forEach(booking => {
        const statusClass = {
            'confirmed': 'success',
            'pending': 'warning',
            'cancelled': 'danger',
            'completed': 'info'
        }[booking.status] || 'secondary';
        
        const row = `
            <tr>
                <td><strong>${booking.booking_reference}</strong></td>
                <td>${booking.passenger_name}</td>
                <td>${booking.route_number || 'N/A'}</td>
                <td>${new Date(booking.journey_date).toLocaleDateString()}</td>
                <td>₹${parseFloat(booking.fare_amount).toFixed(2)}</td>
                <td><span class="badge bg-secondary">${booking.passenger_category}</span></td>
                <td><span class="badge bg-${statusClass}">${booking.status}</span></td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="viewBooking(${booking.id})">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
    
    updatePagination(filteredBookings.length);
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
            Showing ${((currentPage - 1) * itemsPerPage) + 1} to ${Math.min(currentPage * itemsPerPage, totalItems)} of ${totalItems} bookings
        </div>
    `;
    
    paginationContainer.innerHTML = paginationHTML;
}

function changePage(page) {
    const totalPages = Math.ceil(filteredBookings.length / itemsPerPage);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    displayBookings();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function displayNoData() {
    const tbody = document.getElementById('bookingsTable');
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

function filterBookings() {
    const statusFilter = document.getElementById('statusFilter').value.toLowerCase();
    const dateFilter = document.getElementById('dateFilter').value;
    const searchFilter = document.getElementById('searchFilter').value.toLowerCase();
    
    filteredBookings = allBookings.filter(booking => {
        const matchStatus = !statusFilter || booking.status.toLowerCase() === statusFilter;
        const matchDate = !dateFilter || booking.journey_date.startsWith(dateFilter);
        const matchSearch = !searchFilter || 
            booking.booking_reference.toLowerCase().includes(searchFilter) ||
            booking.passenger_name.toLowerCase().includes(searchFilter);
        
        return matchStatus && matchDate && matchSearch;
    });
    
    currentPage = 1;
    displayBookings();
}

function clearFilters() {
    document.getElementById('statusFilter').value = '';
    document.getElementById('dateFilter').value = '';
    document.getElementById('searchFilter').value = '';
    filteredBookings = [...allBookings];
    currentPage = 1;
    displayBookings();
}

function refreshBookings() {
    loadBookings();
    loadStats();
}

function exportBookings() {
    showInfoPanel(
        'Export Bookings',
        'Export functionality is coming soon! You will be able to export bookings in CSV, Excel, and PDF formats.',
        'info',
        4000
    );
}

function viewBooking(id) {
    const booking = allBookings.find(b => b.id === id);
    if (booking) {
        const bookingData = {
            'Booking Reference': booking.booking_reference,
            'Passenger Name': booking.passenger_name,
            'Passenger Category': booking.passenger_category,
            'Route Number': booking.route_number || 'N/A',
            'Journey Date': new Date(booking.journey_date).toLocaleString('en-IN', {
                dateStyle: 'full',
                timeStyle: 'short'
            }),
            'Fare Amount': '₹' + parseFloat(booking.fare_amount).toFixed(2),
            'Status': booking.status.toUpperCase(),
            'Booking ID': '#' + booking.id
        };
        
        const actions = [
            {
                label: 'Close',
                icon: 'fa-times',
                primary: false,
                onclick: 'closeDetailsModal()'
            },
            {
                label: 'Print Ticket',
                icon: 'fa-print',
                primary: true,
                onclick: `printBooking(${id})`
            }
        ];
        
        showDetailsModal('Booking Details', bookingData, actions);
    }
}

function printBooking(id) {
    closeDetailsModal();
    showInfoPanel('Print Ticket', 'Print functionality will be available soon!', 'info', 3000);
}
