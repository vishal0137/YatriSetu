/**
 * Enhanced Data Import JavaScript
 * Handles file upload, preview, editing, and database import with duplicate detection
 */

let uploadedFile = null;
let uploadedFilePath = null;
let selectedCategory = null;
let previewData = [];
let currentFilter = 'all';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupFileUpload();
    setupImportConfirmation();
});

function setupFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#0d6efd';
        uploadArea.style.background = '#f8f9fa';
    });
    
    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#dee2e6';
        uploadArea.style.background = '';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#dee2e6';
        uploadArea.style.background = '';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect({ target: fileInput });
        }
    });
    
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showAlert('error', 'File size exceeds 10MB limit');
        return;
    }
    
    // Validate file type
    const validTypes = ['.csv', '.pdf'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    if (!validTypes.includes(fileExt)) {
        showAlert('error', 'Invalid file type. Only CSV and PDF files are allowed');
        return;
    }
    
    uploadedFile = file;
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileInfo').style.display = 'block';
}

function clearFile() {
    uploadedFile = null;
    uploadedFilePath = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('previewSection').style.display = 'none';
    document.getElementById('importSection').style.display = 'none';
}

async function analyzeAndPreview() {
    if (!uploadedFile) {
        showAlert('error', 'Please select a file first');
        return;
    }
    
    selectedCategory = document.getElementById('categorySelect').value;
    
    // Show loading
    showLoading('Analyzing file and checking for duplicates...');
    
    try {
        // Upload file first
        const formData = new FormData();
        formData.append('file', uploadedFile);
        
        const uploadResponse = await fetch('/admin/api/data-import/analyze', {
            method: 'POST',
            body: formData
        });
        
        const uploadResult = await uploadResponse.json();
        
        if (!uploadResult.success) {
            throw new Error(uploadResult.error);
        }
        
        uploadedFilePath = uploadResult.analysis.filepath;
        
        // Auto-detect category if not selected
        if (!selectedCategory || selectedCategory === '') {
            selectedCategory = uploadResult.analysis.detected_category;
            console.log('Auto-detected category:', selectedCategory);
        }
        
        // Validate category before proceeding
        if (!selectedCategory || selectedCategory === '') {
            hideLoading();
            showAlert('error', 'Could not detect data category. Please select one manually.');
            return;
        }
        
        console.log('Sending preview request with:', {
            filepath: uploadedFilePath,
            category: selectedCategory
        });
        
        // Get preview with duplicate checking
        const previewResponse = await fetch('/admin/api/data-import/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: uploadedFilePath,
                category: selectedCategory
            })
        });
        
        const previewResult = await previewResponse.json();
        
        if (!previewResult.success) {
            throw new Error(previewResult.error);
        }
        
        // Store preview data
        previewData = previewResult.preview;
        
        // Display preview
        displayPreview(previewResult);
        
        // Update steps
        updateStep(2);
        
        hideLoading();
        
    } catch (error) {
        hideLoading();
        showAlert('error', 'Error: ' + error.message);
        console.error('Preview error:', error);
    }
}

function displayPreview(result) {
    // Update statistics
    document.getElementById('totalRecords').textContent = result.total_records;
    document.getElementById('totalRecordsBadge').textContent = result.total_records + ' records';
    document.getElementById('duplicatesBadge').textContent = result.duplicates.total_duplicates + ' duplicates';
    document.getElementById('errorsBadge').textContent = result.validation.total_errors + ' errors';
    
    const insertCount = result.preview.filter(r => r.action === 'insert').length;
    const duplicateCount = result.preview.filter(r => r.is_duplicate).length;
    
    document.getElementById('toInsert').textContent = insertCount;
    document.getElementById('duplicateCount').textContent = duplicateCount;
    document.getElementById('errorCount').textContent = result.validation.total_errors;
    
    // Build table
    buildPreviewTable(result.preview);
    
    // Show preview section
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('previewSection').style.display = 'block';
}

function buildPreviewTable(data) {
    if (data.length === 0) return;
    
    const table = document.getElementById('previewTable');
    const thead = document.getElementById('previewTableHeader');
    const tbody = document.getElementById('previewTableBody');
    
    // Clear existing content
    tbody.innerHTML = '';
    
    // Get column names from first record
    const columns = Object.keys(data[0].data);
    
    // Build header (only once)
    if (thead.children.length === 3) {
        columns.forEach(col => {
            const th = document.createElement('th');
            th.textContent = col.replace(/_/g, ' ').toUpperCase();
            thead.appendChild(th);
        });
        // Add duplicate info column
        const thDup = document.createElement('th');
        thDup.textContent = 'DUPLICATE INFO';
        thDup.style.width = '200px';
        thead.appendChild(thDup);
    }
    
    // Build rows
    data.forEach((record, index) => {
        const tr = document.createElement('tr');
        tr.dataset.recordId = record.id;
        
        // Add row class based on status
        if (record.is_duplicate) {
            tr.classList.add('row-duplicate');
        } else if (record.action === 'insert') {
            tr.classList.add('row-insert');
        }
        
        // Row number
        const tdNum = document.createElement('td');
        tdNum.textContent = index + 1;
        tr.appendChild(tdNum);
        
        // Action dropdown
        const tdAction = document.createElement('td');
        const actionSelect = document.createElement('select');
        actionSelect.className = 'form-select form-select-sm';
        actionSelect.innerHTML = `
            <option value="insert" ${record.action === 'insert' ? 'selected' : ''}>Insert</option>
            <option value="update" ${record.action === 'update' ? 'selected' : ''}>Update</option>
            <option value="skip" ${record.action === 'skip' ? 'selected' : ''}>Skip</option>
        `;
        actionSelect.onchange = (e) => updateRecordAction(record.id, e.target.value);
        tdAction.appendChild(actionSelect);
        tr.appendChild(tdAction);
        
        // Status badge with tooltip
        const tdStatus = document.createElement('td');
        if (record.is_duplicate) {
            const badge = document.createElement('span');
            badge.className = 'badge bg-warning';
            badge.textContent = 'Duplicate';
            badge.style.cursor = 'pointer';
            badge.title = 'Click to view details';
            badge.onclick = () => showDuplicateDetails(record);
            tdStatus.appendChild(badge);
        } else {
            tdStatus.innerHTML = '<span class="badge bg-success">New</span>';
        }
        tr.appendChild(tdStatus);
        
        // Data columns (editable)
        columns.forEach(col => {
            const td = document.createElement('td');
            td.className = 'editable-cell';
            
            // Highlight changed fields for duplicates
            if (record.is_duplicate && record.duplicate_info && record.duplicate_info.differences) {
                const diff = record.duplicate_info.differences.find(d => d.field === col);
                if (diff && diff.changed) {
                    td.style.backgroundColor = '#fff3cd';
                    td.style.fontWeight = 'bold';
                    td.title = `Existing: ${diff.existing_value}\nNew: ${diff.new_value}`;
                }
            }
            
            td.textContent = record.data[col] || '-';
            td.dataset.column = col;
            td.onclick = () => editCell(td, record.id, col);
            tr.appendChild(td);
        });
        
        // Duplicate info column
        const tdDupInfo = document.createElement('td');
        if (record.is_duplicate && record.duplicate_info) {
            const btn = document.createElement('button');
            btn.className = 'btn btn-sm btn-outline-warning';
            btn.innerHTML = '<i class="fas fa-info-circle"></i> View Details';
            btn.onclick = () => showDuplicateDetails(record);
            tdDupInfo.appendChild(btn);
        } else {
            tdDupInfo.textContent = '-';
        }
        tr.appendChild(tdDupInfo);
        
        tbody.appendChild(tr);
    });
}

function showDuplicateDetails(record) {
    if (!record.is_duplicate || !record.duplicate_info) return;
    
    const dupInfo = record.duplicate_info;
    
    // Build differences table
    let differencesHtml = '';
    if (dupInfo.differences && dupInfo.differences.length > 0) {
        differencesHtml = `
            <h6 class="mt-3">Field Differences:</h6>
            <table class="table table-sm table-bordered">
                <thead>
                    <tr>
                        <th>Field</th>
                        <th>Existing Value</th>
                        <th>New Value</th>
                    </tr>
                </thead>
                <tbody>
                    ${dupInfo.differences.map(diff => `
                        <tr>
                            <td><strong>${diff.field.replace(/_/g, ' ')}</strong></td>
                            <td>${diff.existing_value}</td>
                            <td style="background-color: #fff3cd;">${diff.new_value}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } else {
        differencesHtml = '<p class="text-success mt-3"><i class="fas fa-check"></i> No differences found - data is identical</p>';
    }
    
    // Build existing data display
    let existingDataHtml = '';
    if (dupInfo.existing_data) {
        existingDataHtml = `
            <h6 class="mt-3">Existing Database Record:</h6>
            <div class="alert alert-info">
                ${Object.entries(dupInfo.existing_data).map(([key, value]) => `
                    <div><strong>${key.replace(/_/g, ' ')}:</strong> ${value || 'Not set'}</div>
                `).join('')}
            </div>
        `;
    }
    
    const modalHtml = `
        <div class="modal fade" id="duplicateModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-warning">
                        <h5 class="modal-title">
                            <i class="fas fa-exclamation-triangle"></i> Duplicate Entry Details
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-warning">
                            <strong>Duplicate Field:</strong> ${dupInfo.field}<br>
                            <strong>Value:</strong> ${dupInfo.value}<br>
                            <strong>Database ID:</strong> ${dupInfo.existing_id}
                        </div>
                        
                        ${existingDataHtml}
                        ${differencesHtml}
                        
                        <h6 class="mt-3">Recommended Actions:</h6>
                        <div class="list-group">
                            <div class="list-group-item">
                                <strong>Skip:</strong> Don't import this record (keep existing data)
                            </div>
                            <div class="list-group-item">
                                <strong>Update:</strong> Update existing record with new values
                            </div>
                            <div class="list-group-item">
                                <strong>Insert:</strong> Force insert (may cause database error)
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-warning" onclick="setRecordAction(${record.id}, 'skip')" data-bs-dismiss="modal">
                            Skip This Record
                        </button>
                        <button type="button" class="btn btn-primary" onclick="setRecordAction(${record.id}, 'update')" data-bs-dismiss="modal">
                            Update Existing
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('duplicateModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('duplicateModal'));
    modal.show();
}

function setRecordAction(recordId, action) {
    updateRecordAction(recordId, action);
    
    // Update the dropdown in the table
    const row = document.querySelector(`tr[data-record-id="${recordId}"]`);
    if (row) {
        const select = row.querySelector('select');
        if (select) {
            select.value = action;
        }
    }
    
    showAlert('success', `Action set to "${action}" for record #${recordId + 1}`);
}

function editCell(cell, recordId, column) {
    const currentValue = cell.textContent;
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'form-control form-control-sm';
    input.value = currentValue === '-' ? '' : currentValue;
    
    input.onblur = () => {
        const newValue = input.value;
        cell.textContent = newValue || '-';
        updateRecordData(recordId, column, newValue);
    };
    
    input.onkeypress = (e) => {
        if (e.key === 'Enter') {
            input.blur();
        }
    };
    
    cell.textContent = '';
    cell.appendChild(input);
    input.focus();
}

function updateRecordAction(recordId, action) {
    const record = previewData.find(r => r.id === recordId);
    if (record) {
        record.action = action;
        updateStatistics();
    }
}

function updateRecordData(recordId, column, value) {
    const record = previewData.find(r => r.id === recordId);
    if (record) {
        record.data[column] = value;
    }
}

function updateStatistics() {
    const insertCount = previewData.filter(r => r.action === 'insert').length;
    const updateCount = previewData.filter(r => r.action === 'update').length;
    const skipCount = previewData.filter(r => r.action === 'skip').length;
    
    document.getElementById('toInsert').textContent = insertCount;
    document.getElementById('finalInsertCount').textContent = insertCount;
    document.getElementById('finalUpdateCount').textContent = updateCount;
    document.getElementById('finalSkipCount').textContent = skipCount;
}

function filterPreview(filter) {
    currentFilter = filter;
    const rows = document.querySelectorAll('#previewTableBody tr');
    
    rows.forEach(row => {
        const recordId = parseInt(row.dataset.recordId);
        const record = previewData.find(r => r.id === recordId);
        
        if (!record) return;
        
        let show = false;
        
        switch(filter) {
            case 'all':
                show = true;
                break;
            case 'insert':
                show = record.action === 'insert';
                break;
            case 'duplicate':
                show = record.is_duplicate;
                break;
            case 'error':
                show = record.validation_status === 'error';
                break;
        }
        
        row.style.display = show ? '' : 'none';
    });
}

function proceedToImport() {
    updateStatistics();
    updateStep(3);
    document.getElementById('previewSection').style.display = 'none';
    document.getElementById('importSection').style.display = 'block';
}

function backToUpload() {
    updateStep(1);
    document.getElementById('previewSection').style.display = 'none';
    document.getElementById('uploadSection').style.display = 'block';
}

function backToPreview() {
    updateStep(2);
    document.getElementById('importSection').style.display = 'none';
    document.getElementById('previewSection').style.display = 'block';
}

function setupImportConfirmation() {
    const checkbox = document.getElementById('confirmImport');
    const button = document.getElementById('importButton');
    
    checkbox.addEventListener('change', () => {
        button.disabled = !checkbox.checked;
    });
}

async function executeImport() {
    document.getElementById('importProgress').style.display = 'block';
    document.getElementById('importButton').disabled = true;
    
    try {
        const response = await fetch('/admin/api/data-import/import', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: uploadedFilePath,
                category: selectedCategory,
                preview_data: previewData
            })
        });
        
        const result = await response.json();
        
        document.getElementById('importProgress').style.display = 'none';
        
        if (result.success) {
            document.getElementById('importResults').innerHTML = `
                <div class="alert alert-success">
                    <h6><i class="fas fa-check-circle"></i> Import Successful!</h6>
                    <ul>
                        <li>Inserted: ${result.statistics.inserted} records</li>
                        <li>Updated: ${result.statistics.updated} records</li>
                        <li>Skipped: ${result.statistics.skipped} records</li>
                    </ul>
                    ${result.errors && result.errors.length > 0 ? 
                        '<p class="mb-0"><strong>Errors:</strong> ' + result.errors.join(', ') + '</p>' : ''}
                </div>
                <button class="btn btn-primary" onclick="location.reload()">
                    <i class="fas fa-redo"></i> Import Another File
                </button>
            `;
        } else {
            document.getElementById('importResults').innerHTML = `
                <div class="alert alert-danger">
                    <h6><i class="fas fa-exclamation-circle"></i> Import Failed</h6>
                    <p>${result.error}</p>
                    ${result.errors ? '<ul>' + result.errors.map(e => '<li>' + e + '</li>').join('') + '</ul>' : ''}
                </div>
            `;
            document.getElementById('importButton').disabled = false;
        }
        
        document.getElementById('importResults').style.display = 'block';
        
    } catch (error) {
        document.getElementById('importProgress').style.display = 'none';
        document.getElementById('importButton').disabled = false;
        showAlert('error', 'Import failed: ' + error.message);
    }
}

function updateStep(stepNumber) {
    for (let i = 1; i <= 3; i++) {
        const step = document.getElementById('step' + i);
        if (i < stepNumber) {
            step.classList.add('completed');
            step.classList.remove('active');
        } else if (i === stepNumber) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active', 'completed');
        }
    }
}

function showLoading(message) {
    // Implement loading overlay
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    `;
    overlay.innerHTML = `
        <div class="text-center text-white">
            <div class="spinner-border mb-3" role="status"></div>
            <div>${message}</div>
        </div>
    `;
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.main-content');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => alertDiv.remove(), 5000);
}
