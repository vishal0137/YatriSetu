// Payments Management JavaScript

let allPayments = [];
let filteredPayments = [];
let currentPage = 1;
const itemsPerPage = 10;

document.addEventListener('DOMContentLoaded', function() {
    loadPayments();
    loadStats();
});

async function loadPayments() {
    try {
        const response = await fetch('/admin/api/payments/all');
        const result = await response.json();
        
        if (result.success) {
            allPayments = result.data;
            filteredPayments = [...allPayments];
            currentPage = 1;
            displayPayments();
            if (result.data.length === 0) {
                showAlert('No payments found. Please import database.', 'info');
            }
        } else {
            showAlert('Failed to load payments: ' + result.error, 'danger');
        }
    } catch (error) {
        showAlert('Database connection error.', 'danger');
        displayNoData();
    }
}

async function loadStats() {
    try {
        const response = await fetch('/admin/api/payments/stats');
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('totalPayments').textContent = result.data.total;
            document.getElementById('completedPayments').textContent = result.data.completed;
            document.getElementById('totalRevenue').textContent = '₹' + result.data.total_revenue.toLocaleString();
            document.getElementById('todayRevenue').textContent = '₹' + result.data.today_revenue.toLocaleString();
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function displayPayments() {
    const tbody = document.getElementById('paymentsTable');
    tbody.innerHTML = '';
    
    if (filteredPayments.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No payments found</td></tr>';
        updatePagination(0);
        return;
    }
    
    // Calculate pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedPayments = filteredPayments.slice(startIndex, endIndex);
    
    paginatedPayments.forEach(payment => {
        const paymentDate = payment.payment_date ? new Date(payment.payment_date).toLocaleDateString() : 'N/A';
        const row = `
            <tr>
                <td><code>${payment.transaction_id || 'N/A'}</code></td>
                <td><strong>${payment.booking_reference}</strong></td>
                <td>₹${payment.amount.toFixed(2)}</td>
                <td><span class="badge bg-info">${payment.payment_method}</span></td>
                <td><span class="badge bg-${payment.status === 'completed' ? 'success' : payment.status === 'pending' ? 'warning' : 'danger'}">${payment.status}</span></td>
                <td>${paymentDate}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="viewPayment(${payment.id})" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-success" onclick="downloadReceipt(${payment.id})" title="Download Receipt">
                        <i class="fas fa-download"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
    
    updatePagination(filteredPayments.length);
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
    const totalPages = Math.ceil(filteredPayments.length / itemsPerPage);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    displayPayments();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function displayNoData() {
    const tbody = document.getElementById('paymentsTable');
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

function filterPayments() {
    const statusFilter = document.getElementById('statusFilter').value.toLowerCase();
    const methodFilter = document.getElementById('methodFilter').value.toLowerCase();
    const searchFilter = document.getElementById('searchFilter').value.toLowerCase();
    
    filteredPayments = allPayments.filter(payment => {
        const matchesStatus = !statusFilter || payment.status.toLowerCase() === statusFilter;
        const matchesMethod = !methodFilter || payment.payment_method.toLowerCase() === methodFilter;
        const matchesSearch = !searchFilter || 
            (payment.transaction_id && payment.transaction_id.toLowerCase().includes(searchFilter)) ||
            payment.booking_reference.toLowerCase().includes(searchFilter);
        
        return matchesStatus && matchesMethod && matchesSearch;
    });
    
    currentPage = 1;
    displayPayments();
}

function clearFilters() {
    document.getElementById('statusFilter').value = '';
    document.getElementById('methodFilter').value = '';
    document.getElementById('searchFilter').value = '';
    filteredPayments = [...allPayments];
    currentPage = 1;
    displayPayments();
}

function refreshPayments() {
    loadPayments();
    loadStats();
}

function exportPayments() {
    showInfoPanel(
        'Export Payments',
        'Export functionality is coming soon! You will be able to export payment records in CSV and Excel formats.',
        'info',
        4000
    );
}

function viewPayment(id) {
    const payment = allPayments.find(p => p.id === id);
    if (payment) {
        const paymentData = {
            'Transaction ID': payment.transaction_id || 'N/A',
            'Booking Reference': payment.booking_reference,
            'Amount': '₹' + payment.amount.toFixed(2),
            'Payment Method': payment.payment_method.toUpperCase(),
            'Status': payment.status.toUpperCase(),
            'Payment Date': payment.payment_date ? new Date(payment.payment_date).toLocaleString('en-IN', {
                dateStyle: 'full',
                timeStyle: 'short'
            }) : 'N/A',
            'Payment ID': '#' + payment.id
        };
        
        const actions = [
            {
                label: 'Close',
                icon: 'fa-times',
                primary: false,
                onclick: 'closeDetailsModal()'
            },
            {
                label: 'Download Receipt',
                icon: 'fa-download',
                primary: true,
                onclick: `downloadReceipt(${id})`
            }
        ];
        
        showDetailsModal('Payment Details', paymentData, actions);
    }
}

function downloadReceipt(id) {
    closeDetailsModal();
    showInfoPanel(
        'Download Receipt',
        'Receipt download functionality is coming soon! You will be able to download payment receipts in PDF format.',
        'success',
        4000
    );
}
