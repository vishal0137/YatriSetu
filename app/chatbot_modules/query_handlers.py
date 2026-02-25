"""
Query Handlers Module
Handles specific query types (fare, booking, AC bus, etc.)
"""

import re
from app.models.database_models import Route, Bus, Booking
from .algorithms import PathfindingAlgorithms

class QueryHandlers:
    """Handles specific query types"""
    
    def __init__(self, location_handler, route_search):
        self.location_handler = location_handler
        self.route_search = route_search
    
    def handle_fare_query(self, user_id, message_lower, original_message):
        """Handle fare inquiry"""
        locations = self.location_handler.extract_locations_from_message(original_message)
        
        if len(locations) >= 2:
            source_match, _ = self.location_handler.find_best_location_match(locations[0])
            dest_match, _ = self.location_handler.find_best_location_match(locations[1])
            
            routes = self.route_search.find_routes(locations[0], locations[1], self.location_handler)
            if routes:
                cheapest = min(routes, key=lambda r: float(r.fare))
                most_expensive = max(routes, key=lambda r: float(r.fare))
                fare_min = float(cheapest.fare)
                fare_max = float(most_expensive.fare)
                
                msg = f"FARE: {source_match} → {dest_match}\n\n"
                
                if fare_min == fare_max:
                    msg += f"Route: {cheapest.route_number}\n"
                    if cheapest.distance_km:
                        msg += f"Distance: {float(cheapest.distance_km)} km\n\n"
                    msg += f"• General: ₹{int(fare_min)}\n"
                    msg += f"• Student: ₹{int(fare_min * 0.5)}\n"
                    msg += f"• Senior: ₹{int(fare_min * 0.5)}\n"
                    msg += f"• Disabled: Free"
                else:
                    msg += f"Fare Range: ₹{int(fare_min)} - ₹{int(fare_max)}\n"
                    msg += f"Routes available: {len(routes)}\n\n"
                    msg += f"• General: ₹{int(fare_min)} - ₹{int(fare_max)}\n"
                    msg += f"• Student: ₹{int(fare_min * 0.5)} - ₹{int(fare_max * 0.5)}\n"
                    msg += f"• Senior: ₹{int(fare_min * 0.5)} - ₹{int(fare_max * 0.5)}\n"
                    msg += f"• Disabled: Free"
                
                return {
                    'message': msg,
                    'type': 'text',
                    'suggestions': ['Book Ticket', 'View Routes', 'New Search']
                }
            else:
                return {
                    'message': f"No routes found\n\nFrom: {source_match}\nTo: {dest_match}",
                    'type': 'text',
                    'suggestions': self.location_handler.get_popular_destinations()[:4]
                }
        elif len(locations) == 1:
            # Only destination provided, ask for source
            dest_match, _ = self.location_handler.find_best_location_match(locations[0])
            return {
                'message': f"To check fare to {dest_match}\n\nWhere are you starting from?",
                'type': 'text',
                'suggestions': self.location_handler.get_popular_destinations()[:4]
            }
        
        return {
            'message': "Check fare between locations\n\nExample:\n• 'Fare from CP to Dwarka'\n• 'How much from CP to Airport'",
            'type': 'text',
            'suggestions': ['Find Route', 'Help']
        }
    
    def handle_booking_intent(self, user_id, user_context):
        """Handle booking"""
        context = user_context.get(user_id, {})
        
        if context.get('source') and context.get('destination'):
            routes = self.route_search.find_routes(context['source'], context['destination'], self.location_handler)
            if routes:
                cheapest = min(routes, key=lambda r: float(r.fare))
                return {
                    'message': f"BOOKING\n\n"
                              f"From: {context['source']}\n"
                              f"To: {context['destination']}\n"
                              f"Fare: ₹{float(cheapest.fare)}\n\n"
                              f"Select category:",
                    'type': 'booking',
                    'suggestions': ['General', 'Student', 'Senior', 'Disabled']
                }
        
        return {
            'message': "To book, tell me your journey details first",
            'type': 'text',
            'suggestions': ['Find Route']
        }
    
    def handle_cheapest_route_query(self, user_id, message_lower, original_message):
        """Handle cheapest route queries using Greedy algorithm"""
        locations = self.location_handler.extract_locations_from_message(original_message)
        
        if len(locations) >= 2:
            source_match, _ = self.location_handler.find_best_location_match(locations[0])
            dest_match, _ = self.location_handler.find_best_location_match(locations[1])
            
            # Use Greedy algorithm for minimum fare
            cheapest_route, total_fare, path = PathfindingAlgorithms.greedy_minimum_fare(source_match, dest_match)
            
            if cheapest_route:
                bus = Bus.query.get(cheapest_route.bus_id) if cheapest_route.bus_id else None
                path_str = " → ".join(path) if len(path) > 2 else f"{source_match} → {dest_match}"
                
                return {
                    'message': f"CHEAPEST ROUTE (Greedy Algorithm)\n\n"
                              f"From: {source_match}\n"
                              f"To: {dest_match}\n\n"
                              f"Bus: {bus.bus_number if bus else cheapest_route.route_number}\n"
                              f"Type: {bus.bus_type if bus else 'Standard'}\n"
                              f"Total Fare: ₹{total_fare:.2f}\n"
                              f"Distance: {float(cheapest_route.distance_km) if cheapest_route.distance_km else 'N/A'} km\n"
                              f"Path: {path_str}",
                    'type': 'text',
                    'suggestions': ['Book Ticket', 'Shortest Path', 'New Search']
                }
            else:
                # Fallback to simple search
                routes = self.route_search.find_routes(locations[0], locations[1], self.location_handler)
                if routes:
                    cheapest = min(routes, key=lambda r: float(r.fare))
                    bus = Bus.query.get(cheapest.bus_id) if cheapest.bus_id else None
                    
                    return {
                        'message': f"CHEAPEST ROUTE\n\n"
                                  f"From: {source_match}\n"
                                  f"To: {dest_match}\n\n"
                                  f"Bus: {bus.bus_number if bus else cheapest.route_number}\n"
                                  f"Type: {bus.bus_type if bus else 'Standard'}\n"
                                  f"Fare: ₹{float(cheapest.fare)}\n"
                                  f"Distance: {float(cheapest.distance_km) if cheapest.distance_km else 'N/A'} km",
                        'type': 'text',
                        'suggestions': ['Book Ticket', 'View All Routes', 'New Search']
                    }
        
        return {
            'message': "Find cheapest route\n\nExample: 'Cheapest route from CP to Dwarka'",
            'type': 'text',
            'suggestions': ['Find Route']
        }
    
    def handle_fastest_route_query(self, user_id, message_lower, original_message):
        """Handle fastest route queries using Dijkstra's algorithm"""
        locations = self.location_handler.extract_locations_from_message(original_message)
        
        if len(locations) >= 2:
            source_match, _ = self.location_handler.find_best_location_match(locations[0])
            dest_match, _ = self.location_handler.find_best_location_match(locations[1])
            
            # Use Dijkstra's algorithm for shortest distance
            shortest_route, total_distance, path = PathfindingAlgorithms.dijkstra_shortest_path(source_match, dest_match)
            
            if shortest_route:
                bus = Bus.query.get(shortest_route.bus_id) if shortest_route.bus_id else None
                path_str = " → ".join(path) if len(path) > 2 else f"{source_match} → {dest_match}"
                
                return {
                    'message': f"SHORTEST PATH (Dijkstra's Algorithm)\n\n"
                              f"From: {source_match}\n"
                              f"To: {dest_match}\n\n"
                              f"Bus: {bus.bus_number if bus else shortest_route.route_number}\n"
                              f"Type: {bus.bus_type if bus else 'Standard'}\n"
                              f"Total Distance: {total_distance:.2f} km\n"
                              f"Fare: ₹{float(shortest_route.fare)}\n"
                              f"Duration: {shortest_route.estimated_duration_minutes if shortest_route.estimated_duration_minutes else 'N/A'} min\n"
                              f"Path: {path_str}",
                    'type': 'text',
                    'suggestions': ['Book Ticket', 'Cheapest Route', 'New Search']
                }
            else:
                # Fallback to simple search
                routes = self.route_search.find_routes(locations[0], locations[1], self.location_handler)
                if routes:
                    fastest = min(routes, key=lambda r: r.estimated_duration_minutes if r.estimated_duration_minutes else float(r.distance_km) if r.distance_km else 999)
                    bus = Bus.query.get(fastest.bus_id) if fastest.bus_id else None
                    
                    return {
                        'message': f"FASTEST ROUTE\n\n"
                                  f"From: {source_match}\n"
                                  f"To: {dest_match}\n\n"
                                  f"Bus: {bus.bus_number if bus else fastest.route_number}\n"
                                  f"Type: {bus.bus_type if bus else 'Standard'}\n"
                                  f"Duration: {fastest.estimated_duration_minutes if fastest.estimated_duration_minutes else 'N/A'} min\n"
                                  f"Distance: {float(fastest.distance_km) if fastest.distance_km else 'N/A'} km\n"
                                  f"Fare: ₹{float(fastest.fare)}",
                        'type': 'text',
                        'suggestions': ['Book Ticket', 'View All Routes', 'New Search']
                    }
        
        return {
            'message': "Find fastest route\n\nExample: 'Fastest route from CP to Dwarka'",
            'type': 'text',
            'suggestions': ['Find Route']
        }
    
    def handle_ac_bus_query(self, user_id, message_lower, original_message):
        """Handle AC bus queries"""
        locations = self.location_handler.extract_locations_from_message(original_message)
        
        if len(locations) >= 2:
            source_match, _ = self.location_handler.find_best_location_match(locations[0])
            dest_match, _ = self.location_handler.find_best_location_match(locations[1])
            
            routes = self.route_search.find_routes(locations[0], locations[1], self.location_handler)
            if routes:
                # Filter AC buses
                ac_routes = []
                for route in routes:
                    bus = Bus.query.get(route.bus_id) if route.bus_id else None
                    if bus and 'AC' in bus.bus_type.upper():
                        ac_routes.append(route)
                
                if ac_routes:
                    return self.route_search.generate_recommendations(ac_routes, source_match, dest_match)
                else:
                    return {
                        'message': f"No AC buses available\n\nFrom: {source_match}\nTo: {dest_match}\n\nShowing all routes:",
                        'type': 'text',
                        'suggestions': ['View All Routes', 'New Search']
                    }
        
        return {
            'message': "Find AC bus routes\n\nExample: 'AC bus from CP to Dwarka'",
            'type': 'text',
            'suggestions': ['Find Route']
        }
