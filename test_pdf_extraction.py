"""
Test script to extract data from DTC PDF file
Extracts bus services data and generates clean CSV files
"""

import sys
import os
import pandas as pd
import re
from datetime import datetime

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from data_extractor import DataExtractor


def extract_pdf_tables(pdf_path):
    """
    Extract tables from PDF file
    """
    try:
        import pdfplumber
        
        print(f"\n{'='*60}")
        print(f"Extracting data from: {pdf_path}")
        print(f"{'='*60}\n")
        
        all_tables = []
        
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Total pages: {len(pdf.pages)}\n")
            
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"Processing page {page_num}...")
                
                # Extract tables
                tables = page.extract_tables()
                
                if tables:
                    print(f"  Found {len(tables)} table(s)")
                    for table_idx, table in enumerate(tables, 1):
                        if table and len(table) > 0:
                            print(f"    Table {table_idx}: {len(table)} rows x {len(table[0]) if table[0] else 0} columns")
                            all_tables.append({
                                'page': page_num,
                                'table_number': table_idx,
                                'data': table
                            })
                else:
                    print(f"  No tables found")
        
        print(f"\nTotal tables extracted: {len(all_tables)}\n")
        return all_tables
        
    except ImportError:
        print("Error: pdfplumber not installed")
        print("Install with: pip install pdfplumber")
        return []
    except Exception as e:
        print(f"Error extracting PDF: {str(e)}")
        return []


def clean_text(text):
    """
    Clean text data
    """
    if text is None or text == '':
        return None
    
    # Convert to string
    text = str(text).strip()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep alphanumeric, spaces, and common punctuation
    text = re.sub(r'[^\w\s\-.,():/]', '', text)
    
    return text if text else None


def parse_route_data(tables):
    """
    Parse route data from extracted tables
    """
    routes = []
    stops_data = []
    
    for table_info in tables:
        table = table_info['data']
        page = table_info['page']
        
        if not table or len(table) < 2:
            continue
        
        # Try to identify table structure
        header = table[0] if table else []
        
        print(f"\nAnalyzing table from page {page}:")
        print(f"Header: {header}")
        
        # Process each row
        for row_idx, row in enumerate(table[1:], 1):
            if not row or all(cell is None or str(cell).strip() == '' for cell in row):
                continue
            
            # Clean row data
            cleaned_row = [clean_text(cell) for cell in row]
            
            # Try to extract route information
            # Assuming format: Route Number, Route Name, Start, End, Distance, etc.
            if len(cleaned_row) >= 2:
                route_data = {
                    'page': page,
                    'row': row_idx,
                    'raw_data': cleaned_row
                }
                
                # Try to identify route number (usually starts with number or contains 'Route')
                for idx, cell in enumerate(cleaned_row):
                    if cell and (cell.isdigit() or 'route' in cell.lower()):
                        route_data['route_number'] = cell
                        break
                
                routes.append(route_data)
    
    return routes, stops_data


def create_routes_csv(routes, output_path):
    """
    Create routes CSV file
    """
    if not routes:
        print("No route data to export")
        return
    
    # Prepare data for CSV
    csv_data = []
    
    for route in routes:
        raw = route.get('raw_data', [])
        
        # Helper function to safely get value
        def get_value(lst, idx, default=''):
            if idx < len(lst) and lst[idx] is not None:
                return str(lst[idx]).strip()
            return default
        
        # Extract fields based on position
        row_data = {
            'route_number': route.get('route_number', get_value(raw, 0)),
            'route_name': get_value(raw, 1),
            'start_location': get_value(raw, 2),
            'end_location': get_value(raw, 3),
            'distance': get_value(raw, 4),
            'column_6': get_value(raw, 5),
            'column_7': get_value(raw, 6),
            'source_page': route.get('page', ''),
            'source_row': route.get('row', '')
        }
        
        csv_data.append(row_data)
    
    # Create DataFrame
    df = pd.DataFrame(csv_data)
    
    # Save to CSV
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nRoutes CSV created: {output_path}")
    print(f"Total records: {len(df)}")
    
    # Display sample
    print("\nSample data (first 5 rows):")
    print(df.head().to_string())
    
    # Display statistics
    print("\nData Statistics:")
    print(f"  - Non-empty route numbers: {df['route_number'].notna().sum()}")
    print(f"  - Non-empty route names: {df['route_name'].notna().sum()}")
    print(f"  - Non-empty start locations: {df['start_location'].notna().sum()}")
    print(f"  - Non-empty end locations: {df['end_location'].notna().sum()}")
    
    return df


def create_summary_report(tables, routes, output_dir):
    """
    Create summary report
    """
    report_path = os.path.join(output_dir, 'extraction_report.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("PDF Data Extraction Report\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Source File: destination_bus_services_nov_2025_1_0.pdf\n\n")
        
        f.write("Extraction Summary:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total tables extracted: {len(tables)}\n")
        f.write(f"Total route records: {len(routes)}\n\n")
        
        f.write("Table Distribution by Page:\n")
        f.write("-" * 40 + "\n")
        page_counts = {}
        for table in tables:
            page = table['page']
            page_counts[page] = page_counts.get(page, 0) + 1
        
        for page, count in sorted(page_counts.items()):
            f.write(f"Page {page}: {count} table(s)\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("Data Quality Notes:\n")
        f.write("="*60 + "\n")
        f.write("- Review extracted data for accuracy\n")
        f.write("- Verify route numbers and names\n")
        f.write("- Check location names for consistency\n")
        f.write("- Validate distance values\n")
        f.write("- Clean any special characters or formatting issues\n")
    
    print(f"\nSummary report created: {report_path}")


def main():
    """
    Main execution function
    """
    # PDF file path
    pdf_path = r"C:\Project\YatriSetu_Prototype\destination_bus_services_nov_2025_1_0.pdf"
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return
    
    # Create output directory
    output_dir = "extracted_data"
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*60)
    print("DTC Bus Services Data Extraction")
    print("="*60)
    
    # Step 1: Extract tables from PDF
    print("\nStep 1: Extracting tables from PDF...")
    tables = extract_pdf_tables(pdf_path)
    
    if not tables:
        print("No tables extracted. Exiting.")
        return
    
    # Step 2: Parse route data
    print("\nStep 2: Parsing route data...")
    routes, stops = parse_route_data(tables)
    print(f"Parsed {len(routes)} route records")
    
    # Step 3: Create CSV files
    print("\nStep 3: Creating CSV files...")
    
    # Routes CSV
    routes_csv = os.path.join(output_dir, "routes_extracted.csv")
    routes_df = create_routes_csv(routes, routes_csv)
    
    # Step 4: Create raw data dump for manual review
    print("\nStep 4: Creating raw data dump...")
    raw_data_path = os.path.join(output_dir, "raw_tables_data.txt")
    with open(raw_data_path, 'w', encoding='utf-8') as f:
        for table_info in tables:
            f.write(f"\n{'='*60}\n")
            f.write(f"Page {table_info['page']} - Table {table_info['table_number']}\n")
            f.write(f"{'='*60}\n\n")
            
            for row_idx, row in enumerate(table_info['data']):
                f.write(f"Row {row_idx}: {row}\n")
    
    print(f"Raw data dump created: {raw_data_path}")
    
    # Step 5: Create summary report
    print("\nStep 5: Creating summary report...")
    create_summary_report(tables, routes, output_dir)
    
    # Final summary
    print("\n" + "="*60)
    print("Extraction Complete!")
    print("="*60)
    print(f"\nOutput files created in: {output_dir}/")
    print(f"  - routes_extracted.csv (cleaned route data)")
    print(f"  - raw_tables_data.txt (raw extracted data)")
    print(f"  - extraction_report.txt (summary report)")
    print("\nNext steps:")
    print("1. Review the CSV file for data accuracy")
    print("2. Clean any inconsistencies manually if needed")
    print("3. Use the Data Import feature in admin panel to import")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
