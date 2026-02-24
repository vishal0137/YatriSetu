// Common Utilities for YatriSetu Admin Panel

// Show alert notification
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer') || createAlertContainer();
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 500px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        animation: slideInRight 0.3s ease-out;
    `;
    
    const iconMap = {
        'success': 'fa-check-circle',
        'danger': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    
    alertDiv.innerHTML = `
        <i class="fas ${iconMap[type] || 'fa-info-circle'}" style="margin-right: 8px;"></i>
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    alertContainer.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        alertDiv.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alertContainer';
    container.style.cssText = 'position: fixed; top: 0; right: 0; z-index: 9999; padding: 20px;';
    document.body.appendChild(container);
    return container;
}

// Logout functionality
function logout() {
    showConfirmDialog(
        'Confirm Logout',
        'Are you sure you want to logout?',
        'Logout',
        'Cancel',
        () => {
            showAlert('Logging out...', 'info');
            setTimeout(() => {
                window.location.href = '/logout';
            }, 1000);
        }
    );
}

// Settings functionality
function openSettings() {
    showAlert('Settings panel coming soon!', 'info');
}

// Search functionality
function openSearch() {
    const searchModal = document.getElementById('searchModal') || createSearchModal();
    searchModal.style.display = 'flex';
    document.getElementById('globalSearchInput')?.focus();
}

function createSearchModal() {
    const modal = document.createElement('div');
    modal.id = 'searchModal';
    modal.style.cssText = `
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 10000;
        align-items: flex-start;
        justify-content: center;
        padding-top: 100px;
        animation: fadeIn 0.2s;
    `;
    
    modal.innerHTML = `
        <div style="background: white; border-radius: 16px; width: 90%; max-width: 600px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); animation: slideDown 0.3s;">
            <div style="padding: 24px; border-bottom: 1px solid #e5e7eb;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <i class="fas fa-search" style="color: var(--text-muted);"></i>
                    <input type="text" id="globalSearchInput" placeholder="Search bookings, users, routes..." 
                           style="flex: 1; border: none; outline: none; font-size: 16px; color: var(--text-primary);"
                           onkeyup="performGlobalSearch(this.value)">
                    <button onclick="closeSearch()" style="background: none; border: none; cursor: pointer; color: var(--text-muted);">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div id="searchResults" style="padding: 20px; max-height: 400px; overflow-y: auto;">
                <p style="text-align: center; color: var(--text-muted);">Start typing to search...</p>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeSearch();
    });
    
    return modal;
}

function closeSearch() {
    const modal = document.getElementById('searchModal');
    if (modal) modal.style.display = 'none';
}

function performGlobalSearch(query) {
    const resultsDiv = document.getElementById('searchResults');
    
    if (!query || query.length < 2) {
        resultsDiv.innerHTML = '<p style="text-align: center; color: var(--text-muted);">Start typing to search...</p>';
        return;
    }
    
    resultsDiv.innerHTML = '<p style="text-align: center; color: var(--text-muted);"><i class="fas fa-spinner fa-spin"></i> Searching...</p>';
    
    // Simulate search (replace with actual API call)
    setTimeout(() => {
        resultsDiv.innerHTML = `
            <div style="margin-bottom: 20px;">
                <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 12px;">Bookings</h4>
                <div style="padding: 12px; background: var(--bg-secondary); border-radius: 8px; cursor: pointer; margin-bottom: 8px;" onclick="window.location.href='/admin/bookings'">
                    <div style="font-weight: 600;">Booking #BK001</div>
                    <div style="font-size: 13px; color: var(--text-muted);">John Doe - Route 101</div>
                </div>
            </div>
            <div>
                <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 12px;">Routes</h4>
                <div style="padding: 12px; background: var(--bg-secondary); border-radius: 8px; cursor: pointer;" onclick="window.location.href='/admin/routes'">
                    <div style="font-weight: 600;">Route 101</div>
                    <div style="font-size: 13px; color: var(--text-muted);">Delhi to Mumbai</div>
                </div>
            </div>
        `;
    }, 500);
}

// Notifications functionality
function openNotifications() {
    const notifModal = document.getElementById('notificationModal') || createNotificationModal();
    notifModal.style.display = 'block';
    loadNotifications();
}

function createNotificationModal() {
    const modal = document.createElement('div');
    modal.id = 'notificationModal';
    modal.style.cssText = `
        display: none;
        position: fixed;
        top: 60px;
        right: 20px;
        width: 400px;
        max-height: 500px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        animation: slideDown 0.3s;
        overflow: hidden;
    `;
    
    modal.innerHTML = `
        <div style="padding: 20px; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0; font-size: 18px; font-weight: 700;">Notifications</h3>
            <button onclick="closeNotifications()" style="background: none; border: none; cursor: pointer; color: var(--text-muted);">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div id="notificationList" style="max-height: 400px; overflow-y: auto;">
            <div style="padding: 20px; text-align: center; color: var(--text-muted);">
                <i class="fas fa-spinner fa-spin"></i> Loading...
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!modal.contains(e.target) && !e.target.closest('.nav-icon')) {
            closeNotifications();
        }
    });
    
    return modal;
}

function closeNotifications() {
    const modal = document.getElementById('notificationModal');
    if (modal) modal.style.display = 'none';
}

function loadNotifications() {
    const listDiv = document.getElementById('notificationList');
    
    // Simulate loading notifications (replace with actual API call)
    setTimeout(() => {
        listDiv.innerHTML = `
            <div style="padding: 16px; border-bottom: 1px solid #e5e7eb; cursor: pointer; transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='white'">
                <div style="display: flex; gap: 12px;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: rgba(59, 130, 246, 0.1); display: flex; align-items: center; justify-content: center;">
                        <i class="fas fa-ticket-alt" style="color: #3b82f6;"></i>
                    </div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; margin-bottom: 4px;">New Booking</div>
                        <div style="font-size: 13px; color: var(--text-muted);">Booking #BK123 confirmed</div>
                        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">2 minutes ago</div>
                    </div>
                </div>
            </div>
            <div style="padding: 16px; border-bottom: 1px solid #e5e7eb; cursor: pointer; transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='white'">
                <div style="display: flex; gap: 12px;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: rgba(16, 185, 129, 0.1); display: flex; align-items: center; justify-content: center;">
                        <i class="fas fa-check-circle" style="color: #10b981;"></i>
                    </div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; margin-bottom: 4px;">Payment Received</div>
                        <div style="font-size: 13px; color: var(--text-muted);">₹500 payment completed</div>
                        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">15 minutes ago</div>
                    </div>
                </div>
            </div>
            <div style="padding: 16px; text-align: center;">
                <a href="#" style="color: var(--accent-primary); font-weight: 600; text-decoration: none;">View All Notifications</a>
            </div>
        `;
    }, 500);
}

// User profile dropdown
function toggleUserDropdown() {
    const dropdown = document.getElementById('userDropdown') || createUserDropdown();
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

function createUserDropdown() {
    const dropdown = document.createElement('div');
    dropdown.id = 'userDropdown';
    dropdown.style.cssText = `
        display: none;
        position: fixed;
        top: 60px;
        right: 20px;
        width: 250px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        animation: slideDown 0.3s;
        overflow: hidden;
    `;
    
    dropdown.innerHTML = `
        <div style="padding: 20px; border-bottom: 1px solid #e5e7eb;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 48px; height: 48px; border-radius: 50%; background: var(--accent-primary); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 20px;">A</div>
                <div>
                    <div style="font-weight: 600;">Admin User</div>
                    <div style="font-size: 13px; color: var(--text-muted);">admin@yatrisetu.com</div>
                </div>
            </div>
        </div>
        <div style="padding: 8px;">
            <a href="#" onclick="openSettings(); return false;" style="display: flex; align-items: center; gap: 12px; padding: 12px; border-radius: 8px; text-decoration: none; color: var(--text-primary); transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='white'">
                <i class="fas fa-user-circle" style="width: 20px;"></i>
                <span>Profile</span>
            </a>
            <a href="#" onclick="openSettings(); return false;" style="display: flex; align-items: center; gap: 12px; padding: 12px; border-radius: 8px; text-decoration: none; color: var(--text-primary); transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='white'">
                <i class="fas fa-cog" style="width: 20px;"></i>
                <span>Settings</span>
            </a>
            <a href="#" onclick="logout(); return false;" style="display: flex; align-items: center; gap: 12px; padding: 12px; border-radius: 8px; text-decoration: none; color: #ef4444; transition: background 0.2s;" onmouseover="this.style.background='#fef2f2'" onmouseout="this.style.background='white'">
                <i class="fas fa-sign-out-alt" style="width: 20px;"></i>
                <span>Logout</span>
            </a>
        </div>
    `;
    
    document.body.appendChild(dropdown);
    
    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target) && !e.target.closest('.user-profile')) {
            dropdown.style.display = 'none';
        }
    });
    
    return dropdown;
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(style);


// Professional Confirm Dialog
function showConfirmDialog(title, message, confirmText, cancelText, onConfirm, onCancel) {
    const dialog = document.createElement('div');
    dialog.id = 'confirmDialog';
    dialog.style.cssText = `
        display: flex;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 10001;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.2s;
    `;
    
    dialog.innerHTML = `
        <div style="background: white; border-radius: 16px; width: 90%; max-width: 450px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); animation: slideDown 0.3s; overflow: hidden;">
            <div style="padding: 24px; border-bottom: 1px solid #e5e7eb;">
                <h3 style="margin: 0; font-size: 20px; font-weight: 700; color: var(--text-primary); display: flex; align-items: center; gap: 12px;">
                    <i class="fas fa-exclamation-circle" style="color: var(--accent-primary);"></i>
                    ${title}
                </h3>
            </div>
            <div style="padding: 24px;">
                <p style="margin: 0; color: var(--text-secondary); font-size: 15px; line-height: 1.6;">${message}</p>
            </div>
            <div style="padding: 20px 24px; background: #f9fafb; display: flex; gap: 12px; justify-content: flex-end;">
                <button id="cancelBtn" style="padding: 10px 24px; border: 2px solid var(--border-color); background: white; color: var(--text-primary); border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s;">
                    ${cancelText}
                </button>
                <button id="confirmBtn" style="padding: 10px 24px; border: none; background: var(--accent-primary); color: white; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 12px rgba(255, 107, 74, 0.3);">
                    ${confirmText}
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(dialog);
    
    const confirmBtn = dialog.querySelector('#confirmBtn');
    const cancelBtn = dialog.querySelector('#cancelBtn');
    
    confirmBtn.addEventListener('mouseover', () => {
        confirmBtn.style.transform = 'translateY(-2px)';
        confirmBtn.style.boxShadow = '0 6px 16px rgba(255, 107, 74, 0.4)';
    });
    
    confirmBtn.addEventListener('mouseout', () => {
        confirmBtn.style.transform = 'translateY(0)';
        confirmBtn.style.boxShadow = '0 4px 12px rgba(255, 107, 74, 0.3)';
    });
    
    cancelBtn.addEventListener('mouseover', () => {
        cancelBtn.style.borderColor = 'var(--accent-primary)';
        cancelBtn.style.color = 'var(--accent-primary)';
    });
    
    cancelBtn.addEventListener('mouseout', () => {
        cancelBtn.style.borderColor = 'var(--border-color)';
        cancelBtn.style.color = 'var(--text-primary)';
    });
    
    confirmBtn.onclick = () => {
        dialog.remove();
        if (onConfirm) onConfirm();
    };
    
    cancelBtn.onclick = () => {
        dialog.remove();
        if (onCancel) onCancel();
    };
    
    dialog.addEventListener('click', (e) => {
        if (e.target === dialog) {
            dialog.remove();
            if (onCancel) onCancel();
        }
    });
}

// Professional Details Modal
function showDetailsModal(title, data, actions = []) {
    const modal = document.createElement('div');
    modal.id = 'detailsModal';
    modal.style.cssText = `
        display: flex;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 10001;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.2s;
        padding: 20px;
    `;
    
    // Build data rows
    let dataRows = '';
    for (const [key, value] of Object.entries(data)) {
        const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        const displayValue = value || 'N/A';
        
        dataRows += `
            <div style="display: flex; padding: 16px; border-bottom: 1px solid #e5e7eb; transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='white'">
                <div style="flex: 0 0 180px; font-weight: 600; color: var(--text-muted); font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">
                    ${label}
                </div>
                <div style="flex: 1; color: var(--text-primary); font-weight: 500; font-size: 15px;">
                    ${displayValue}
                </div>
            </div>
        `;
    }
    
    // Build action buttons
    let actionButtons = '';
    if (actions.length > 0) {
        actionButtons = '<div style="padding: 20px 24px; background: #f9fafb; display: flex; gap: 12px; justify-content: flex-end; border-top: 1px solid #e5e7eb;">';
        actions.forEach(action => {
            const btnStyle = action.primary 
                ? 'background: var(--accent-primary); color: white; border: none; box-shadow: 0 4px 12px rgba(255, 107, 74, 0.3);'
                : 'background: white; color: var(--text-primary); border: 2px solid var(--border-color);';
            
            actionButtons += `
                <button onclick="${action.onclick}" style="padding: 10px 24px; ${btnStyle} border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s;">
                    <i class="fas ${action.icon}"></i> ${action.label}
                </button>
            `;
        });
        actionButtons += '</div>';
    }
    
    modal.innerHTML = `
        <div style="background: white; border-radius: 16px; width: 100%; max-width: 700px; max-height: 90vh; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); animation: slideDown 0.3s; overflow: hidden; display: flex; flex-direction: column;">
            <div style="padding: 24px; border-bottom: 1px solid #e5e7eb; background: linear-gradient(135deg, var(--accent-primary), #ff8a65); color: white;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; font-size: 22px; font-weight: 700; display: flex; align-items: center; gap: 12px;">
                        <i class="fas fa-info-circle"></i>
                        ${title}
                    </h3>
                    <button onclick="closeDetailsModal()" style="background: rgba(255, 255, 255, 0.2); border: none; color: white; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; transition: all 0.3s; display: flex; align-items: center; justify-content: center;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div style="flex: 1; overflow-y: auto;">
                ${dataRows}
            </div>
            ${actionButtons}
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeDetailsModal();
    });
    
    // Close on ESC key
    document.addEventListener('keydown', function escHandler(e) {
        if (e.key === 'Escape') {
            closeDetailsModal();
            document.removeEventListener('keydown', escHandler);
        }
    });
}

function closeDetailsModal() {
    const modal = document.getElementById('detailsModal');
    if (modal) modal.remove();
}

// Professional Info Panel (for notifications/warnings)
function showInfoPanel(title, message, type = 'info', duration = 5000) {
    const panel = document.createElement('div');
    panel.className = 'info-panel';
    
    const icons = {
        'info': 'fa-info-circle',
        'success': 'fa-check-circle',
        'warning': 'fa-exclamation-triangle',
        'error': 'fa-times-circle'
    };
    
    const colors = {
        'info': '#3b82f6',
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444'
    };
    
    const bgColors = {
        'info': 'rgba(59, 130, 246, 0.1)',
        'success': 'rgba(16, 185, 129, 0.1)',
        'warning': 'rgba(245, 158, 11, 0.1)',
        'error': 'rgba(239, 68, 68, 0.1)'
    };
    
    panel.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        width: 400px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        animation: slideInRight 0.3s ease-out;
        border-left: 4px solid ${colors[type]};
        overflow: hidden;
    `;
    
    panel.innerHTML = `
        <div style="padding: 20px; display: flex; gap: 16px;">
            <div style="width: 48px; height: 48px; border-radius: 50%; background: ${bgColors[type]}; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <i class="fas ${icons[type]}" style="color: ${colors[type]}; font-size: 24px;"></i>
            </div>
            <div style="flex: 1;">
                <h4 style="margin: 0 0 8px 0; font-size: 16px; font-weight: 700; color: var(--text-primary);">${title}</h4>
                <p style="margin: 0; color: var(--text-secondary); font-size: 14px; line-height: 1.5;">${message}</p>
            </div>
            <button onclick="this.closest('.info-panel').remove()" style="background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 0; width: 24px; height: 24px; flex-shrink: 0;">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div style="height: 4px; background: #e5e7eb;">
            <div style="height: 100%; background: ${colors[type]}; width: 100%; animation: shrink ${duration}ms linear;"></div>
        </div>
    `;
    
    document.body.appendChild(panel);
    
    if (duration > 0) {
        setTimeout(() => {
            panel.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => panel.remove(), 300);
        }, duration);
    }
}

// Add shrink animation for progress bar
const shrinkStyle = document.createElement('style');
shrinkStyle.textContent += `
    @keyframes shrink {
        from { width: 100%; }
        to { width: 0%; }
    }
`;
document.head.appendChild(shrinkStyle);
