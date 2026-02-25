"""
YatriSetu Data Processing CLI Tool
Processes DTC PDF files and generates database-ready CSV files
"""

import sys
import os
import argparse
from datetime import datetime
from app.models.unified_data_processor import UnifiedDataProcessor


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Process DTC PDF files and generate database-ready CSV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process PDF and save to processed_data directory
  python process_dtc_data.py input.pdf processed_data
  
  # Process with specific category
  python process_dtc_data.py input.pdf output_dir --category routes
  
  # Show verbose output
  python process_dtc_data.py input.pdf output_dir --verbose
        """
    )
    
    parser.add_argument(
        'pdf_path',
        help='Path to the PDF file to process'
    )
    
    parser.add_argument(
        'output_dir',
        help='Directory to save processed CSV files'
    )
    
    parser.add_argument(
        '--category',
        choices=['routes', 'buses', 'stops', 'fares'],
        default='routes',
        help='Data category to extract (default: routes)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed processing information'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}")
        sys.exit(1)
    
    if not args.pdf_path.lower().endswith('.pdf'):
        print(f"Error: Input file must be a PDF: {args.pdf_path}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 70)
    print("YatriSetu Data Processing Tool")
    print("=" * 70)
    print(f"Input File: {args.pdf_path}")
    print(f"Output Directory: {args.output_dir}")
    print(f"Category: {args.category}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    # Initialize processor
    processor = UnifiedDataProcessor()
    
    # Process PDF
    print(f"Processing PDF file...")
    result = processor.process_pdf(args.pdf_path, category=args.category)
    
    if not result['success']:
        print(f"\nError: {result.get('error', 'Unknown error occurred')}")
        sys.exit(1)
    
    print(f"✓ PDF processing completed successfully")
    print()
    
    # Export data
    print("Exporting processed data to CSV files...")
    print()
    
    exported_files = []
    
    # Export routes
    if processor.get_all_data().get('routes'):
        routes_file = os.path.join(args.output_dir, 'routes_final.csv')
        processor.export_to_csv('routes', routes_file)
        exported_files.append(('routes', routes_file, len(processor.get_all_data()['routes'])))
        print(f"✓ Routes exported: {routes_file}")
    
    # Export stops
    if processor.get_all_data().get('stops'):
        stops_file = os.path.join(args.output_dir, 'stops_final.csv')
        processor.export_to_csv('stops', stops_file)
        exported_files.append(('stops', stops_file, len(processor.get_all_data()['stops'])))
        print(f"✓ Stops exported: {stops_file}")
    
    # Export fares
    if processor.get_all_data().get('fares'):
        fares_file = os.path.join(args.output_dir, 'fares_final.csv')
        processor.export_to_csv('fares', fares_file)
        exported_files.append(('fares', fares_file, len(processor.get_all_data()['fares'])))
        print(f"✓ Fares exported: {fares_file}")
    
    print()
    
    # Get validation report
    validation = processor.get_validation_report()
    
    # Display summary
    print("=" * 70)
    print("PROCESSING SUMMARY")
    print("=" * 70)
    print()
    
    print("Exported Files:")
    for category, filepath, count in exported_files:
        print(f"  • {category.capitalize()}: {count} records → {os.path.basename(filepath)}")
    print()
    
    print("Validation Results:")
    print(f"  • Total Errors: {validation.get('total_errors', 0)}")
    print(f"  • Total Warnings: {validation.get('total_warnings', 0)}")
    print(f"  • Status: {'✓ PASSED' if validation.get('total_errors', 0) == 0 else '✗ FAILED'}")
    print()
    
    if args.verbose and validation.get('errors'):
        print("Validation Errors:")
        for error in validation['errors'][:10]:  # Show first 10 errors
            print(f"  • {error}")
        if len(validation['errors']) > 10:
            print(f"  ... and {len(validation['errors']) - 10} more errors")
        print()
    
    print("=" * 70)
    print("Processing completed successfully!")
    print("=" * 70)
    print()
    print("Next Steps:")
    print("  1. Review generated CSV files in:", args.output_dir)
    print("  2. Import data via Admin Panel: http://localhost:5000/admin/data-import")
    print("  3. Or use direct PostgreSQL import (see processed_data/README.md)")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcessing interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        if '--verbose' in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
