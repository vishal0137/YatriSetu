"""
Update route fares to be in increments of 5, 10, 15, 25, 35, 45, etc.
Based on distance ranges
"""

from app import create_app, db
from app.models import Route

def update_fares():
    """Update all route fares based on distance"""
    app = create_app()
    
    with app.app_context():
        print("="*70)
        print("UPDATING ROUTE FARES")
        print("="*70)
        
        # Get all active routes
        routes = Route.query.filter_by(is_active=True).all()
        
        print(f"\nFound {len(routes)} active routes")
        print("\nUpdating fares based on distance...")
        
        updated_count = 0
        
        for route in routes:
            distance = float(route.distance_km) if route.distance_km else 0
            old_fare = float(route.fare)
            
            # Determine new fare based on distance
            if distance <= 5:
                new_fare = 5.00
            elif distance <= 10:
                new_fare = 10.00
            elif distance <= 15:
                new_fare = 15.00
            elif distance <= 20:
                new_fare = 20.00
            elif distance <= 25:
                new_fare = 25.00
            elif distance <= 30:
                new_fare = 30.00
            elif distance <= 35:
                new_fare = 35.00
            elif distance <= 40:
                new_fare = 40.00
            elif distance <= 45:
                new_fare = 45.00
            elif distance <= 50:
                new_fare = 50.00
            else:
                new_fare = 55.00
            
            # Update if different
            if old_fare != new_fare:
                route.fare = new_fare
                updated_count += 1
                print(f"  Route {route.route_number}: {distance:.2f} km - ₹{old_fare} → ₹{new_fare}")
        
        # Commit changes
        db.session.commit()
        
        print(f"\n✅ Updated {updated_count} routes")
        
        # Show summary
        print("\n" + "="*70)
        print("FARE SUMMARY BY DISTANCE RANGE")
        print("="*70)
        
        ranges = [
            (0, 5, "0-5 km", 5),
            (5, 10, "5-10 km", 10),
            (10, 15, "10-15 km", 15),
            (15, 20, "15-20 km", 20),
            (20, 25, "20-25 km", 25),
            (25, 30, "25-30 km", 30),
            (30, 35, "30-35 km", 35),
            (35, 40, "35-40 km", 40),
            (40, 45, "40-45 km", 45),
            (45, 50, "45-50 km", 50),
            (50, 999, "50+ km", 55)
        ]
        
        for min_dist, max_dist, label, expected_fare in ranges:
            count = Route.query.filter(
                Route.is_active == True,
                Route.distance_km > min_dist,
                Route.distance_km <= max_dist
            ).count()
            
            if count > 0:
                print(f"{label:12} - ₹{expected_fare:2} - {count:3} routes")
        
        print("\n" + "="*70)
        print("FARE UPDATE COMPLETE")
        print("="*70)

if __name__ == "__main__":
    update_fares()
