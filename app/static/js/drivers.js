// Drivers & Staff Management JavaScript

let allDrivers = [];
let allConductors = [];
let currentTab = 'drivers';
let currentFilter = { status: 'all', shift: null };

document.addEventListener('DOMContentLoaded', function() {
    console.log('Drivers page initialized');
    loadStaffData();
    loadStats();
});

async function loadStaffData() {
    try {
        const response = await fetch('/admin/api/staff');
        const result = await response.json();
        
        if (result.success) {
            allDrivers = result.drivers || [];
            allConductors = result.conductors || [];
            console.log(`Loaded ${allDrivers.length} drivers and ${allConductors.length} conductors`);
            displayCurrentTab();
        } else {
            showAlert('Failed to load staff data: ' + result.error, 'danger');
            displayEmptyState();
        }
    } catch (error) {
        console.error('Error loading staff:', error);
        showAlert('Database connection error', 'danger');
        displayEmptyState();
    }
}

async function loadStats() {
    try {
        const response = await fetch('/admin/api/staff/stats');
        const result = await response.json();
        
        if (result.success) {
            const data = result.data;
            document.getElementById('totalDrivers').textContent = data.total_drivers || 0;
            document.getElementById('totalConductors').textContent = data.total_conductors || 0;
            document.getElementById('activeStaff').textContent = data.active_staff || 0;
            document.getElementById('onLeave').textContent = (data.on_leave_drivers + data.on_leave_conductors) || 0;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function switchTab(tab) {
    currentTab = tab;
    
    // Update tab buttons
    document.querySelectorAll('.staff-tab').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.staff-tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById(tab + 'Tab').classList.add('active');
    
    // Reset filters
    currentFilter = { status: 'all', shift: null };
    resetFilterButtons();
    
    displayCurrentTab();
}

function displayCurrentTab() {
    switch(currentTab) {
        case 'drivers':
            displayStaff(allDrivers, 'driversContainer', 'driver');
            break;
        case 'conductors':
            displayStaff(allConductors, 'conductorsContainer', 'conductor');
            break;
        case 'all':
            const allStaff = [...allDrivers, ...allConductors];
            displayStaff(allStaff, 'allStaffContainer', 'mixed');
            break;
    }
}

function displayStaff(staffList, containerId, type) {
    const container = document.getElementById(containerId);
    
    // Apply filters
    let filteredStaff = staffList.filter(staff => {
        const matchStatus = currentFilter.status === 'all' || staff.status === currentFilter.status;
        const matchShift = !currentFilter.shift || staff.shift === currentFilter.shift;
        return matchStatus && matchShift;
    });
    
    if (filteredStaff.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="empty-state">
                    <div class="icon"><i class="fas fa-users"></i></div>
                    <h3>No Staff Found</h3>
                    <p>No staff members match the current filters</p>
                </div>
            </div>
        `;
        return;
    }
    
    container.innerHTML = '';
    
    filteredStaff.forEach(staff => {
        const card = createStaffCard(staff, type);
        container.innerHTML += card;
    });
}

function createStaffCard(staff, type) {
    const isDriver = type === 'driver' || staff.driver_id;
    const staffId = isDriver ? staff.driver_id : staff.conductor_id;
    const initials = staff.full_name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
    
    // Status badge
    const statusClass = {
        'Active': 'status-active',
        'On Leave': 'status-leave',
        'Inactive': 'status-inactive'
    }[staff.status] || 'status-inactive';
    
    // Shift badge
    const shiftClass = {
        'Morning': 'shift-morning',
        'Evening': 'shift-evening',
        'Night': 'shift-night'
    }[staff.shift] || 'shift-morning';
    
    // Assignment info
    const busInfo = staff.assigned_bus_number || 'Not Assigned';
    const routeInfo = staff.assigned_route_number 
        ? `${staff.assigned_route_number}${staff.assigned_route_name ? ' - ' + staff.assigned_route_name : ''}`
        : 'Not Assigned';
    
    return `
        <div class="col-4">
            <div class="staff-card">
                <div class="staff-header">
                    <div class="staff-avatar">${initials}</div>
                    <div class="staff-info">
                        <h3>${staff.full_name}</h3>
                        <div class="staff-id">${staffId}</div>
                    </div>
                </div>
                
                <div class="staff-details">
                    <div class="detail-item">
                        <div class="detail-label">Phone</div>
                        <div class="detail-value">
                            <i class="fas fa-phone" style="color: var(--text-muted); font-size: 12px;"></i>
                            ${staff.phone || 'N/A'}
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Experience</div>
                        <div class="detail-value">
                            <i class="fas fa-calendar" style="color: var(--text-muted); font-size: 12px;"></i>
                            ${staff.experience_years || 0} years
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Shift</div>
                        <div class="detail-value">
                            <span class="shift-badge ${shiftClass}">${staff.shift || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Status</div>
                        <div class="detail-value">
                            <span class="status-indicator ${statusClass}">${staff.status || 'Inactive'}</span>
                        </div>
                    </div>
                </div>
                
                ${staff.assigned_bus_id || staff.assigned_route_id ? `
                <div class="staff-assignment">
                    <div class="assignment-title">Current Assignment</div>
                    <div class="assignment-info">
                        <div class="assignment-row">
                            <span class="label">Bus:</span>
                            <span class="value">${busInfo}</span>
                        </div>
                        <div class="assignment-row">
                            <span class="label">Route:</span>
                            <span class="value">${routeInfo}</span>
                        </div>
                    </div>
                </div>
                ` : ''}
                
                <div class="staff-actions">
                    <button class="action-btn action-btn-primary" onclick="viewStaffDetails(${staff.id}, '${isDriver ? 'driver' : 'conductor'}')">
                        <i class="fas fa-eye"></i> View Details
                    </button>
                    <button class="action-btn action-btn-secondary" onclick="editStaff(${staff.id}, '${isDriver ? 'driver' : 'conductor'}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                </div>
            </div>
        </div>
    `;
}

function displayEmptyState() {
    const containers = ['driversContainer', 'conductorsContainer', 'allStaffContainer'];
    containers.forEach(id => {
        const container = document.getElementById(id);
        if (container) {
            container.innerHTML = `
                <div class="col-12">
                    <div class="empty-state">
                        <div class="icon"><i class="fas fa-database"></i></div>
                        <h3>No Data Available</h3>
                        <p>Unable to load staff data. Please check database connection.</p>
                    </div>
                </div>
            `;
        }
    });
}

function filterByStatus(status) {
    currentFilter.status = status;
    
    // Update filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.textContent.includes('All Staff') || 
            btn.textContent.includes(status)) {
            btn.classList.add('active');
        } else if (btn.textContent.includes('Active') || 
                   btn.textContent.includes('On Leave') || 
                   btn.textContent.includes('Inactive')) {
            btn.classList.remove('active');
        }
    });
    
    displayCurrentTab();
}

function filterByShift(shift) {
    currentFilter.shift = currentFilter.shift === shift ? null : shift;
    
    // Update shift filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.textContent.includes(shift)) {
            btn.classList.toggle('active');
        }
    });
    
    displayCurrentTab();
}

function resetFilterButtons() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.textContent.includes('All Staff')) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

function refreshData() {
    showInfoPanel('Refreshing Data', 'Loading latest staff information...', 'info', 2000);
    loadStaffData();
    loadStats();
}

function addStaff() {
    showInfoPanel(
        'Add New Staff',
        'Staff creation form is coming soon! You will be able to add new drivers and conductors with assignments.',
        'info',
        4000
    );
}

function viewStaffDetails(id, type) {
    const staff = type === 'driver' 
        ? allDrivers.find(d => d.id === id)
        : allConductors.find(c => c.id === id);
    
    if (staff) {
        const isDriver = type === 'driver';
        const staffData = {
            'Full Name': staff.full_name,
            'Staff ID': isDriver ? staff.driver_id : staff.conductor_id,
            'Phone': staff.phone || 'Not provided',
            'Email': staff.email || 'Not provided',
            'Experience': (staff.experience_years || 0) + ' years',
            'Shift': staff.shift || 'Not assigned',
            'Status': staff.status || 'Inactive',
            'Assigned Bus': staff.assigned_bus_number || 'Not assigned',
            'Assigned Route': staff.assigned_route_number 
                ? `${staff.assigned_route_number}${staff.assigned_route_name ? ' - ' + staff.assigned_route_name : ''}`
                : 'Not assigned'
        };
        
        if (isDriver) {
            staffData['License Number'] = staff.license_number || 'N/A';
        } else {
            staffData['Employee ID'] = staff.employee_id || 'N/A';
            staffData['Role'] = staff.role || 'Conductor';
        }
        
        const actions = [
            {
                label: 'Close',
                icon: 'fa-times',
                primary: false,
                onclick: 'closeDetailsModal()'
            },
            {
                label: 'Edit Staff',
                icon: 'fa-edit',
                primary: true,
                onclick: `editStaff(${id}, '${type}')`
            }
        ];
        
        showDetailsModal(
            `${isDriver ? 'Driver' : 'Conductor'} Details`,
            staffData,
            actions
        );
    }
}

function editStaff(id, type) {
    closeDetailsModal();
    showInfoPanel(
        'Edit Staff',
        'Staff editing form is coming soon! You will be able to update staff information and assignments.',
        'info',
        4000
    );
}
