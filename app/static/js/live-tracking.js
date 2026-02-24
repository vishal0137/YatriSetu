// Live Bus Tracking JavaScript

let activeBuses = [];
let selectedBus = null;
let autoRefreshInterval = null;
let isAutoRefresh = false;
let currentZoom = 1;

// Demo route stations (in real app, this would come from API)
const demoStations = [
    { id: 1, name: 'Central Station', x: 100, y: 300 },
    { id: 2, name: 'Market Square', x: 250, y: 200 },
    { id: 3, name: 'City Hospital', x: 400, y: 250 },
    { id: 4, name: 'University', x: 550, y: 150 },
    { id: 5, name: 'Tech Park', x: 700, y: 200 },
    { id: 6, name: 'Airport', x: 850, y: 300 }
];

// Demo buses with animated positions
const demoBuses = [
    {
        id: 1,
        bus_number: 'DL-1234',
        route_number: '101',
        route_name: 'Central - Airport',
        status: 'moving',
        current_station: 'Market Square',
        next_station: 'City Hospital',
        progress: 0,
        speed: 0.5,
        passengers: 45,
        capacity: 60
    },
    {
        id: 2,
        bus_number: 'DL-5678',
        route_number: '102',
        route_name: 'Central - Tech Park',
        status: 'moving',
        current_station: 'University',
        next_station: 'Tech Park',
        progress: 0,
        speed: 0.7,
        passengers: 32,
        capacity: 50
    },
    {
        id: 3,
        bus_number: 'DL-9012',
        route_number: '103',
        route_name: 'Airport Express',
        status: 'stopped',
        current_station: 'Central Station',
        next_station: 'Market Square',
        progress: 0,
        speed: 0.6,
        passengers: 58,
        capacity: 60
    }
];

document.addEventListener('DOMContentLoaded', function() {
    console.log('Live tracking initialized');
    loadActiveBuses();
    startAnimation();
});

function loadActiveBuses() {
    // In real app, this would fetch from API
    // For demo, we use the demo data
    activeBuses = [...demoBuses];
    displayBusList();
}

function displayBusList() {
    const busList = document.getElementById('busList');
    const countElement = document.getElementById('activeBusCount');
    
    countElement.textContent = activeBuses.length;
    
    if (activeBuses.length === 0) {
        busList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-bus"></i>
                <h3>No Active Buses</h3>
                <p>No buses are currently active</p>
            </div>
        `;
        return;
    }
    
    busList.innerHTML = '';
    
    activeBuses.forEach(bus => {
        const busItem = document.createElement('div');
        busItem.className = 'bus-item';
        if (selectedBus && selectedBus.id === bus.id) {
            busItem.classList.add('active');
        }
        
        busItem.innerHTML = `
            <div class="bus-number">${bus.bus_number}</div>
            <div class="bus-route">Route ${bus.route_number}: ${bus.route_name}</div>
            <div class="bus-status">
                <span class="status-dot ${bus.status}"></span>
                <span>${bus.status === 'moving' ? 'Moving' : 'Stopped'} • ${bus.current_station}</span>
            </div>
        `;
        
        busItem.onclick = () => selectBus(bus);
        busList.appendChild(busItem);
    });
}

function selectBus(bus) {
    selectedBus = bus;
    displayBusList();
    drawRoute();
    
    // Update route info
    document.getElementById('routeTitle').textContent = `Route ${bus.route_number}: ${bus.route_name}`;
    document.getElementById('routeSubtitle').textContent = `Bus ${bus.bus_number} • ${bus.status === 'moving' ? 'Moving' : 'Stopped at'} ${bus.current_station}`;
}

function drawRoute() {
    const svg = document.getElementById('routeVisualization');
    
    // Clear previous content (except defs)
    while (svg.childNodes.length > 1) {
        svg.removeChild(svg.lastChild);
    }
    
    if (!selectedBus) {
        // Show empty state
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', '500');
        text.setAttribute('y', '300');
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('fill', '#9ca3af');
        text.setAttribute('font-size', '18');
        text.setAttribute('font-weight', '600');
        text.textContent = 'Select a bus to view its route';
        svg.appendChild(text);
        return;
    }
    
    // Draw route path
    const pathData = demoStations.map((station, index) => {
        return `${index === 0 ? 'M' : 'L'} ${station.x} ${station.y}`;
    }).join(' ');
    
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', pathData);
    path.setAttribute('stroke', '#FF6B4A');
    path.setAttribute('stroke-width', '4');
    path.setAttribute('fill', 'none');
    path.setAttribute('marker-end', 'url(#arrowhead)');
    svg.appendChild(path);
    
    // Draw stations
    demoStations.forEach((station, index) => {
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.setAttribute('class', 'station');
        group.setAttribute('data-station-id', station.id);
        
        // Station circle
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('class', 'station-circle');
        circle.setAttribute('cx', station.x);
        circle.setAttribute('cy', station.y);
        circle.setAttribute('r', '10');
        
        // Highlight current station
        if (station.name === selectedBus.current_station) {
            circle.setAttribute('fill', '#10b981');
            circle.setAttribute('r', '12');
        } else {
            circle.setAttribute('fill', '#6b7280');
        }
        
        circle.setAttribute('stroke', 'white');
        circle.setAttribute('stroke-width', '3');
        
        // Station label
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', station.x);
        text.setAttribute('y', station.y - 20);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('fill', '#1f2937');
        text.setAttribute('font-size', '12');
        text.setAttribute('font-weight', '600');
        text.textContent = station.name;
        
        group.appendChild(circle);
        group.appendChild(text);
        
        group.onclick = () => showStationInfo(station);
        
        svg.appendChild(group);
    });
    
    // Draw bus icon
    drawBus();
}

function drawBus() {
    if (!selectedBus) return;
    
    const svg = document.getElementById('routeVisualization');
    
    // Find current and next station positions
    const currentStationIndex = demoStations.findIndex(s => s.name === selectedBus.current_station);
    const nextStationIndex = demoStations.findIndex(s => s.name === selectedBus.next_station);
    
    if (currentStationIndex === -1 || nextStationIndex === -1) return;
    
    const currentStation = demoStations[currentStationIndex];
    const nextStation = demoStations[nextStationIndex];
    
    // Calculate bus position based on progress
    const busX = currentStation.x + (nextStation.x - currentStation.x) * selectedBus.progress;
    const busY = currentStation.y + (nextStation.y - currentStation.y) * selectedBus.progress;
    
    // Remove old bus icon
    const oldBus = svg.querySelector('.bus-icon');
    if (oldBus) oldBus.remove();
    
    // Create bus group
    const busGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    busGroup.setAttribute('class', 'bus-icon');
    busGroup.setAttribute('transform', `translate(${busX}, ${busY})`);
    
    // Bus body (rectangle)
    const busBody = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    busBody.setAttribute('x', '-20');
    busBody.setAttribute('y', '-12');
    busBody.setAttribute('width', '40');
    busBody.setAttribute('height', '24');
    busBody.setAttribute('rx', '4');
    busBody.setAttribute('fill', '#FF6B4A');
    busBody.setAttribute('stroke', 'white');
    busBody.setAttribute('stroke-width', '2');
    
    // Bus windows
    const window1 = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    window1.setAttribute('x', '-15');
    window1.setAttribute('y', '-8');
    window1.setAttribute('width', '10');
    window1.setAttribute('height', '8');
    window1.setAttribute('rx', '2');
    window1.setAttribute('fill', 'white');
    window1.setAttribute('opacity', '0.8');
    
    const window2 = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    window2.setAttribute('x', '5');
    window2.setAttribute('y', '-8');
    window2.setAttribute('width', '10');
    window2.setAttribute('height', '8');
    window2.setAttribute('rx', '2');
    window2.setAttribute('fill', 'white');
    window2.setAttribute('opacity', '0.8');
    
    // Bus number label
    const busLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    busLabel.setAttribute('x', '0');
    busLabel.setAttribute('y', '25');
    busLabel.setAttribute('text-anchor', 'middle');
    busLabel.setAttribute('fill', '#1f2937');
    busLabel.setAttribute('font-size', '11');
    busLabel.setAttribute('font-weight', '700');
    busLabel.textContent = selectedBus.bus_number;
    
    busGroup.appendChild(busBody);
    busGroup.appendChild(window1);
    busGroup.appendChild(window2);
    busGroup.appendChild(busLabel);
    
    busGroup.onclick = () => showBusInfo(selectedBus);
    
    svg.appendChild(busGroup);
}

function startAnimation() {
    setInterval(() => {
        if (!selectedBus) return;
        
        // Update bus progress
        selectedBus.progress += selectedBus.speed / 100;
        
        // If reached next station
        if (selectedBus.progress >= 1) {
            selectedBus.progress = 0;
            
            // Move to next station
            const currentIndex = demoStations.findIndex(s => s.name === selectedBus.current_station);
            const nextIndex = demoStations.findIndex(s => s.name === selectedBus.next_station);
            
            if (nextIndex !== -1) {
                selectedBus.current_station = selectedBus.next_station;
                
                // Set new next station (loop back if at end)
                const newNextIndex = (nextIndex + 1) % demoStations.length;
                selectedBus.next_station = demoStations[newNextIndex].name;
            }
            
            // Update bus list
            displayBusList();
        }
        
        // Redraw bus
        drawBus();
    }, 50); // Update every 50ms for smooth animation
}

function showBusInfo(bus) {
    // Remove existing info panel
    const existingPanel = document.querySelector('.info-panel');
    if (existingPanel) existingPanel.remove();
    
    const panel = document.createElement('div');
    panel.className = 'info-panel';
    panel.innerHTML = `
        <div class="info-panel-header">
            <h4><i class="fas fa-bus"></i> ${bus.bus_number}</h4>
            <button class="close-info" onclick="this.closest('.info-panel').remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="info-row">
            <span class="info-label">Route:</span>
            <span class="info-value">${bus.route_number}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Status:</span>
            <span class="info-value">${bus.status === 'moving' ? 'Moving' : 'Stopped'}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Current:</span>
            <span class="info-value">${bus.current_station}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Next:</span>
            <span class="info-value">${bus.next_station}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Passengers:</span>
            <span class="info-value">${bus.passengers}/${bus.capacity}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Occupancy:</span>
            <span class="info-value">${Math.round((bus.passengers / bus.capacity) * 100)}%</span>
        </div>
    `;
    
    document.querySelector('.route-canvas').appendChild(panel);
}

function showStationInfo(station) {
    showInfoPanel(
        station.name,
        `Station information and upcoming buses will be displayed here.`,
        'info',
        3000
    );
}

function refreshTracking() {
    showInfoPanel('Refreshing', 'Loading latest bus locations...', 'info', 2000);
    loadActiveBuses();
    if (selectedBus) {
        drawRoute();
    }
}

function toggleAutoRefresh() {
    isAutoRefresh = !isAutoRefresh;
    const btn = document.querySelector('.btn-primary-modern');
    const text = document.getElementById('autoRefreshText');
    
    if (isAutoRefresh) {
        btn.innerHTML = '<i class="fas fa-pause"></i> <span id="autoRefreshText">Stop Auto Refresh</span>';
        autoRefreshInterval = setInterval(refreshTracking, 10000); // Refresh every 10 seconds
        showInfoPanel('Auto Refresh', 'Auto refresh enabled - updating every 10 seconds', 'success', 3000);
    } else {
        btn.innerHTML = '<i class="fas fa-play"></i> <span id="autoRefreshText">Auto Refresh</span>';
        if (autoRefreshInterval) {
            clearInterval(autoRefreshInterval);
            autoRefreshInterval = null;
        }
        showInfoPanel('Auto Refresh', 'Auto refresh disabled', 'info', 2000);
    }
}

function zoomIn() {
    currentZoom = Math.min(currentZoom + 0.2, 2);
    applyZoom();
}

function zoomOut() {
    currentZoom = Math.max(currentZoom - 0.2, 0.5);
    applyZoom();
}

function resetView() {
    currentZoom = 1;
    applyZoom();
}

function applyZoom() {
    const svg = document.getElementById('routeVisualization');
    const centerX = 500;
    const centerY = 300;
    svg.setAttribute('viewBox', `${centerX - (500 / currentZoom)} ${centerY - (300 / currentZoom)} ${1000 / currentZoom} ${600 / currentZoom}`);
}
