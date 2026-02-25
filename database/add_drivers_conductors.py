"""
Script to add mock drivers and conductors data to the database
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.database_models import Driver, Conductor, Bus, Route
from datetime import datetime, date, timedelta
import random

app = create_app()

# Mock data
driver_names = [
    "Rajesh Kumar", "Amit Singh", "Suresh Sharma", "Vijay Verma", "Manoj Gupta",
    "Ravi Patel", "Sanjay Yadav", "Deepak Joshi", "Anil Chauhan", "Rakesh Mehta",
    "Ashok Kumar", "Ramesh Singh", "Dinesh Sharma", "Mukesh Verma", "Pankaj Gupta"
]

conductor_names = [
    "Priya Sharma", "Sunita Devi", "Kavita Singh", "Meena Kumari", "Rekha Patel",
    "Anita Yadav", "Geeta Joshi", "Savita Chauhan", "Neha Mehta", "Pooja Kumar",
    "Ritu Singh", "Anjali Sharma", "Seema Verma", "Nisha Gupta", "Asha Devi"
]

shifts = ["Morning", "Evening", "Night"]
statuses = ["Active", "Active", "Active", "Active", "On Leave"]  # 80% active

def add_drivers_and_conductors():
    """Add mock drivers and conductors with valid bus and route assignments"""
    with app.app_context():
        # Check if data already exists
        existing_drivers = Driver.query.count()
        existing_conductors = Conductor.query.count()
        
        if existing_drivers > 0 or existing_conductors > 0:
            print(f"Data already exists: {existing_drivers} drivers, {existing_conductors} conductors")
            response = input("Do you want to clear and re-add? (yes/no): ")
            if response.lower() != 'yes':
                print("Aborted.")
                return
            
            # Clear existing data
            Driver.query.delete()
            Conductor.query.delete()
            db.session.commit()
            print("Cleared existing data.")
        
        # Get all active buses and routes for assignment
        buses = Bus.query.filter_by(is_active=True).all()
        routes = Route.query.filter_by(is_active=True).all()
        
        if not buses or not routes:
            print("Error: No buses or routes found. Please add buses and routes first.")
            return
        
        print(f"Found {len(buses)} buses and {len(routes)} routes")
        
        # Create a mapping of routes to their assigned buses
        route_bus_map = {}
        for route in routes:
            if route.bus_id:
                route_bus_map[route.id] = route.bus_id
        
        # Get list of buses that have routes assigned
        buses_with_routes = list(set(route_bus_map.values()))
        available_buses = [b for b in buses if b.id in buses_with_routes]
        
        print(f"Found {len(available_buses)} buses with route assignments")
        
        # Add Drivers
        print("\nAdding drivers...")
        drivers_added = 0
        
        for i, name in enumerate(driver_names, 1):
            # Assign bus and matching route (80% get assignments)
            if random.random() > 0.2 and available_buses:
                assigned_bus = random.choice(available_buses)
                # Find a route that uses this bus
                matching_routes = [r for r in routes if r.bus_id == assigned_bus.id]
                assigned_route = random.choice(matching_routes) if matching_routes else None
            else:
                assigned_bus = None
                assigned_route = None
            
            driver = Driver(
                driver_id=f"DRV{str(i).zfill(4)}",
                full_name=name,
                phone=f"+91-98765{str(i).zfill(5)}",
                email=f"{name.lower().replace(' ', '.')}@yatrisetu.com",
                license_number=f"DL-{random.randint(10, 99)}-{random.randint(1000000000, 9999999999)}",
                license_expiry=date.today() + timedelta(days=random.randint(365, 1825)),
                date_of_birth=date.today() - timedelta(days=random.randint(10950, 18250)),  # 30-50 years
                address=f"{random.randint(1, 999)}, Sector-{random.randint(1, 50)}, Delhi",
                experience_years=random.randint(3, 20),
                assigned_bus_id=assigned_bus.id if assigned_bus else None,
                assigned_route_id=assigned_route.id if assigned_route else None,
                shift=random.choice(shifts),
                status=random.choice(statuses),
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            db.session.add(driver)
            drivers_added += 1
            assignment_info = f"Bus: {assigned_bus.bus_number}, Route: {assigned_route.route_number}" if assigned_bus and assigned_route else "No assignment"
            print(f"  Added: {name} (ID: DRV{str(i).zfill(4)}) - {driver.shift} shift - {driver.status} - {assignment_info}")
        
        # Add Conductors
        print("\nAdding conductors/ticket collectors...")
        conductors_added = 0
        
        for i, name in enumerate(conductor_names, 1):
            # Assign bus and matching route (80% get assignments)
            if random.random() > 0.2 and available_buses:
                assigned_bus = random.choice(available_buses)
                # Find a route that uses this bus
                matching_routes = [r for r in routes if r.bus_id == assigned_bus.id]
                assigned_route = random.choice(matching_routes) if matching_routes else None
            else:
                assigned_bus = None
                assigned_route = None
            
            role = "Conductor" if i <= 10 else "Ticket Collector"
            
            conductor = Conductor(
                conductor_id=f"CON{str(i).zfill(4)}",
                full_name=name,
                phone=f"+91-87654{str(i).zfill(5)}",
                email=f"{name.lower().replace(' ', '.')}@yatrisetu.com",
                employee_id=f"EMP{str(i + 100).zfill(4)}",
                date_of_birth=date.today() - timedelta(days=random.randint(8030, 14600)),  # 22-40 years
                address=f"{random.randint(1, 999)}, Block-{chr(65 + random.randint(0, 25))}, Delhi",
                experience_years=random.randint(1, 15),
                assigned_bus_id=assigned_bus.id if assigned_bus else None,
                assigned_route_id=assigned_route.id if assigned_route else None,
                shift=random.choice(shifts),
                role=role,
                status=random.choice(statuses),
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            db.session.add(conductor)
            conductors_added += 1
            assignment_info = f"Bus: {assigned_bus.bus_number}, Route: {assigned_route.route_number}" if assigned_bus and assigned_route else "No assignment"
            print(f"  Added: {name} (ID: CON{str(i).zfill(4)}) - {role} - {conductor.shift} shift - {conductor.status} - {assignment_info}")
        
        # Commit all changes
        db.session.commit()
        
        print(f"\n✅ Successfully added:")
        print(f"   - {drivers_added} drivers")
        print(f"   - {conductors_added} conductors/ticket collectors")
        print(f"\nTotal staff: {drivers_added + conductors_added}")
        
        # Show assignment statistics
        assigned_drivers = Driver.query.filter(Driver.assigned_bus_id.isnot(None)).count()
        assigned_conductors = Conductor.query.filter(Conductor.assigned_bus_id.isnot(None)).count()
        active_drivers = Driver.query.filter_by(status='Active').count()
        active_conductors = Conductor.query.filter_by(status='Active').count()
        
        print(f"\n📊 Statistics:")
        print(f"   Drivers:")
        print(f"     - Assigned to buses: {assigned_drivers}/{drivers_added}")
        print(f"     - Active: {active_drivers}/{drivers_added}")
        print(f"   Conductors:")
        print(f"     - Assigned to buses: {assigned_conductors}/{conductors_added}")
        print(f"     - Active: {active_conductors}/{conductors_added}")
        
        # Show shift distribution
        print(f"\n🕐 Shift Distribution:")
        for shift in shifts:
            driver_count = Driver.query.filter_by(shift=shift).count()
            conductor_count = Conductor.query.filter_by(shift=shift).count()
            print(f"   {shift}: {driver_count} drivers, {conductor_count} conductors")
        
        # Verify data integrity
        print(f"\n🔍 Data Integrity Check:")
        invalid_drivers = Driver.query.filter(
            Driver.assigned_bus_id.isnot(None),
            ~Driver.assigned_bus_id.in_([b.id for b in buses])
        ).count()
        invalid_conductors = Conductor.query.filter(
            Conductor.assigned_bus_id.isnot(None),
            ~Conductor.assigned_bus_id.in_([b.id for b in buses])
        ).count()
        
        if invalid_drivers == 0 and invalid_conductors == 0:
            print("   ✅ All assignments are valid!")
        else:
            print(f"   ⚠️ Found {invalid_drivers} invalid driver assignments")
            print(f"   ⚠️ Found {invalid_conductors} invalid conductor assignments")

if __name__ == '__main__':
    print("=" * 60)
    print("YatriSetu - Add Drivers & Conductors Mock Data")
    print("=" * 60)
    add_drivers_and_conductors()
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
