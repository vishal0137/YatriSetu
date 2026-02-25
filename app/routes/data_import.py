"""
Data Import Routes for YatriSetu Admin Panel
Handles file uploads and data extraction
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.data_extractor import DataExtractor

# Create blueprint
data_import_bp = Blueprint('data_import', __name__)

# Configuration
UPLOAD_FOLDER = 'uploads/data_imports'
ALLOWED_EXTENSIONS = {'csv', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@data_import_bp.route('/admin/data-import')
def data_import_page():
    """Render data import page"""
    return render_template('admin/data_import.html')


@data_import_bp.route('/admin/api/data-import/analyze', methods=['POST'])
def analyze_file():
    """
    Analyze uploaded file structure
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Only CSV and PDF files are allowed'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Initialize extractor
        extractor = DataExtractor()
        
        # Analyze file
        if filepath.endswith('.csv'):
            analysis = extractor.analyze_csv_structure(filepath)
            
            return jsonify({
                'success': True,
                'analysis': {
                    'filename': file.filename,
                    'filepath': filepath,
                    'file_type': 'CSV',
                    'total_rows': analysis['total_rows'],
                    'total_columns': analysis['total_columns'],
                    'columns': analysis['columns'],
                    'detected_category': analysis['detected_category'],
                    'confidence': analysis['matching_score'],
                    'sample_data': analysis['sample_data'],
                    'null_counts': analysis['null_counts']
                }
            })
        
        elif filepath.endswith('.pdf'):
            pdf_data = extractor.extract_from_pdf(filepath)
            
            return jsonify({
                'success': True,
                'analysis': {
                    'filename': file.filename,
                    'filepath': filepath,
                    'file_type': 'PDF',
                    'total_pages': pdf_data['total_pages'],
                    'tables_found': len(pdf_data['tables']),
                    'text_pages': len(pdf_data['text'])
                }
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@data_import_bp.route('/admin/api/data-import/extract', methods=['POST'])
def extract_data():
    """
    Extract data from uploaded file
    """
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        category = data.get('category')  # buses, routes, fares, stops
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        if category not in ['buses', 'routes', 'fares', 'stops']:
            return jsonify({
                'success': False,
                'error': 'Invalid category'
            }), 400
        
        # Initialize extractor
        extractor = DataExtractor()
        
        # Extract data based on category
        if category == 'buses':
            extracted = extractor.extract_buses_from_csv(filepath)
        elif category == 'routes':
            extracted = extractor.extract_routes_from_csv(filepath)
        elif category == 'fares':
            extracted = extractor.extract_fares_from_csv(filepath)
        elif category == 'stops':
            extracted = extractor.extract_stops_from_csv(filepath)
        
        # Get validation report
        report = extractor.get_validation_report()
        
        return jsonify({
            'success': True,
            'data': {
                'extracted_count': len(extracted),
                'extracted_data': extracted[:10],  # First 10 records for preview
                'validation_errors': report['errors'],
                'total_errors': report['total_errors']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@data_import_bp.route('/admin/api/data-import/import', methods=['POST'])
def import_to_database():
    """
    Import extracted data to database
    """
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        category = data.get('category')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        # Initialize extractor with database connection
        # TODO: Pass actual database connection
        extractor = DataExtractor()
        
        # Extract data
        if category == 'buses':
            extractor.extract_buses_from_csv(filepath)
        elif category == 'routes':
            extractor.extract_routes_from_csv(filepath)
        elif category == 'fares':
            extractor.extract_fares_from_csv(filepath)
        elif category == 'stops':
            extractor.extract_stops_from_csv(filepath)
        
        # Get validation report
        report = extractor.get_validation_report()
        
        if report['total_errors'] > 0:
            return jsonify({
                'success': False,
                'error': 'Validation errors found',
                'validation_errors': report['errors']
            }), 400
        
        # Insert to database
        inserted_count = extractor.insert_to_database(category)
        
        return jsonify({
            'success': True,
            'message': f'Successfully imported {inserted_count} {category} records',
            'inserted_count': inserted_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@data_import_bp.route('/admin/api/data-import/validate', methods=['POST'])
def validate_data():
    """
    Validate data structure and categories
    """
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        category = data.get('category')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        # Initialize extractor
        extractor = DataExtractor()
        
        # Extract and validate
        if category == 'buses':
            extractor.extract_buses_from_csv(filepath)
        elif category == 'routes':
            extractor.extract_routes_from_csv(filepath)
        elif category == 'fares':
            extractor.extract_fares_from_csv(filepath)
        elif category == 'stops':
            extractor.extract_stops_from_csv(filepath)
        
        # Get validation report
        report = extractor.get_validation_report()
        
        return jsonify({
            'success': True,
            'validation': {
                'total_errors': report['total_errors'],
                'errors': report['errors'],
                'extracted_counts': report['extracted_counts'],
                'is_valid': report['total_errors'] == 0
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@data_import_bp.route('/admin/api/data-import/export', methods=['POST'])
def export_data():
    """
    Export extracted data to CSV
    """
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        category = data.get('category')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        # Initialize extractor
        extractor = DataExtractor()
        
        # Extract data
        if category == 'buses':
            extractor.extract_buses_from_csv(filepath)
        elif category == 'routes':
            extractor.extract_routes_from_csv(filepath)
        elif category == 'fares':
            extractor.extract_fares_from_csv(filepath)
        elif category == 'stops':
            extractor.extract_stops_from_csv(filepath)
        
        # Export to CSV
        output_filename = f"exported_{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        extractor.export_to_csv(category, output_path)
        
        return jsonify({
            'success': True,
            'message': f'Data exported successfully',
            'output_file': output_filename,
            'download_url': f'/uploads/data_imports/{output_filename}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
