"""
Route Search Module
Handles route searching and recommendations
"""

from sqlalchemy import or_, and_
from app.models.database_models import Route, Stop, Bus, Booking

class RouteSearchHandler:
    """Handles route search operations"""
    
    @staticmethod
    def find_routes(source, destination, location_handler):
        """Find routes from database with fuzzy matching"""
        try:
            # Normalize locations
            source_match, source_score = location_handler.find_best_location_match(source)
            dest_match, dest_score = location_handler.find_best_location_match(destination)
            
            # Direct route search
            routes = Route.query.filter(
                and_(
                    or_(
                        Route.start_location.ilike(f'%{source_match}%'),
                        Route.route_name.ilike(f'%{source_match}%')
                    ),
                    or_(
                        Route.end_location.ilike(f'%{dest_match}%'),
                        Route.route_name.ilike(f'%{dest_match}%')
                    ),
                    Route.is_active == True
                )
            ).all()
            
            # If no direct routes, try finding routes through stops
            if not routes:
                routes = RouteSearchHandler.find_routes_via_stops(source_match, dest_match)
            
            return routes
        except:
            return []
    
    @staticmethod
    def find_routes_via_stops(source, destination):
        """Find routes that pass through source and destination as stops"""
        try:
            # Find routes that have both locations as stops
            source_stops = Stop.query.filter(Stop.stop_name.ilike(f'%{source}%')).all()
            dest_stops = Stop.query.filter(Stop.stop_name.ilike(f'%{destination}%')).all()
            
            source_route_ids = set([s.route_id for s in source_stops])
            dest_route_ids = set([s.route_id for s in dest_stops])
            
            common_route_ids = source_route_ids.intersection(dest_route_ids)
            
            if common_route_ids:
                routes = Route.query.filter(
                    and_(
                        Route.id.in_(common_route_ids),
                        Route.is_active == True
                    )
                ).all()
                return routes
            
            return []
        except:
            return []
    
    @staticmethod
    def find_all_routes_to_destination(destination):
        """Find ALL routes going to a specific destination"""
        try:
            # Search in end_location
            routes = Route.query.filter(
                and_(
                    Route.end_location.ilike(f'%{destination}%'),
                    Route.is_active == True
                )
            ).all()
            
            # Also search in route_name
            routes_by_name = Route.query.filter(
                and_(
                    Route.route_name.ilike(f'%{destination}%'),
                    Route.is_active == True
                )
            ).all()
            
            # Combine and remove duplicates
            all_routes = list(set(routes + routes_by_name))
            
            # Also check stops
            dest_stops = Stop.query.filter(Stop.stop_name.ilike(f'%{destination}%')).all()
            if dest_stops:
                stop_route_ids = set([s.route_id for s in dest_stops])
                stop_routes = Route.query.filter(
                    and_(
                        Route.id.in_(stop_route_ids),
                        Route.is_active == True
                    )
                ).all()
                all_routes.extend(stop_routes)
            
            return list(set(all_routes))
        except:
            return []
    
    @staticmethod
    def generate_recommendations(routes, source, destination):
        """Generate route recommendations"""
        if not routes:
            return {
                'message': f"No routes found\n\nFrom: {source}\nTo: {destination}",
                'type': 'text',
                'suggestions': ['Try Again', 'Help']
            }
        
        # Sort by fare
        sorted_routes = sorted(routes, key=lambda r: float(r.fare))[:10]
        
        msg = f"ROUTES: {source} → {destination}\n"
        msg += f"Found {len(routes)} route(s)\n\n"
        
        for idx, route in enumerate(sorted_routes, 1):
            bus = Bus.query.get(route.bus_id) if route.bus_id else None
            bus_num = bus.bus_number if bus else route.route_number
            bus_type = bus.bus_type if bus else 'Standard'
            
            msg += f"{idx}. Bus {bus_num} ({bus_type})\n"
            msg += f"   Fare: ₹{float(route.fare)}"
            
            if route.distance_km:
                msg += f" | {float(route.distance_km)} km"
            
            # Check popularity
            try:
                booking_count = Booking.query.filter_by(route_id=route.id).count()
                if booking_count >= 10:
                    msg += f" | Most Used"
                elif booking_count >= 5:
                    msg += f" | Popular"
            except:
                pass
            
            msg += "\n\n"
        
        return {
            'message': msg,
            'type': 'route_list',
            'routes': [{
                'route_number': r.route_number,
                'fare': float(r.fare),
                'distance': float(r.distance_km) if r.distance_km else None
            } for r in sorted_routes],
            'suggestions': ['Book Ticket', 'Cheapest Route', 'Fastest Route', 'New Search']
        }
    
    @staticmethod
    def generate_destination_based_recommendations(routes, destination):
        """Generate recommendations for destination-based search"""
        if not routes:
            return {
                'message': f"No routes found to {destination}",
                'type': 'text',
                'suggestions': ['Try Again', 'Help']
            }
        
        # Sort by fare
        sorted_routes = sorted(routes, key=lambda r: float(r.fare))[:10]
        
        msg = f"All Routes to {destination}\n"
        msg += f"Found {len(routes)} route(s)\n"
        msg += f"Showing top {len(sorted_routes)} routes\n\n"
        
        for idx, route in enumerate(sorted_routes, 1):
            bus = Bus.query.get(route.bus_id) if route.bus_id else None
            bus_num = bus.bus_number if bus else route.route_number
            bus_type = bus.bus_type if bus else 'Standard'
            
            msg += f"{idx}. {route.start_location} → {destination}\n"
            msg += f"   Bus {bus_num} ({bus_type})\n"
            msg += f"   Fare: ₹{float(route.fare)}"
            
            if route.distance_km:
                msg += f" | {float(route.distance_km)} km"
            
            # Check popularity
            try:
                booking_count = Booking.query.filter_by(route_id=route.id).count()
                if booking_count >= 10:
                    msg += f" | Most Used"
                elif booking_count >= 5:
                    msg += f" | Popular"
            except:
                pass
            
            msg += "\n\n"
        
        return {
            'message': msg,
            'type': 'destination_routes',
            'routes': [{
                'route_number': r.route_number,
                'start': r.start_location,
                'end': r.end_location,
                'fare': float(r.fare)
            } for r in sorted_routes],
            'suggestions': ['Book Ticket', 'New Search', 'Popular Routes']
        }
