"""
Clean and format extracted data for database import
"""

import pandas as pd
import re

def clean_route_data(input_csv, output_csv):
    """
    Clean and format route data
    """
    print("\n" + "="*60)
    print("Cleaning Extracted Data")
    print("="*60 + "\n")
    
    # Read CSV
    df = pd.read_csv(input_csv)
    
    print(f"Original records: {len(df)}")
    
    # Remove header rows and empty rows
    df = df[df['route_number'].notna()]
    df = df[~df['route_number'].isin(['AC Buses', 'Route No.'])]
    
    print(f"After removing headers: {len(df)}")
    
    # Clean and format data
    cleaned_data = []
    
    for idx, row in df.iterrows():
        # Extract route number (remove leading numbers if present)
        route_num = str(row['route_number']).strip()
        route_name = str(row['route_name']).strip()
        
        # Clean location names
        start_loc = str(row['start_location']).strip()
        end_loc = str(row['end_location']).strip()
        
        # Extract stops
        stops = str(row['distance']).strip() if pd.notna(row['distance']) else ''
        
        # Extract timings
        morning_time = str(row['column_6']).strip() if pd.notna(row['column_6']) else ''
        evening_time = str(row['column_7']).strip() if pd.notna(row['column_7']) else ''
        
        cleaned_row = {
            'route_number': route_name,  # DS-1, DS-2, etc.
            'route_name': f"{start_loc} to {end_loc}",
            'start_location': start_loc,
            'end_location': end_loc,
            'intermediate_stops': stops,
            'morning_departure': morning_time,
            'evening_departure': evening_time,
            'bus_type': 'AC',  # From PDF title
            'status': 'Active'
        }
        
        cleaned_data.append(cleaned_row)
    
    # Create cleaned DataFrame
    cleaned_df = pd.DataFrame(cleaned_data)
    
    # Save to CSV
    cleaned_df.to_csv(output_csv, index=False, encoding='utf-8')
    
    print(f"\nCleaned records: {len(cleaned_df)}")
    print(f"\nCleaned CSV created: {output_csv}")
    
    # Display sample
    print("\nSample cleaned data (first 10 rows):")
    print(cleaned_df.head(10).to_string())
    
    # Display statistics
    print("\n" + "="*60)
    print("Data Quality Report")
    print("="*60)
    print(f"Total routes: {len(cleaned_df)}")
    print(f"Unique route numbers: {cleaned_df['route_number'].nunique()}")
    print(f"Routes with start location: {cleaned_df['start_location'].notna().sum()}")
    print(f"Routes with end location: {cleaned_df['end_location'].notna().sum()}")
    print(f"Routes with morning departure: {(cleaned_df['morning_departure'] != '').sum()}")
    print(f"Routes with evening departure: {(cleaned_df['evening_departure'] != '').sum()}")
    
    return cleaned_df


def create_stops_csv(cleaned_routes_df, output_csv):
    """
    Create stops CSV from route data
    """
    print("\n" + "="*60)
    print("Creating Stops Data")
    print("="*60 + "\n")
    
    stops_data = []
    
    for idx, row in cleaned_routes_df.iterrows():
        route_num = row['route_number']
        
        # Add start location
        stops_data.append({
            'route_id': route_num,
            'stop_name': row['start_location'],
            'sequence': 1,
            'stop_type': 'Origin'
        })
        
        # Add intermediate stops
        if row['intermediate_stops'] and row['intermediate_stops'] != 'nan':
            intermediate = row['intermediate_stops'].split(',')
            for seq, stop in enumerate(intermediate, 2):
                stops_data.append({
                    'route_id': route_num,
                    'stop_name': stop.strip(),
                    'sequence': seq,
                    'stop_type': 'Intermediate'
                })
        
        # Add end location
        final_seq = len(stops_data) - stops_data.count({'route_id': route_num}) + 2
        stops_data.append({
            'route_id': route_num,
            'stop_name': row['end_location'],
            'sequence': final_seq,
            'stop_type': 'Destination'
        })
    
    # Create DataFrame
    stops_df = pd.DataFrame(stops_data)
    
    # Save to CSV
    stops_df.to_csv(output_csv, index=False, encoding='utf-8')
    
    print(f"Stops CSV created: {output_csv}")
    print(f"Total stops: {len(stops_df)}")
    print(f"Unique stops: {stops_df['stop_name'].nunique()}")
    
    # Display sample
    print("\nSample stops data (first 10 rows):")
    print(stops_df.head(10).to_string())
    
    return stops_df


def create_fares_csv(cleaned_routes_df, output_csv):
    """
    Create fares CSV with standard DTC fare structure
    """
    print("\n" + "="*60)
    print("Creating Fares Data")
    print("="*60 + "\n")
    
    # Standard DTC AC bus fares (example)
    fare_structure = {
        'General': 50,
        'Student': 25,
        'Senior Citizen': 30,
        'Differently Abled': 25,
        'Child': 20
    }
    
    fares_data = []
    
    for idx, row in cleaned_routes_df.iterrows():
        route_num = row['route_number']
        
        for passenger_type, fare in fare_structure.items():
            fares_data.append({
                'route_id': route_num,
                'passenger_type': passenger_type,
                'fare_amount': fare,
                'currency': 'INR',
                'effective_date': '2025-11-01'
            })
    
    # Create DataFrame
    fares_df = pd.DataFrame(fares_data)
    
    # Save to CSV
    fares_df.to_csv(output_csv, index=False, encoding='utf-8')
    
    print(f"Fares CSV created: {output_csv}")
    print(f"Total fare records: {len(fares_df)}")
    
    # Display sample
    print("\nSample fares data (first 10 rows):")
    print(fares_df.head(10).to_string())
    
    return fares_df


def main():
    """
    Main execution
    """
    print("\n" + "="*60)
    print("DTC Data Cleaning and Formatting")
    print("="*60)
    
    # Input and output paths
    input_csv = "extracted_data/routes_extracted.csv"
    
    # Clean routes data
    cleaned_routes_csv = "extracted_data/routes_cleaned.csv"
    cleaned_df = clean_route_data(input_csv, cleaned_routes_csv)
    
    # Create stops data
    stops_csv = "extracted_data/stops_cleaned.csv"
    stops_df = create_stops_csv(cleaned_df, stops_csv)
    
    # Create fares data
    fares_csv = "extracted_data/fares_cleaned.csv"
    fares_df = create_fares_csv(cleaned_df, fares_csv)
    
    # Final summary
    print("\n" + "="*60)
    print("Data Cleaning Complete!")
    print("="*60)
    print("\nGenerated Files:")
    print(f"  1. {cleaned_routes_csv} - {len(cleaned_df)} routes")
    print(f"  2. {stops_csv} - {len(stops_df)} stops")
    print(f"  3. {fares_csv} - {len(fares_df)} fare records")
    print("\nThese files are ready for import into the database!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
