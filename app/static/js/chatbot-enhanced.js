/**
 * Enhanced Chatbot UI Functions
 * Provides rich UI components for different response types
 */

// Create statistics card
function createStatisticsCard(stats) {
    const container = document.createElement('div');
    container.style.cssText = 'margin-top: 15px;';
    
    // Header
    const header = document.createElement('div');
    header.style.cssText = 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; text-align: center;';
    header.innerHTML = `
        <div style="font-size: 24px; font-weight: 700; margin-bottom: 5px;">
            <i class="fas fa-chart-bar"></i> YATRISETU STATISTICS
        </div>
        <div style="font-size: 14px; opacity: 0.9;">Real-time System Overview</div>
    `;
    container.appendChild(header);
    
    // Stats grid
    const statsGrid = document.createElement('div');
    statsGrid.style.cssText = 'display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;';
    
    const statItems = [
        { label: 'Total Buses', value: stats.total_buses, icon: 'fa-bus', color: '#667eea' },
        { label: 'Active Now', value: stats.active_buses, icon: 'fa-circle', color: '#2ecc71' },
        { label: 'AC Buses', value: stats.ac_buses, icon: 'fa-snowflake', color: '#3498db' },
        { label: 'Non-AC Buses', value: stats.non_ac_buses, icon: 'fa-bus-alt', color: '#e74c3c' },
        { label: 'Total Routes', value: stats.total_routes, icon: 'fa-route', color: '#f39c12' },
        { label: 'Total Bookings', value: stats.total_bookings, icon: 'fa-ticket-alt', color: '#9b59b6' }
    ];
    
    statItems.forEach(item => {
        const statCard = document.createElement('div');
        statCard.style.cssText = 'background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; transition: transform 0.2s;';
        statCard.onmouseenter = () => statCard.style.transform = 'translateY(-5px)';
        statCard.onmouseleave = () => statCard.style.transform = 'translateY(0)';
        
        statCard.innerHTML = `
            <div style="font-size: 32px; color: ${item.color}; margin-bottom: 8px;">
                <i class="fas ${item.icon}"></i>
            </div>
            <div style="font-size: 24px; font-weight: 700; color: var(--text-primary); margin-bottom: 5px;">
                ${item.value}
            </div>
            <div style="font-size: 12px; color: var(--text-muted); font-weight: 600; text-transform: uppercase;">
                ${item.label}
            </div>
        `;
        
        statsGrid.appendChild(statCard);
    });
    
    container.appendChild(statsGrid);
    
    return container;
}

// Create help card
function createHelpCard(helpData) {
    const container = document.createElement('div');
    container.style.cssText = 'margin-top: 15px;';
    
    // Header
    const header = document.createElement('div');
    header.style.cssText = 'background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; text-align: center;';
    header.innerHTML = `
        <div style="font-size: 24px; font-weight: 700; margin-bottom: 5px;">
            <i class="fas fa-question-circle"></i> COMMAND REFERENCE
        </div>
        <div style="font-size: 14px; opacity: 0.9;">Quick guide to all available commands</div>
    `;
    container.appendChild(header);
    
    // Help categories
    if (helpData.help_categories) {
        helpData.help_categories.forEach(category => {
            const categoryCard = document.createElement('div');
            categoryCard.style.cssText = 'background: white; border-radius: 10px; padding: 15px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);';
            
            // Category header
            const categoryHeader = document.createElement('div');
            categoryHeader.style.cssText = 'font-size: 16px; font-weight: 700; color: var(--accent-primary); margin-bottom: 12px; display: flex; align-items: center; gap: 10px;';
            categoryHeader.innerHTML = `
                <span style="font-size: 24px;">${category.icon}</span>
                <span>${category.title}</span>
            `;
            categoryCard.appendChild(categoryHeader);
            
            // Commands
            category.commands.forEach(cmd => {
                const cmdDiv = document.createElement('div');
                cmdDiv.style.cssText = 'padding: 10px; margin-bottom: 8px; background: #f8f9fa; border-radius: 8px; cursor: pointer; transition: all 0.2s;';
                cmdDiv.onmouseenter = () => {
                    cmdDiv.style.background = 'var(--accent-primary)';
                    cmdDiv.style.color = 'white';
                };
                cmdDiv.onmouseleave = () => {
                    cmdDiv.style.background = '#f8f9fa';
                    cmdDiv.style.color = 'var(--text-primary)';
                };
                cmdDiv.onclick = () => {
                    messageInput.value = cmd.cmd;
                    sendMessage();
                };
                
                cmdDiv.innerHTML = `
                    <div style="font-family: 'Courier New', monospace; font-weight: 600; margin-bottom: 4px;">
                        ${cmd.cmd}
                    </div>
                    <div style="font-size: 12px; opacity: 0.8;">
                        ${cmd.desc}
                    </div>
                `;
                
                categoryCard.appendChild(cmdDiv);
            });
            
            container.appendChild(categoryCard);
        });
    }
    
    return container;
}

// Create fare breakdown card
function createFareBreakdownCard(fareData) {
    const container = document.createElement('div');
    container.style.cssText = 'margin-top: 15px;';
    
    // Header
    const header = document.createElement('div');
    header.style.cssText = 'background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;';
    header.innerHTML = `
        <div style="font-size: 20px; font-weight: 700; margin-bottom: 5px;">
            <i class="fas fa-rupee-sign"></i> FARE BREAKDOWN
        </div>
        <div style="font-size: 14px; opacity: 0.9;">${fareData.from} → ${fareData.to}</div>
    `;
    container.appendChild(header);
    
    // Fare categories
    const categories = [
        { label: 'General', value: fareData.general, icon: 'fa-user', color: '#3498db' },
        { label: 'Student', value: fareData.student, icon: 'fa-graduation-cap', color: '#9b59b6' },
        { label: 'Senior Citizen', value: fareData.senior, icon: 'fa-user-clock', color: '#e67e22' },
        { label: 'Disabled', value: 'FREE', icon: 'fa-wheelchair', color: '#2ecc71' }
    ];
    
    const fareGrid = document.createElement('div');
    fareGrid.style.cssText = 'display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;';
    
    categories.forEach(cat => {
        const fareCard = document.createElement('div');
        fareCard.style.cssText = 'background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center;';
        
        fareCard.innerHTML = `
            <div style="font-size: 28px; color: ${cat.color}; margin-bottom: 8px;">
                <i class="fas ${cat.icon}"></i>
            </div>
            <div style="font-size: 20px; font-weight: 700; color: var(--text-primary); margin-bottom: 5px;">
                ${cat.value === 'FREE' ? cat.value : '₹' + cat.value}
            </div>
            <div style="font-size: 12px; color: var(--text-muted); font-weight: 600;">
                ${cat.label}
            </div>
        `;
        
        fareGrid.appendChild(fareCard);
    });
    
    container.appendChild(fareGrid);
    
    return container;
}

// Create algorithm indicator badge
function createAlgorithmBadge(algorithm) {
    const badge = document.createElement('div');
    badge.style.cssText = 'display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;';
    
    const icons = {
        'dijkstra': 'fa-project-diagram',
        'greedy': 'fa-bolt'
    };
    
    badge.innerHTML = `
        <i class="fas ${icons[algorithm] || 'fa-calculator'}"></i>
        ${algorithm} Algorithm
    `;
    
    return badge;
}

// Create quick action buttons
function createQuickActionButtons(actions) {
    const container = document.createElement('div');
    container.style.cssText = 'display: flex; gap: 8px; margin-top: 12px; flex-wrap: wrap;';
    
    actions.forEach(action => {
        const btn = document.createElement('button');
        btn.className = 'quick-action-btn';
        btn.innerHTML = `<i class="fas ${action.icon}"></i> ${action.label}`;
        btn.onclick = action.onClick;
        container.appendChild(btn);
    });
    
    return container;
}

// Export functions for use in main chatbot
window.chatbotEnhanced = {
    createStatisticsCard,
    createHelpCard,
    createFareBreakdownCard,
    createAlgorithmBadge,
    createQuickActionButtons
};
