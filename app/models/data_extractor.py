"""
Data Extractor Module for YatriSetu
Extracts buses, routes, and fares data from CSV and PDF files
Validates data structure and inserts into database
"""

import csv
import re
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExtractor:
    """
    Main class for extracting and validating transport data from files
    """
    
    def __init__(self, db_connection=None):
        """
        Initialize the data extractor
        
        Args:
            db_connection: Database connection object (optional)
        """
        self.db = db_connection
        self.validation_errors = []
        self.validation_warnings = []
        self.duplicate_checks = []
        self.extracted_data = {
            'buses': [],
            'routes': [],
            'fares': [],
            'stops': []
        }
        self.preview_data = {
            'buses': [],
            'routes': [],
            'fares': [],
            'stops': []
        }
        
        # Define expected data structures
        self.expected_schemas = {
            'buses': ['bus_number', 'bus_type', 'capacity', 'status'],
            'routes': ['route_number', 'route_name', 'start_location', 'end_location', 'distance'],
            'fares': ['route_id', 'passenger_type', 'fare_amount'],
            'stops': ['stop_name', 'latitude', 'longitude', 'route_id', 'sequence']
        }
        
        # Valid values for categorical fields
        self.valid_categories = {
            'bus_type': ['AC', 'Non-AC', 'Electric', 'CNG', 'Diesel'],
            'status': ['Active', 'Inactive', 'Maintenance', 'Retired'],
            'passenger_type': ['General', 'Student', 'Senior Citizen', 'Differently Abled', 'Child']
        }
    
    def detect_file_type(self, file_path: str) -> str:
        """
        Detect file type from extension
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type ('csv' or 'pdf')
        """
        if file_path.lower().endswith('.csv'):
            return 'csv'
        elif file_path.lower().endswith('.pdf'):
            return 'pdf'
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
    
    def analyze_csv_structure(self, file_path: str) -> Dict:
        """
        Analyze CSV file structure and detect data categories
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Dictionary with file analysis results
        """
        try:
            df = pd.read_csv(file_path)
            
            analysis = {
                'file_path': file_path,
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'columns': list(df.columns),
                'data_types': df.dtypes.to_dict(),
                'null_counts': df.isnull().sum().to_dict(),
                'detected_category': None,
                'matching_score': 0
            }
            
            # Detect which category this file belongs to
            category, score = self._detect_data_category(df.columns)
            analysis['detected_category'] = category
            analysis['matching_score'] = score
            
            # Sample data
            analysis['sample_data'] = df.head(3).to_dict('records')
            
            logger.info(f"CSV Analysis: {analysis['detected_category']} detected with {score}% confidence")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing CSV: {str(e)}")
            raise
    
    def _detect_data_category(self, columns: List[str]) -> Tuple[str, int]:
        """
        Detect which data category (buses, routes, fares, stops) based on columns
        
        Args:
            columns: List of column names
            
        Returns:
            Tuple of (category_name, matching_percentage)
        """
        columns_lower = [col.lower().strip() for col in columns]
        best_match = None
        best_score = 0
        
        for category, expected_cols in self.expected_schemas.items():
            matches = 0
            for expected_col in expected_cols:
                # Check for exact or partial matches
                for col in columns_lower:
                    if expected_col.lower() in col or col in expected_col.lower():
                        matches += 1
                        break
            
            score = int((matches / len(expected_cols)) * 100)
            
            if score > best_score:
                best_score = score
                best_match = category
        
        return best_match, best_score
    
    def extract_buses_from_csv(self, file_path: str) -> List[Dict]:
        """
        Extract bus data from CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of bus dictionaries
        """
        try:
            df = pd.read_csv(file_path)
            buses = []
            
            # Normalize column names
            df.columns = [col.lower().strip().replace(' ', '_') for col in df.columns]
            
            for idx, row in df.iterrows():
                bus = {
                    'bus_number': self._extract_value(row, ['bus_number', 'bus_no', 'registration_number', 'vehicle_number']),
                    'bus_type': self._extract_value(row, ['bus_type', 'type', 'category']),
                    'capacity': self._extract_value(row, ['capacity', 'seating_capacity', 'seats']),
                    'status': self._extract_value(row, ['status', 'operational_status', 'state']),
                    'manufacturer': self._extract_value(row, ['manufacturer', 'make', 'brand']),
                    'model': self._extract_value(row, ['model', 'vehicle_model']),
                    'year': self._extract_value(row, ['year', 'manufacturing_year', 'model_year'])
                }
                
                # Validate bus data
                if self._validate_bus_data(bus, idx + 1):
                    buses.append(bus)
            
            self.extracted_data['buses'] = buses
            logger.info(f"Extracted {len(buses)} buses from CSV")
            
            return buses
            
        except Exception as e:
            logger.error(f"Error extracting buses: {str(e)}")
            raise
    
    def extract_routes_from_csv(self, file_path: str) -> List[Dict]:
        """
        Extract route data from CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of route dictionaries
        """
        try:
            df = pd.read_csv(file_path)
            routes = []
            
            # Normalize column names
            df.columns = [col.lower().strip().replace(' ', '_') for col in df.columns]
            
            for idx, row in df.iterrows():
                route = {
                    'route_number': self._extract_value(row, ['route_number', 'route_no', 'route_id', 'route_code']),
                    'route_name': self._extract_value(row, ['route_name', 'name', 'route_description']),
                    'start_location': self._extract_value(row, ['start_location', 'origin', 'from', 'source', 'start_point']),
                    'end_location': self._extract_value(row, ['end_location', 'destination', 'to', 'end_point']),
                    'distance': self._extract_value(row, ['distance', 'total_distance', 'route_distance']),
                    'duration': self._extract_value(row, ['duration', 'travel_time', 'estimated_time']),
                    'frequency': self._extract_value(row, ['frequency', 'service_frequency', 'buses_per_hour'])
                }
                
                # Validate route data
                if self._validate_route_data(route, idx + 1):
                    routes.append(route)
            
            self.extracted_data['routes'] = routes
            logger.info(f"Extracted {len(routes)} routes from CSV")
            
            return routes
            
        except Exception as e:
            logger.error(f"Error extracting routes: {str(e)}")
            raise
    
    def extract_fares_from_csv(self, file_path: str) -> List[Dict]:
        """
        Extract fare data from CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of fare dictionaries
        """
        try:
            df = pd.read_csv(file_path)
            fares = []
            
            # Normalize column names
            df.columns = [col.lower().strip().replace(' ', '_') for col in df.columns]
            
            for idx, row in df.iterrows():
                fare = {
                    'route_id': self._extract_value(row, ['route_id', 'route_number', 'route_no']),
                    'passenger_type': self._extract_value(row, ['passenger_type', 'category', 'type', 'passenger_category']),
                    'fare_amount': self._extract_value(row, ['fare_amount', 'fare', 'price', 'amount', 'cost']),
                    'distance_range': self._extract_value(row, ['distance_range', 'distance', 'km_range']),
                    'effective_date': self._extract_value(row, ['effective_date', 'valid_from', 'start_date'])
                }
                
                # Validate fare data
                if self._validate_fare_data(fare, idx + 1):
                    fares.append(fare)
            
            self.extracted_data['fares'] = fares
            logger.info(f"Extracted {len(fares)} fares from CSV")
            
            return fares
            
        except Exception as e:
            logger.error(f"Error extracting fares: {str(e)}")
            raise
    
    def extract_stops_from_csv(self, file_path: str) -> List[Dict]:
        """
        Extract stop data from CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of stop dictionaries
        """
        try:
            df = pd.read_csv(file_path)
            stops = []
            
            # Normalize column names
            df.columns = [col.lower().strip().replace(' ', '_') for col in df.columns]
            
            for idx, row in df.iterrows():
                stop = {
                    'stop_name': self._extract_value(row, ['stop_name', 'name', 'station_name', 'location']),
                    'latitude': self._extract_value(row, ['latitude', 'lat']),
                    'longitude': self._extract_value(row, ['longitude', 'lon', 'lng', 'long']),
                    'route_id': self._extract_value(row, ['route_id', 'route_number', 'route_no']),
                    'sequence': self._extract_value(row, ['sequence', 'stop_sequence', 'order', 'stop_order']),
                    'arrival_time': self._extract_value(row, ['arrival_time', 'arrival', 'time'])
                }
                
                # Validate stop data
                if self._validate_stop_data(stop, idx + 1):
                    stops.append(stop)
            
            self.extracted_data['stops'] = stops
            logger.info(f"Extracted {len(stops)} stops from CSV")
            
            return stops
            
        except Exception as e:
            logger.error(f"Error extracting stops: {str(e)}")
            raise
    
    def extract_from_pdf(self, file_path: str) -> Dict:
        """
        Extract data from PDF file
        Requires: pip install PyPDF2 pdfplumber tabula-py
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary with extracted data
        """
        try:
            import pdfplumber
            
            extracted_text = []
            tables = []
            
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    text = page.extract_text()
                    if text:
                        extracted_text.append({
                            'page': page_num,
                            'text': text
                        })
                    
                    # Extract tables
                    page_tables = page.extract_tables()
                    if page_tables:
                        for table_num, table in enumerate(page_tables, 1):
                            tables.append({
                                'page': page_num,
                                'table_number': table_num,
                                'data': table
                            })
            
            logger.info(f"Extracted {len(tables)} tables from PDF")
            
            return {
                'text': extracted_text,
                'tables': tables,
                'total_pages': len(pdf.pages)
            }
            
        except ImportError:
            logger.error("PDF extraction requires: pip install pdfplumber")
            raise
        except Exception as e:
            logger.error(f"Error extracting from PDF: {str(e)}")
            raise
    
    def _extract_value(self, row: pd.Series, possible_keys: List[str]) -> Optional[str]:
        """
        Extract value from row using multiple possible column names
        
        Args:
            row: Pandas Series (row)
            possible_keys: List of possible column names
            
        Returns:
            Extracted value or None
        """
        for key in possible_keys:
            if key in row.index and pd.notna(row[key]):
                return str(row[key]).strip()
        return None
    
    def _validate_bus_data(self, bus: Dict, row_num: int) -> bool:
        """
        Validate bus data
        
        Args:
            bus: Bus dictionary
            row_num: Row number for error reporting
            
        Returns:
            True if valid, False otherwise
        """
        errors = []
        
        # Required fields
        if not bus.get('bus_number'):
            errors.append(f"Row {row_num}: Missing bus_number")
        
        # Validate bus_type
        if bus.get('bus_type') and bus['bus_type'] not in self.valid_categories['bus_type']:
            errors.append(f"Row {row_num}: Invalid bus_type '{bus['bus_type']}'")
        
        # Validate capacity
        if bus.get('capacity'):
            try:
                capacity = int(bus['capacity'])
                if capacity <= 0 or capacity > 200:
                    errors.append(f"Row {row_num}: Invalid capacity {capacity}")
            except ValueError:
                errors.append(f"Row {row_num}: Capacity must be a number")
        
        # Validate status
        if bus.get('status') and bus['status'] not in self.valid_categories['status']:
            errors.append(f"Row {row_num}: Invalid status '{bus['status']}'")
        
        if errors:
            self.validation_errors.extend(errors)
            logger.warning(f"Validation errors for bus at row {row_num}: {errors}")
            return False
        
        return True
    
    def _validate_route_data(self, route: Dict, row_num: int) -> bool:
        """
        Validate route data
        
        Args:
            route: Route dictionary
            row_num: Row number for error reporting
            
        Returns:
            True if valid, False otherwise
        """
        errors = []
        
        # Required fields
        if not route.get('route_number'):
            errors.append(f"Row {row_num}: Missing route_number")
        
        if not route.get('start_location'):
            errors.append(f"Row {row_num}: Missing start_location")
        
        if not route.get('end_location'):
            errors.append(f"Row {row_num}: Missing end_location")
        
        # Validate distance
        if route.get('distance'):
            try:
                distance = float(route['distance'])
                if distance <= 0:
                    errors.append(f"Row {row_num}: Distance must be positive")
            except ValueError:
                errors.append(f"Row {row_num}: Distance must be a number")
        
        if errors:
            self.validation_errors.extend(errors)
            logger.warning(f"Validation errors for route at row {row_num}: {errors}")
            return False
        
        return True
    
    def _validate_fare_data(self, fare: Dict, row_num: int) -> bool:
        """
        Validate fare data
        
        Args:
            fare: Fare dictionary
            row_num: Row number for error reporting
            
        Returns:
            True if valid, False otherwise
        """
        errors = []
        
        # Required fields
        if not fare.get('route_id'):
            errors.append(f"Row {row_num}: Missing route_id")
        
        if not fare.get('passenger_type'):
            errors.append(f"Row {row_num}: Missing passenger_type")
        
        # Validate passenger_type
        if fare.get('passenger_type') and fare['passenger_type'] not in self.valid_categories['passenger_type']:
            errors.append(f"Row {row_num}: Invalid passenger_type '{fare['passenger_type']}'")
        
        # Validate fare_amount
        if not fare.get('fare_amount'):
            errors.append(f"Row {row_num}: Missing fare_amount")
        else:
            try:
                amount = float(fare['fare_amount'])
                if amount < 0:
                    errors.append(f"Row {row_num}: Fare amount cannot be negative")
            except ValueError:
                errors.append(f"Row {row_num}: Fare amount must be a number")
        
        if errors:
            self.validation_errors.extend(errors)
            logger.warning(f"Validation errors for fare at row {row_num}: {errors}")
            return False
        
        return True
    
    def _validate_stop_data(self, stop: Dict, row_num: int) -> bool:
        """
        Validate stop data
        
        Args:
            stop: Stop dictionary
            row_num: Row number for error reporting
            
        Returns:
            True if valid, False otherwise
        """
        errors = []
        
        # Required fields
        if not stop.get('stop_name'):
            errors.append(f"Row {row_num}: Missing stop_name")
        
        # Validate coordinates
        if stop.get('latitude'):
            try:
                lat = float(stop['latitude'])
                if lat < -90 or lat > 90:
                    errors.append(f"Row {row_num}: Invalid latitude {lat}")
            except ValueError:
                errors.append(f"Row {row_num}: Latitude must be a number")
        
        if stop.get('longitude'):
            try:
                lon = float(stop['longitude'])
                if lon < -180 or lon > 180:
                    errors.append(f"Row {row_num}: Invalid longitude {lon}")
            except ValueError:
                errors.append(f"Row {row_num}: Longitude must be a number")
        
        # Validate sequence
        if stop.get('sequence'):
            try:
                seq = int(stop['sequence'])
                if seq < 1:
                    errors.append(f"Row {row_num}: Sequence must be positive")
            except ValueError:
                errors.append(f"Row {row_num}: Sequence must be a number")
        
        if errors:
            self.validation_errors.extend(errors)
            logger.warning(f"Validation errors for stop at row {row_num}: {errors}")
            return False
        
        return True
    
    def check_duplicates_in_database(self, category: str) -> Dict:
        """
        Check for duplicate entries in database with detailed comparison
        
        Args:
            category: Data category (buses, routes, fares, stops)
            
        Returns:
            Dictionary with duplicate information including existing data
        """
        if not self.db:
            logger.warning("Database connection not provided, skipping duplicate check")
            return {'duplicates': [], 'total_duplicates': 0}
        
        from app.models.database_models import Bus, Route, Stop
        
        duplicates = []
        data = self.extracted_data.get(category, [])
        
        try:
            if category == 'buses':
                for idx, bus in enumerate(data):
                    existing = Bus.query.filter_by(bus_number=bus.get('bus_number')).first()
                    if existing:
                        duplicates.append({
                            'index': idx,
                            'field': 'bus_number',
                            'value': bus.get('bus_number'),
                            'existing_id': existing.id,
                            'existing_data': {
                                'bus_number': existing.bus_number,
                                'bus_type': existing.bus_type,
                                'capacity': existing.capacity,
                                'status': 'Active' if existing.is_active else 'Inactive',
                                'registration_number': existing.registration_number
                            },
                            'new_data': bus,
                            'differences': self._compare_data(
                                {
                                    'bus_number': existing.bus_number,
                                    'bus_type': existing.bus_type,
                                    'capacity': str(existing.capacity),
                                    'status': 'Active' if existing.is_active else 'Inactive'
                                },
                                bus
                            ),
                            'action': 'skip'
                        })
            
            elif category == 'routes':
                for idx, route in enumerate(data):
                    existing = Route.query.filter_by(route_number=route.get('route_number')).first()
                    if existing:
                        duplicates.append({
                            'index': idx,
                            'field': 'route_number',
                            'value': route.get('route_number'),
                            'existing_id': existing.id,
                            'existing_data': {
                                'route_number': existing.route_number,
                                'route_name': existing.route_name,
                                'start_location': existing.start_location,
                                'end_location': existing.end_location,
                                'distance': str(existing.distance_km) if existing.distance_km else None,
                                'duration': str(existing.estimated_duration_minutes) if existing.estimated_duration_minutes else None
                            },
                            'new_data': route,
                            'differences': self._compare_data(
                                {
                                    'route_number': existing.route_number,
                                    'route_name': existing.route_name,
                                    'start_location': existing.start_location,
                                    'end_location': existing.end_location,
                                    'distance': str(existing.distance_km) if existing.distance_km else None
                                },
                                route
                            ),
                            'action': 'skip'
                        })
            
            elif category == 'stops':
                for idx, stop in enumerate(data):
                    # Try to find route by route_number
                    route = Route.query.filter_by(route_number=stop.get('route_id')).first()
                    if route:
                        existing = Stop.query.filter_by(
                            route_id=route.id,
                            stop_name=stop.get('stop_name'),
                            stop_order=int(stop.get('sequence', 0))
                        ).first()
                        if existing:
                            duplicates.append({
                                'index': idx,
                                'field': 'stop_name + sequence',
                                'value': f"{stop.get('stop_name')} (Seq: {stop.get('sequence')})",
                                'existing_id': existing.id,
                                'existing_data': {
                                    'stop_name': existing.stop_name,
                                    'sequence': str(existing.stop_order),
                                    'route_id': stop.get('route_id'),
                                    'latitude': str(existing.latitude) if existing.latitude else None,
                                    'longitude': str(existing.longitude) if existing.longitude else None
                                },
                                'new_data': stop,
                                'differences': self._compare_data(
                                    {
                                        'stop_name': existing.stop_name,
                                        'sequence': str(existing.stop_order),
                                        'latitude': str(existing.latitude) if existing.latitude else None,
                                        'longitude': str(existing.longitude) if existing.longitude else None
                                    },
                                    stop
                                ),
                                'action': 'skip'
                            })
            
            self.duplicate_checks = duplicates
            logger.info(f"Found {len(duplicates)} potential duplicates in {category}")
            
        except Exception as e:
            logger.error(f"Error checking duplicates: {str(e)}")
        
        return {
            'duplicates': duplicates,
            'total_duplicates': len(duplicates)
        }
    
    def _compare_data(self, existing: Dict, new: Dict) -> List[Dict]:
        """
        Compare existing and new data to find differences
        
        Args:
            existing: Existing data from database
            new: New data from file
            
        Returns:
            List of differences
        """
        differences = []
        
        for key in existing.keys():
            existing_value = str(existing.get(key, '')).strip() if existing.get(key) else ''
            new_value = str(new.get(key, '')).strip() if new.get(key) else ''
            
            if existing_value != new_value:
                differences.append({
                    'field': key,
                    'existing_value': existing_value or 'Not set',
                    'new_value': new_value or 'Not set',
                    'changed': True
                })
        
        return differences
    
    def get_preview_data(self, category: str, limit: int = 100) -> List[Dict]:
        """
        Get preview of extracted data with editable fields
        
        Args:
            category: Data category (buses, routes, fares, stops)
            limit: Maximum number of records to preview
            
        Returns:
            List of dictionaries with preview data
        """
        data = self.extracted_data.get(category, [])
        preview = []
        
        for idx, record in enumerate(data[:limit]):
            preview_record = {
                'id': idx,
                'data': record,
                'is_duplicate': False,
                'duplicate_info': None,
                'validation_status': 'valid',
                'editable': True,
                'action': 'insert'  # insert, update, skip
            }
            
            # Check if this record is a duplicate
            for dup in self.duplicate_checks:
                if dup['index'] == idx:
                    preview_record['is_duplicate'] = True
                    preview_record['duplicate_info'] = dup
                    preview_record['action'] = 'skip'
                    break
            
            preview.append(preview_record)
        
        self.preview_data[category] = preview
        return preview
    
    def update_preview_record(self, category: str, record_id: int, updated_data: Dict, action: str = 'insert'):
        """
        Update a preview record with edited data
        
        Args:
            category: Data category
            record_id: Record ID in preview
            updated_data: Updated data dictionary
            action: Action to take (insert, update, skip)
        """
        if category not in self.preview_data:
            raise ValueError(f"No preview data for category: {category}")
        
        for record in self.preview_data[category]:
            if record['id'] == record_id:
                record['data'] = updated_data
                record['action'] = action
                logger.info(f"Updated preview record {record_id} in {category}")
                break
    
    def get_validation_report(self) -> Dict:
        """
        Get validation report
        
        Returns:
            Dictionary with validation statistics
        """
        return {
            'total_errors': len(self.validation_errors),
            'total_warnings': len(self.validation_warnings),
            'errors': self.validation_errors,
            'warnings': self.validation_warnings,
            'duplicates': self.duplicate_checks,
            'total_duplicates': len(self.duplicate_checks),
            'extracted_counts': {
                'buses': len(self.extracted_data['buses']),
                'routes': len(self.extracted_data['routes']),
                'fares': len(self.extracted_data['fares']),
                'stops': len(self.extracted_data['stops'])
            }
        }
    
    def export_to_csv(self, category: str, output_path: str):
        """
        Export extracted data to CSV
        
        Args:
            category: Data category (buses, routes, fares, stops)
            output_path: Output CSV file path
        """
        if category not in self.extracted_data:
            raise ValueError(f"Invalid category: {category}")
        
        data = self.extracted_data[category]
        if not data:
            logger.warning(f"No data to export for category: {category}")
            return
        
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        logger.info(f"Exported {len(data)} {category} records to {output_path}")
    
    def insert_to_database(self, category: str, use_preview: bool = True) -> Dict:
        """
        Insert extracted data into database with duplicate prevention
        
        Args:
            category: Data category (buses, routes, fares, stops)
            use_preview: Use preview data with user modifications
            
        Returns:
            Dictionary with insertion statistics
        """
        if not self.db:
            raise ValueError("Database connection not provided")
        
        if category not in self.extracted_data:
            raise ValueError(f"Invalid category: {category}")
        
        from app.models.database_models import Bus, Route, Stop
        from app import db as database
        
        # Use preview data if available and requested
        if use_preview and self.preview_data.get(category):
            data_to_insert = [
                record['data'] for record in self.preview_data[category]
                if record['action'] == 'insert'
            ]
            data_to_update = [
                record for record in self.preview_data[category]
                if record['action'] == 'update'
            ]
            data_to_skip = [
                record for record in self.preview_data[category]
                if record['action'] == 'skip'
            ]
        else:
            data_to_insert = self.extracted_data[category]
            data_to_update = []
            data_to_skip = []
        
        inserted_count = 0
        updated_count = 0
        skipped_count = len(data_to_skip)
        errors = []
        
        try:
            # Insert new records
            if category == 'buses':
                for bus_data in data_to_insert:
                    try:
                        # Check for duplicate one more time
                        existing = Bus.query.filter_by(bus_number=bus_data.get('bus_number')).first()
                        if existing:
                            skipped_count += 1
                            logger.warning(f"Skipping duplicate bus: {bus_data.get('bus_number')}")
                            continue
                        
                        bus = Bus(
                            bus_number=bus_data.get('bus_number'),
                            registration_number=bus_data.get('bus_number'),  # Use bus_number as registration
                            bus_type=bus_data.get('bus_type', 'Regular'),
                            capacity=int(bus_data.get('capacity', 50)),
                            is_active=bus_data.get('status', 'Active') == 'Active'
                        )
                        database.session.add(bus)
                        inserted_count += 1
                    except Exception as e:
                        errors.append(f"Error inserting bus {bus_data.get('bus_number')}: {str(e)}")
            
            elif category == 'routes':
                for route_data in data_to_insert:
                    try:
                        # Check for duplicate
                        existing = Route.query.filter_by(route_number=route_data.get('route_number')).first()
                        if existing:
                            skipped_count += 1
                            logger.warning(f"Skipping duplicate route: {route_data.get('route_number')}")
                            continue
                        
                        route = Route(
                            route_number=route_data.get('route_number'),
                            route_name=route_data.get('route_name', ''),
                            start_location=route_data.get('start_location'),
                            end_location=route_data.get('end_location'),
                            distance_km=float(route_data.get('distance', 0)) if route_data.get('distance') else None,
                            estimated_duration_minutes=int(route_data.get('duration', 0)) if route_data.get('duration') else None,
                            fare=50.0  # Default fare
                        )
                        database.session.add(route)
                        inserted_count += 1
                    except Exception as e:
                        errors.append(f"Error inserting route {route_data.get('route_number')}: {str(e)}")
            
            elif category == 'stops':
                for stop_data in data_to_insert:
                    try:
                        # Check for duplicate
                        existing = Stop.query.filter_by(
                            route_id=stop_data.get('route_id'),
                            stop_name=stop_data.get('stop_name'),
                            stop_order=int(stop_data.get('sequence', 0))
                        ).first()
                        if existing:
                            skipped_count += 1
                            logger.warning(f"Skipping duplicate stop: {stop_data.get('stop_name')}")
                            continue
                        
                        # Get route by route_number
                        route = Route.query.filter_by(route_number=stop_data.get('route_id')).first()
                        if not route:
                            errors.append(f"Route not found for stop: {stop_data.get('stop_name')}")
                            continue
                        
                        stop = Stop(
                            route_id=route.id,
                            stop_name=stop_data.get('stop_name'),
                            stop_order=int(stop_data.get('sequence', 0)),
                            latitude=float(stop_data.get('latitude')) if stop_data.get('latitude') else None,
                            longitude=float(stop_data.get('longitude')) if stop_data.get('longitude') else None,
                            estimated_arrival_time=stop_data.get('arrival_time')
                        )
                        database.session.add(stop)
                        inserted_count += 1
                    except Exception as e:
                        errors.append(f"Error inserting stop {stop_data.get('stop_name')}: {str(e)}")
            
            # Handle updates
            for record in data_to_update:
                try:
                    if category == 'buses' and record.get('duplicate_info'):
                        existing_id = record['duplicate_info']['existing_id']
                        bus = Bus.query.get(existing_id)
                        if bus:
                            bus.bus_type = record['data'].get('bus_type', bus.bus_type)
                            bus.capacity = int(record['data'].get('capacity', bus.capacity))
                            updated_count += 1
                    
                    elif category == 'routes' and record.get('duplicate_info'):
                        existing_id = record['duplicate_info']['existing_id']
                        route = Route.query.get(existing_id)
                        if route:
                            route.route_name = record['data'].get('route_name', route.route_name)
                            route.start_location = record['data'].get('start_location', route.start_location)
                            route.end_location = record['data'].get('end_location', route.end_location)
                            updated_count += 1
                except Exception as e:
                    errors.append(f"Error updating record: {str(e)}")
            
            # Commit all changes
            database.session.commit()
            logger.info(f"Database operation completed: {inserted_count} inserted, {updated_count} updated, {skipped_count} skipped")
            
        except Exception as e:
            database.session.rollback()
            logger.error(f"Database operation failed: {str(e)}")
            errors.append(f"Transaction failed: {str(e)}")
        
        return {
            'success': len(errors) == 0,
            'inserted': inserted_count,
            'updated': updated_count,
            'skipped': skipped_count,
            'errors': errors,
            'total_processed': inserted_count + updated_count + skipped_count
        }


def main():
    """
    Example usage of DataExtractor
    """
    # Initialize extractor
    extractor = DataExtractor()
    
    # Example: Analyze CSV file
    print("=== Analyzing CSV File ===")
    analysis = extractor.analyze_csv_structure('sample_buses.csv')
    print(f"Detected Category: {analysis['detected_category']}")
    print(f"Confidence: {analysis['matching_score']}%")
    print(f"Columns: {analysis['columns']}")
    
    # Example: Extract buses
    print("\n=== Extracting Buses ===")
    buses = extractor.extract_buses_from_csv('sample_buses.csv')
    print(f"Extracted {len(buses)} buses")
    
    # Example: Get validation report
    print("\n=== Validation Report ===")
    report = extractor.get_validation_report()
    print(f"Total Errors: {report['total_errors']}")
    print(f"Extracted Counts: {report['extracted_counts']}")
    
    # Example: Export to CSV
    print("\n=== Exporting Data ===")
    extractor.export_to_csv('buses', 'output_buses.csv')


if __name__ == '__main__':
    main()
