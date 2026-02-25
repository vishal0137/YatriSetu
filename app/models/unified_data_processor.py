"""
Unified Data Processor for YatriSetu
Combines PDF extraction, data cleaning, validation, and database schema alignment
"""

import os
import re
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedDataProcessor:
    """
    Unified processor for extracting, cleaning, and preparing data for database import
    """
    
    def __init__(self, db_schema=None):
        """
        Initialize the unified processor
        
        Args:
            db_schema: Database schema configuration (optional)
        """
        self.db_schema = db_schema or self._get_default_schema()
        self.extracted_data = {
            'routes': [],
            'stops': [],
            'fares': [],
            'buses': []
        }
        self.validation_errors = []
        self.cleaning_log = []
        
    def _get_default_schema(self) -> Dict:
        """
        Get default database schema configuration
        """
        return {
            'routes': {
                'required_fields': ['route_number', 'route_name', 'start_location', 'end_location'],
                'optional_fields': ['distance', 'duration', 'bus_type', 'status', 'frequency'],
                'data_types': {
                    'route_number': 'string',
                    'route_name': 'string',
                    'start_location': 'string',
                    'end_location': 'string',
                    'distance': 'float',
                    'duration': 'integer',
                    'bus_type': 'string',
                    'status': 'string',
                    'frequency': 'integer'
                },
                'defaults': {
                    'bus_type': 'Regular',
                    'status': 'Active',
                    'frequency': 30
                }
            },
            'stops': {
                'required_fields': ['route_id', 'stop_name', 'sequence'],
                'optional_fields': ['latitude', 'longitude', 'stop_type', 'arrival_time'],
                'data_types': {
                    'route_id': 'string',
                    'stop_name': 'string',
                    'sequence': 'integer',
                    'latitude': 'float',
                    'longitude': 'float',
                    'stop_type': 'string',
                    'arrival_time': 'string'
                },
                'defaults': {
                    'stop_type': 'Regular'
                }
            },
            'fares': {
                'required_fields': ['route_id', 'passenger_type', 'fare_amount'],
                'optional_fields': ['currency', 'effective_date', 'distance_range'],
                'data_types': {
                    'route_id': 'string',
                    'passenger_type': 'string',
                    'fare_amount': 'float',
                    'currency': 'string',
                    'effective_date': 'date',
                    'distance_range': 'string'
                },
                'defaults': {
                    'currency': 'INR',
                    'effective_date': datetime.now().strftime('%Y-%m-%d')
                }
            },
            'buses': {
                'required_fields': ['bus_number', 'bus_type'],
                'optional_fields': ['capacity', 'status', 'manufacturer', 'model', 'year'],
                'data_types': {
                    'bus_number': 'string',
                    'bus_type': 'string',
                    'capacity': 'integer',
                    'status': 'string',
                    'manufacturer': 'string',
                    'model': 'string',
                    'year': 'integer'
                },
                'defaults': {
                    'status': 'Active',
                    'capacity': 50
                }
            }
        }
    
    def process_pdf(self, pdf_path: str, category: str = 'auto') -> Dict:
        """
        Complete PDF processing pipeline: extract, clean, validate, and format
        
        Args:
            pdf_path: Path to PDF file
            category: Data category (auto, routes, stops, fares, buses)
            
        Returns:
            Dictionary with processed data
        """
        logger.info(f"Starting unified processing for: {pdf_path}")
        
        # Step 1: Extract tables from PDF
        tables = self._extract_pdf_tables(pdf_path)
        
        if not tables:
            logger.error("No tables extracted from PDF")
            return {'success': False, 'error': 'No tables found in PDF'}
        
        # Step 2: Detect category if auto
        if category == 'auto':
            category = self._detect_category(tables)
            logger.info(f"Auto-detected category: {category}")
        
        # Step 3: Parse and clean data
        raw_data = self._parse_tables(tables, category)
        
        # Step 4: Clean and normalize data
        cleaned_data = self._clean_data(raw_data, category)
        
        # Step 5: Align with database schema
        aligned_data = self._align_with_schema(cleaned_data, category)
        
        # Step 6: Validate data
        validation_result = self._validate_data(aligned_data, category)
        
        # Step 7: Generate related data (e.g., stops from routes)
        if category == 'routes':
            self._generate_stops_from_routes(aligned_data)
            self._generate_fares_from_routes(aligned_data)
        
        return {
            'success': True,
            'category': category,
            'data': aligned_data,
            'validation': validation_result,
            'cleaning_log': self.cleaning_log,
            'statistics': self._generate_statistics(aligned_data, category)
        }
    
    def _extract_pdf_tables(self, pdf_path: str) -> List[Dict]:
        """
        Extract tables from PDF file
        """
        try:
            import pdfplumber
            
            tables = []
            
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_tables = page.extract_tables()
                    
                    if page_tables:
                        for table_idx, table in enumerate(page_tables, 1):
                            if table and len(table) > 0:
                                tables.append({
                                    'page': page_num,
                                    'table_number': table_idx,
                                    'data': table,
                                    'rows': len(table),
                                    'columns': len(table[0]) if table[0] else 0
                                })
            
            logger.info(f"Extracted {len(tables)} tables from PDF")
            return tables
            
        except ImportError:
            logger.error("pdfplumber not installed")
            return []
        except Exception as e:
            logger.error(f"Error extracting PDF: {str(e)}")
            return []
    
    def _detect_category(self, tables: List[Dict]) -> str:
        """
        Detect data category from table structure
        """
        # Analyze first table header
        if tables and tables[0]['data']:
            header = tables[0]['data'][0] if tables[0]['data'] else []
            header_text = ' '.join([str(h).lower() for h in header if h])
            
            # Detection keywords
            if any(word in header_text for word in ['route', 'origin', 'destination']):
                return 'routes'
            elif any(word in header_text for word in ['stop', 'station', 'halt']):
                return 'stops'
            elif any(word in header_text for word in ['fare', 'price', 'cost', 'passenger']):
                return 'fares'
            elif any(word in header_text for word in ['bus', 'vehicle', 'fleet']):
                return 'buses'
        
        return 'routes'  # Default
    
    def _parse_tables(self, tables: List[Dict], category: str) -> List[Dict]:
        """
        Parse tables based on category
        """
        parsed_data = []
        
        for table_info in tables:
            table = table_info['data']
            
            if not table or len(table) < 2:
                continue
            
            # Skip header row
            for row_idx, row in enumerate(table[1:], 1):
                if not row or all(cell is None or str(cell).strip() == '' for cell in row):
                    continue
                
                # Clean row data
                cleaned_row = [self._clean_text(cell) for cell in row]
                
                parsed_data.append({
                    'page': table_info['page'],
                    'row': row_idx,
                    'data': cleaned_row
                })
        
        logger.info(f"Parsed {len(parsed_data)} rows from tables")
        return parsed_data
    
    def _clean_text(self, text) -> Optional[str]:
        """
        Clean text data
        """
        if text is None or text == '':
            return None
        
        text = str(text).strip()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\-.,():/]', '', text)
        
        return text if text else None
    
    def _clean_data(self, raw_data: List[Dict], category: str) -> List[Dict]:
        """
        Clean and normalize data based on category
        """
        cleaned = []
        
        for item in raw_data:
            row_data = item['data']
            
            if category == 'routes':
                cleaned_item = self._clean_route_row(row_data, item)
            elif category == 'stops':
                cleaned_item = self._clean_stop_row(row_data, item)
            elif category == 'fares':
                cleaned_item = self._clean_fare_row(row_data, item)
            elif category == 'buses':
                cleaned_item = self._clean_bus_row(row_data, item)
            else:
                cleaned_item = None
            
            if cleaned_item:
                cleaned.append(cleaned_item)
        
        self.cleaning_log.append(f"Cleaned {len(cleaned)} {category} records")
        return cleaned
    
    def _clean_route_row(self, row: List, metadata: Dict) -> Optional[Dict]:
        """
        Clean route data row
        """
        def get_val(idx, default=''):
            return row[idx] if idx < len(row) and row[idx] else default
        
        # Extract route information
        route_data = {
            'route_number': get_val(1),  # Usually second column
            'route_name': f"{get_val(2)} to {get_val(3)}",
            'start_location': get_val(2),
            'end_location': get_val(3),
            'intermediate_stops': get_val(4),
            'morning_departure': get_val(5),
            'evening_departure': get_val(6),
            '_source_page': metadata['page'],
            '_source_row': metadata['row']
        }
        
        # Skip if no route number
        if not route_data['route_number']:
            return None
        
        return route_data
    
    def _clean_stop_row(self, row: List, metadata: Dict) -> Optional[Dict]:
        """
        Clean stop data row
        """
        def get_val(idx, default=''):
            return row[idx] if idx < len(row) and row[idx] else default
        
        stop_data = {
            'route_id': get_val(0),
            'stop_name': get_val(1),
            'sequence': get_val(2),
            'latitude': get_val(3),
            'longitude': get_val(4),
            '_source_page': metadata['page'],
            '_source_row': metadata['row']
        }
        
        if not stop_data['stop_name']:
            return None
        
        return stop_data
    
    def _clean_fare_row(self, row: List, metadata: Dict) -> Optional[Dict]:
        """
        Clean fare data row
        """
        def get_val(idx, default=''):
            return row[idx] if idx < len(row) and row[idx] else default
        
        fare_data = {
            'route_id': get_val(0),
            'passenger_type': get_val(1),
            'fare_amount': get_val(2),
            'distance_range': get_val(3),
            '_source_page': metadata['page'],
            '_source_row': metadata['row']
        }
        
        if not fare_data['route_id'] or not fare_data['fare_amount']:
            return None
        
        return fare_data
    
    def _clean_bus_row(self, row: List, metadata: Dict) -> Optional[Dict]:
        """
        Clean bus data row
        """
        def get_val(idx, default=''):
            return row[idx] if idx < len(row) and row[idx] else default
        
        bus_data = {
            'bus_number': get_val(0),
            'bus_type': get_val(1),
            'capacity': get_val(2),
            'status': get_val(3),
            'manufacturer': get_val(4),
            'model': get_val(5),
            '_source_page': metadata['page'],
            '_source_row': metadata['row']
        }
        
        if not bus_data['bus_number']:
            return None
        
        return bus_data
    
    def _align_with_schema(self, data: List[Dict], category: str) -> List[Dict]:
        """
        Align data with database schema
        """
        schema = self.db_schema.get(category, {})
        required_fields = schema.get('required_fields', [])
        optional_fields = schema.get('optional_fields', [])
        defaults = schema.get('defaults', {})
        data_types = schema.get('data_types', {})
        
        aligned = []
        
        for item in data:
            aligned_item = {}
            
            # Add required fields
            for field in required_fields:
                value = item.get(field)
                
                # Apply defaults if missing
                if value is None or value == '':
                    value = defaults.get(field)
                
                # Convert data type
                if value is not None:
                    value = self._convert_type(value, data_types.get(field, 'string'))
                
                aligned_item[field] = value
            
            # Add optional fields
            for field in optional_fields:
                value = item.get(field)
                
                if value is None or value == '':
                    value = defaults.get(field)
                
                if value is not None:
                    value = self._convert_type(value, data_types.get(field, 'string'))
                
                aligned_item[field] = value
            
            aligned.append(aligned_item)
        
        # Store aligned data
        if category == 'routes':
            self.extracted_data['routes'] = aligned
        elif category == 'stops':
            self.extracted_data['stops'] = aligned
        elif category == 'fares':
            self.extracted_data['fares'] = aligned
        elif category == 'buses':
            self.extracted_data['buses'] = aligned
        
        self.cleaning_log.append(f"Aligned {len(aligned)} records with schema")
        return aligned
    
    def _convert_type(self, value, target_type: str):
        """
        Convert value to target data type
        """
        try:
            if target_type == 'integer':
                return int(float(str(value)))
            elif target_type == 'float':
                return float(str(value))
            elif target_type == 'string':
                return str(value).strip()
            elif target_type == 'date':
                return str(value)
            else:
                return value
        except (ValueError, TypeError):
            return None
    
    def _validate_data(self, data: List[Dict], category: str) -> Dict:
        """
        Validate data against schema rules
        """
        schema = self.db_schema.get(category, {})
        required_fields = schema.get('required_fields', [])
        
        errors = []
        warnings = []
        
        for idx, item in enumerate(data, 1):
            # Check required fields
            for field in required_fields:
                if field not in item or item[field] is None or item[field] == '':
                    errors.append(f"Row {idx}: Missing required field '{field}'")
            
            # Category-specific validation
            if category == 'routes':
                if item.get('start_location') == item.get('end_location'):
                    warnings.append(f"Row {idx}: Start and end locations are the same")
            
            elif category == 'fares':
                fare = item.get('fare_amount')
                if fare is not None and fare < 0:
                    errors.append(f"Row {idx}: Fare amount cannot be negative")
            
            elif category == 'stops':
                seq = item.get('sequence')
                if seq is not None and seq < 1:
                    errors.append(f"Row {idx}: Sequence must be positive")
        
        self.validation_errors = errors
        
        return {
            'is_valid': len(errors) == 0,
            'total_errors': len(errors),
            'total_warnings': len(warnings),
            'errors': errors,
            'warnings': warnings
        }
    
    def _generate_stops_from_routes(self, routes: List[Dict]):
        """
        Generate stops data from routes
        """
        stops = []
        
        for route in routes:
            route_id = route.get('route_number')
            
            # Add origin
            stops.append({
                'route_id': route_id,
                'stop_name': route.get('start_location'),
                'sequence': 1,
                'stop_type': 'Origin'
            })
            
            # Add intermediate stops
            intermediate = route.get('intermediate_stops', '')
            if intermediate:
                intermediate_list = [s.strip() for s in intermediate.split(',')]
                for seq, stop in enumerate(intermediate_list, 2):
                    if stop:
                        stops.append({
                            'route_id': route_id,
                            'stop_name': stop,
                            'sequence': seq,
                            'stop_type': 'Intermediate'
                        })
            
            # Add destination
            final_seq = len([s for s in stops if s['route_id'] == route_id]) + 1
            stops.append({
                'route_id': route_id,
                'stop_name': route.get('end_location'),
                'sequence': final_seq,
                'stop_type': 'Destination'
            })
        
        self.extracted_data['stops'] = stops
        logger.info(f"Generated {len(stops)} stops from routes")
    
    def _generate_fares_from_routes(self, routes: List[Dict]):
        """
        Generate fares data from routes
        """
        # Standard fare structure
        fare_structure = {
            'General': 50,
            'Student': 25,
            'Senior Citizen': 30,
            'Differently Abled': 25,
            'Child': 20
        }
        
        fares = []
        
        for route in routes:
            route_id = route.get('route_number')
            bus_type = route.get('bus_type', 'Regular')
            
            # Adjust fares for AC buses
            multiplier = 1.5 if bus_type == 'AC' else 1.0
            
            for passenger_type, base_fare in fare_structure.items():
                fares.append({
                    'route_id': route_id,
                    'passenger_type': passenger_type,
                    'fare_amount': int(base_fare * multiplier),
                    'currency': 'INR',
                    'effective_date': datetime.now().strftime('%Y-%m-%d')
                })
        
        self.extracted_data['fares'] = fares
        logger.info(f"Generated {len(fares)} fare records from routes")
    
    def _generate_statistics(self, data: List[Dict], category: str) -> Dict:
        """
        Generate statistics for processed data
        """
        stats = {
            'total_records': len(data),
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
        
        if category == 'routes':
            stats['unique_routes'] = len(set(r.get('route_number') for r in data))
            stats['unique_origins'] = len(set(r.get('start_location') for r in data))
            stats['unique_destinations'] = len(set(r.get('end_location') for r in data))
        
        elif category == 'stops':
            stats['unique_stops'] = len(set(s.get('stop_name') for s in data))
            stats['unique_routes'] = len(set(s.get('route_id') for s in data))
        
        elif category == 'fares':
            stats['unique_routes'] = len(set(f.get('route_id') for f in data))
            stats['passenger_types'] = len(set(f.get('passenger_type') for f in data))
        
        return stats
    
    def export_to_csv(self, category: str, output_path: str):
        """
        Export processed data to CSV
        """
        if category == 'routes':
            data = self.extracted_data.get('routes', [])
        elif category == 'stops':
            data = self.extracted_data.get('stops', [])
        elif category == 'fares':
            data = self.extracted_data.get('fares', [])
        else:
            data = []
        
        if not data:
            logger.warning(f"No data to export for category: {category}")
            return
        
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False, encoding='utf-8')
        logger.info(f"Exported {len(data)} records to {output_path}")
    
    def get_all_data(self) -> Dict:
        """
        Get all extracted and generated data
        """
        return {
            'routes': self.extracted_data.get('routes', []),
            'stops': self.extracted_data.get('stops', []),
            'fares': self.extracted_data.get('fares', []),
            'buses': self.extracted_data.get('buses', [])
        }


def main():
    """
    Example usage
    """
    processor = UnifiedDataProcessor()
    
    # Process PDF file
    pdf_path = r"C:\Project\YatriSetu_Prototype\destination_bus_services_nov_2025_1_0.pdf"
    
    result = processor.process_pdf(pdf_path, category='routes')
    
    if result['success']:
        print(f"\nProcessing successful!")
        print(f"Category: {result['category']}")
        print(f"Records: {result['statistics']['total_records']}")
        print(f"Validation: {'Passed' if result['validation']['is_valid'] else 'Failed'}")
        
        # Export data
        processor.export_to_csv('routes', 'output_routes.csv')
        processor.export_to_csv('stops', 'output_stops.csv')
        processor.export_to_csv('fares', 'output_fares.csv')
    else:
        print(f"Processing failed: {result.get('error')}")


if __name__ == '__main__':
    main()
