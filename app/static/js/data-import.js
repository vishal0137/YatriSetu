/**
 * Data Import JavaScript
 * Handles file upload, analysis, extraction, and database import
 */

let currentFilePath = null;
let currentAnalysis = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeUploadArea();
    initializeFileInput();
});

/**
 * Initialize drag and drop upload area
 */
function initializeUploadArea() {
    const uploadArea = document.getElementById('uploadArea');
    
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.add('dragover');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.remove('dragover');
        }, false);
    });
    
    // Handle dropped files
    uploadArea.addEventListener('drop', handleDrop, false);
    
    // Handle click to upload
    uploadArea.addEventListener('click', () => {
        document.getElementById('fileInput').click();
    });
}

/**
 * Initialize file input change handler
 */
function initializeFileInput() {
    const fileInput = document.getElementById('fileInput');
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            handleFile(this.files[0]);
        }
    });
}

/**
 * Prevent default drag behaviors
 */
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

/**
 * Handle dropped file
 */
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

/**
 * Handle file selection
 */
function handleFile(file) {
    // Validate file type
    const allowedTypes = ['text/csv', 'application/pdf', 'application/vnd.ms-excel'];
    const allowedExtensions = ['.csv', '.pdf'];
    
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedExtensions.includes(fileExtension)) {
        showAlert('Invalid file type. Only CSV and PDF files are allowed.', 'danger');
        return;
    }
    
    // Validate file size (10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        showAlert('File size exceeds 10MB limit.', 'danger');
        return;
    }
    
    // Show file info
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileInfo').style.display = 'block';
    
    // Upload and analyze file
    uploadAndAnalyze(file);
}

/**
 * Upload and analyze file
 */
async function uploadAndAnalyze(file) {
    try {
        showLoading('Uploading and analyzing file...');
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/admin/api/data-import/analyze', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        hideLoading();
        
        if (result.success) {
            currentFilePath = result.analysis.filepath;
            currentAnalysis = result.analysis;
            displayAnalysis(result.analysis);
            showAlert('File analyzed successfully!', 'success');
        } else {
            showAlert(result.error, 'danger');
        }
        
    } catch (error) {
        hideLoading();
        showAlert('Error analyzing file: ' + error.message, 'danger');
    }
}

/**
 * Display file analysis results
 */
function displayAnalysis(analysis) {
    // Show analysis section
    document.getElementById('analysisSection').style.display = 'block';
    
    // Update statistics
    document.getElementById('totalRows').textContent = analysis.total_rows || '-';
    document.getElementById('totalColumns').textContent = analysis.total_columns || '-';
    document.getElementById('detectedCategory').textContent = 
        analysis.detected_category ? analysis.detected_category.toUpperCase() : 'Unknown';
    document.getElementById('confidence').textContent = 
        analysis.confidence ? analysis.confidence + '%' : '-';
    
    // Display columns
    const columnsList = document.getElementById('columnsList');
    columnsList.innerHTML = '';
    if (analysis.columns) {
        analysis.columns.forEach(col => {
            const badge = document.createElement('span');
            badge.className = 'badge bg-primary';
            badge.textContent = col;
            columnsList.appendChild(badge);
        });
    }
    
    // Display sample data
    if (analysis.sample_data && analysis.sample_data.length > 0) {
        displaySampleData(analysis.sample_data, analysis.columns);
    }
    
    // Pre-select detected category
    if (analysis.detected_category) {
        document.getElementById('categorySelect').value = analysis.detected_category;
    }
}

/**
 * Display sample data in table
 */
function displaySampleData(data, columns) {
    const thead = document.getElementById('sampleTableHead');
    const tbody = document.getElementById('sampleTableBody');
    
    // Clear existing content
    thead.innerHTML = '';
    tbody.innerHTML = '';
    
    // Create header row
    const headerRow = document.createElement('tr');
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    
    // Create data rows
    data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(col => {
            const td = document.createElement('td');
            td.textContent = row[col] || '-';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

/**
 * Extract data from file
 */
async function extractData() {
    const category = document.getElementById('categorySelect').value;
    
    if (!category) {
        showAlert('Please select a data category', 'warning');
        return;
    }
    
    if (!currentFilePath) {
        showAlert('Please upload a file first', 'warning');
        return;
    }
    
    try {
        showLoading('Extracting data...');
        
        const response = await fetch('/admin/api/data-import/extract', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: currentFilePath,
                category: category
            })
        });
        
        const result = await response.json();
        
        hideLoading();
        
        if (result.success) {
            displayExtractionResults(result.data, category);
            showAlert(`Extracted ${result.data.extracted_count} ${category} records`, 'success');
        } else {
            showAlert(result.error, 'danger');
        }
        
    } catch (error) {
        hideLoading();
        showAlert('Error extracting data: ' + error.message, 'danger');
    }
}

/**
 * Display extraction results
 */
function displayExtractionResults(data, category) {
    // Show extraction section
    document.getElementById('extractionSection').style.display = 'block';
    
    // Show success message
    document.getElementById('extractionMessage').textContent = 
        `Extracted ${data.extracted_count} ${category} records`;
    document.getElementById('extractionSuccess').style.display = 'block';
    
    // Show validation warnings if any
    if (data.total_errors > 0) {
        const errorsList = document.getElementById('validationErrorsList');
        errorsList.innerHTML = '';
        data.validation_errors.forEach(error => {
            const li = document.createElement('li');
            li.textContent = error;
            errorsList.appendChild(li);
        });
        document.getElementById('validationWarnings').style.display = 'block';
    } else {
        document.getElementById('validationWarnings').style.display = 'none';
    }
    
    // Display extracted data
    if (data.extracted_data && data.extracted_data.length > 0) {
        displayExtractedData(data.extracted_data);
    }
}

/**
 * Display extracted data in table
 */
function displayExtractedData(data) {
    const thead = document.getElementById('extractedTableHead');
    const tbody = document.getElementById('extractedTableBody');
    
    // Clear existing content
    thead.innerHTML = '';
    tbody.innerHTML = '';
    
    // Get columns from first record
    const columns = Object.keys(data[0]);
    
    // Create header row
    const headerRow = document.createElement('tr');
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col.replace(/_/g, ' ').toUpperCase();
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    
    // Create data rows
    data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(col => {
            const td = document.createElement('td');
            td.textContent = row[col] || '-';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

/**
 * Validate data
 */
async function validateData() {
    const category = document.getElementById('categorySelect').value;
    
    if (!category) {
        showAlert('Please select a data category', 'warning');
        return;
    }
    
    if (!currentFilePath) {
        showAlert('Please upload a file first', 'warning');
        return;
    }
    
    try {
        showLoading('Validating data...');
        
        const response = await fetch('/admin/api/data-import/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: currentFilePath,
                category: category
            })
        });
        
        const result = await response.json();
        
        hideLoading();
        
        if (result.success) {
            if (result.validation.is_valid) {
                showAlert('Data validation passed! No errors found.', 'success');
            } else {
                showAlert(`Validation found ${result.validation.total_errors} errors`, 'warning');
                
                // Display errors
                const errorsList = document.getElementById('validationErrorsList');
                errorsList.innerHTML = '';
                result.validation.errors.forEach(error => {
                    const li = document.createElement('li');
                    li.textContent = error;
                    errorsList.appendChild(li);
                });
                document.getElementById('validationWarnings').style.display = 'block';
            }
        } else {
            showAlert(result.error, 'danger');
        }
        
    } catch (error) {
        hideLoading();
        showAlert('Error validating data: ' + error.message, 'danger');
    }
}

/**
 * Import data to database
 */
async function importToDatabase() {
    const category = document.getElementById('categorySelect').value;
    
    if (!category) {
        showAlert('Please select a data category', 'warning');
        return;
    }
    
    if (!currentFilePath) {
        showAlert('Please upload a file first', 'warning');
        return;
    }
    
    if (!confirm('Are you sure you want to import this data to the database?')) {
        return;
    }
    
    try {
        showLoading('Importing data to database...');
        
        const response = await fetch('/admin/api/data-import/import', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: currentFilePath,
                category: category
            })
        });
        
        const result = await response.json();
        
        hideLoading();
        
        if (result.success) {
            showAlert(result.message, 'success');
        } else {
            showAlert(result.error, 'danger');
            
            if (result.validation_errors) {
                const errorsList = document.getElementById('validationErrorsList');
                errorsList.innerHTML = '';
                result.validation_errors.forEach(error => {
                    const li = document.createElement('li');
                    li.textContent = error;
                    errorsList.appendChild(li);
                });
                document.getElementById('validationWarnings').style.display = 'block';
            }
        }
        
    } catch (error) {
        hideLoading();
        showAlert('Error importing data: ' + error.message, 'danger');
    }
}

/**
 * Export data to CSV
 */
async function exportData() {
    const category = document.getElementById('categorySelect').value;
    
    if (!category) {
        showAlert('Please select a data category', 'warning');
        return;
    }
    
    if (!currentFilePath) {
        showAlert('Please upload a file first', 'warning');
        return;
    }
    
    try {
        showLoading('Exporting data...');
        
        const response = await fetch('/admin/api/data-import/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: currentFilePath,
                category: category
            })
        });
        
        const result = await response.json();
        
        hideLoading();
        
        if (result.success) {
            showAlert(result.message, 'success');
            // Optionally trigger download
            // window.location.href = result.download_url;
        } else {
            showAlert(result.error, 'danger');
        }
        
    } catch (error) {
        hideLoading();
        showAlert('Error exporting data: ' + error.message, 'danger');
    }
}

/**
 * Clear selected file
 */
function clearFile() {
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('analysisSection').style.display = 'none';
    document.getElementById('extractionSection').style.display = 'none';
    currentFilePath = null;
    currentAnalysis = null;
}

/**
 * Show alert message
 */
function showAlert(message, type) {
    // Use common.js showAlert if available
    if (typeof window.showAlert === 'function') {
        window.showAlert(message, type);
    } else {
        alert(message);
    }
}

/**
 * Show loading indicator
 */
function showLoading(message) {
    // Implement loading indicator
    console.log('Loading:', message);
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    // Implement hide loading
    console.log('Loading complete');
}
