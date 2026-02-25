"""
Sampark - AI Chatbot Route Assistant for YatriSetu
Your intelligent transit companion
Modular architecture with separate components for maintainability
"""

from app import db
from app.models.database_models import Route, Stop, Bus, Booking, LiveBusLocation
from sqlalchemy import func, or_, and_
import re
from datetime import datetime

# Import modular components
from app.chatbot_modules.location_handler import LocationHandler
from app.chatbot_modules.route_search import RouteSearchHandler
from app.chatbot_modules.algorithms import PathfindingAlgorithms
from app.chatbot_modules.query_handlers import QueryHandlers

class SamparkChatbot:
    """Sampark - AI-powered chatbot for YatriSetu with modular architecture"""
    
    def __init__(self):
        self.user_context = {}
        
        # Initialize modular components
        self.location_handler = LocationHandler()
        self.route_search = RouteSearchHandler()
        self.query_handlers = QueryHandlers(self.location_handler, self.route_search)
        
        # Store last search results for filtering
        self.last_search_results = {}
    
    def greeting_response(self):
        """Greeting with real statistics"""
        try:
            routes = Route.query.filter_by(is_active=True).count()
            buses = Bus.query.filter_by(is_active=True).count()
            active = LiveBusLocation.query.count()
            
            return {
                'message': f"Namaste! I'm Sampark, your YatriSetu assistant\n\n"
                          f"SYSTEM STATUS\n"
                          f"Active Routes: {routes}\n"
                          f"Fleet Size: {buses} buses\n"
                          f"Currently Operating: {active} buses\n\n"
                          f"NEW CAPABILITIES\n"
                          f"• Direct route lookup: 'Route 001'\n"
                          f"• Bus information: 'Bus DTC-078'\n"
                          f"• Instant access to complete details\n\n"
                          f"How may I assist you today?",
                'type': 'greeting',
                'stats': {
                    'routes': routes,
                    'buses': buses,
                    'active': active
                },
                'suggestions': ['Route 001', 'Bus DTC-078', 'Find Route', 'Help']
            }
        except:
            return {
                'message': "Namaste! I'm Sampark, your YatriSetu assistant\n\n"
                          "How may I assist you?",
                'type': 'greeting',
                'suggestions': ['Route 001', 'Bus DTC-078', 'Find Route', 'Help']
            }
    
    def help_response(self):
        """Help information"""
        return {
            'message': "SAMPARK - YATRISETU ASSISTANT\n"
                      "COMMAND REFERENCE\n\n"
                      "ROUTE SEARCH\n"
                      "• Route from [location] to [destination]\n"
                      "• Bus to [destination]\n\n"
                      "DIRECT INFORMATION\n"
                      "• Route [number] - e.g., 'Route 001'\n"
                      "• Bus [number] - e.g., 'Bus DTC-078'\n\n"
                      "OTHER COMMANDS\n"
                      "• Track bus [number]\n"
                      "• Stats - System statistics\n"
                      "• Help - This message",
            'type': 'help',
            'help_categories': [
                {
                    'title': 'ROUTE SEARCH',
                    'icon': '🔍',
                    'commands': [
                        {'cmd': 'Route from CP to Dwarka', 'desc': 'Find routes between locations'},
                        {'cmd': 'Bus to Airport', 'desc': 'Find buses to destination'},
                        {'cmd': 'Cheapest route to Noida', 'desc': 'Find lowest fare route'},
                        {'cmd': 'Fastest route to Airport', 'desc': 'Find quickest route'}
                    ]
                },
                {
                    'title': 'DIRECT ACCESS',
                    'icon': '⚡',
                    'commands': [
                        {'cmd': 'Route 001', 'desc': 'Get route details instantly'},
                        {'cmd': 'Bus DTC-078', 'desc': 'Get bus information instantly'}
                    ]
                },
                {
                    'title': 'TRACKING & INFO',
                    'icon': '📍',
                    'commands': [
                        {'cmd': 'Track bus DTC-001', 'desc': 'Live bus location'},
                        {'cmd': 'Stats', 'desc': 'System statistics'},
                        {'cmd': 'Fare from CP to Dwarka', 'desc': 'Check fare details'}
                    ]
                }
            ],
            'suggestions': ['Route 001', 'Bus DTC-078', 'Find Route', 'Stats']
        }
    
    def default_response(self):
        """Default response"""
        return {
            'message': "I didn't quite understand that. Try:\n\n"
                      "• 'Route 001' - Get route details\n"
                      "• 'Bus DTC-078' - Get bus information\n"
                      "• 'Help' - See all commands",
            'type': 'text',
            'suggestions': ['Route 001', 'Bus DTC-078', 'Help']
        }
    
    def process_message(self, user_id, message):
        """Process user message"""
        message_lower = message.lower().strip()
        
        # Initialize user context if needed
        if user_id not in self.user_context:
            self.user_context[user_id] = {
                'state': 'initial',
                'source': None,
                'destination': None
            }
        
        # Initialize last search results if needed
        if user_id not in self.last_search_results:
            self.last_search_results[user_id] = {
                'routes': [],
                'source': None,
                'destination': None
            }
        
        context = self.user_context[user_id]
        
        # Greeting
        if any(word in message_lower for word in ['hi', 'hello', 'hey', 'namaste', 'start']):
            context['state'] = 'initial'
            context['source'] = None
            context['destination'] = None
            return self.greeting_response()
        
        # Help
        if 'help' in message_lower:
            return self.help_response()
        
        # New Search - reset context
        if 'new search' in message_lower or 'reset' in message_lower:
            context['state'] = 'initial'
            context['source'] = None
            context['destination'] = None
            return {
                'message': "Starting fresh! How can I help you?",
                'type': 'text',
                'suggestions': ['Find Route', 'Route 001', 'Check Fare', 'Track Bus']
            }
        
        # Popular Routes
        if 'popular routes' in message_lower or 'popular' in message_lower:
            return self.handle_popular_routes()
        
        # How to Book - check before route search
        if 'how to book' in message_lower or 'booking process' in message_lower:
            return self.handle_booking_instructions()
        
        # Ticket Types - check before route search
        if 'ticket types' in message_lower or 'ticket categories' in message_lower or 'passenger categories' in message_lower:
            return self.handle_ticket_types()
        
        # Contact Support - check before route search
        if 'contact support' in message_lower or 'support' in message_lower or 'contact' in message_lower:
            return self.handle_contact_support()
        
        # Find Route - Start conversational flow
        if message_lower in ['find route', 'find a route', 'search route', 'plan journey']:
            context['state'] = 'awaiting_source'
            context['source'] = None
            context['destination'] = None
            return {
                'message': "Let's find your route!\n\nWhere are you starting from?\n\nPlease enter your starting location:",
                'type': 'text',
                'suggestions': ['Connaught Place', 'IGI Airport', 'Kashmere Gate', 'Anand Vihar', 'Dwarka', 'Noida']
            }
        
        # Check Fare - Start conversational flow
        if message_lower in ['check fare', 'fare', 'check price']:
            context['state'] = 'awaiting_source_fare'
            context['source'] = None
            context['destination'] = None
            return {
                'message': "I can help you check fares!\n\nWhere are you starting from?\n\nPlease enter your starting location:",
                'type': 'text',
                'suggestions': ['Connaught Place', 'IGI Airport', 'Kashmere Gate', 'Anand Vihar', 'Dwarka', 'Noida']
            }
        
        # Handle conversational flow states
        if context['state'] == 'awaiting_source':
            # User provided source location
            source_match, source_score = self.location_handler.find_best_location_match(message)
            context['source'] = source_match
            context['state'] = 'awaiting_destination'
            return {
                'message': f"Starting from: {source_match}\n\nWhere do you want to go?\n\nPlease enter your destination:",
                'type': 'text',
                'suggestions': ['Connaught Place', 'IGI Airport', 'Kashmere Gate', 'Anand Vihar', 'Dwarka', 'Noida']
            }
        
        elif context['state'] == 'awaiting_destination':
            # User provided destination
            dest_match, dest_score = self.location_handler.find_best_location_match(message)
            context['destination'] = dest_match
            source = context['source']
            
            # Search for routes
            routes = self.route_search.find_routes(source, dest_match, self.location_handler)
            
            # Store results for filtering
            self.last_search_results[user_id] = {
                'routes': routes,
                'source': source,
                'destination': dest_match
            }
            
            # Reset state
            context['state'] = 'initial'
            
            if routes:
                return self.route_search.generate_recommendations(routes, source, dest_match)
            else:
                return {
                    'message': f"No routes found\n\nFrom: {source}\nTo: {dest_match}\n\nTry different locations or check popular routes.",
                    'type': 'text',
                    'suggestions': ['Popular Routes', 'New Search', 'Help']
                }
        
        elif context['state'] == 'awaiting_source_fare':
            # User provided source for fare check
            source_match, source_score = self.location_handler.find_best_location_match(message)
            context['source'] = source_match
            context['state'] = 'awaiting_destination_fare'
            return {
                'message': f"Starting from: {source_match}\n\nWhere do you want to go?\n\nPlease enter your destination:",
                'type': 'text',
                'suggestions': ['Connaught Place', 'IGI Airport', 'Kashmere Gate', 'Anand Vihar', 'Dwarka', 'Noida']
            }
        
        elif context['state'] == 'awaiting_destination_fare':
            # User provided destination for fare check
            dest_match, dest_score = self.location_handler.find_best_location_match(message)
            context['destination'] = dest_match
            source = context['source']
            
            # Reset state
            context['state'] = 'initial'
            
            # Handle fare query
            return self.query_handlers.handle_fare_query(user_id, f"fare from {source} to {dest_match}", f"fare from {source} to {dest_match}")
        
        # Context-based filtering - Cheapest Route (after search results)
        if message_lower in ['cheapest route', 'cheapest', 'lowest fare', 'cheap']:
            if self.last_search_results[user_id]['routes']:
                routes = self.last_search_results[user_id]['routes']
                source = self.last_search_results[user_id]['source']
                destination = self.last_search_results[user_id]['destination']
                
                # Sort by fare (ascending)
                cheapest_routes = sorted(routes, key=lambda r: float(r.fare))[:5]
                
                msg = f"CHEAPEST ROUTES: {source} → {destination}\n\n"
                for idx, route in enumerate(cheapest_routes, 1):
                    bus = Bus.query.get(route.bus_id) if route.bus_id else None
                    bus_num = bus.bus_number if bus else route.route_number
                    bus_type = bus.bus_type if bus else 'Standard'
                    
                    msg += f"{idx}. Bus {bus_num} ({bus_type})\n"
                    msg += f"   Fare: ₹{float(route.fare)}"
                    
                    if route.distance_km:
                        msg += f" | {float(route.distance_km)} km"
                    if route.estimated_duration_minutes:
                        msg += f" | ~{route.estimated_duration_minutes} min"
                    
                    msg += "\n\n"
                
                return {
                    'message': msg,
                    'type': 'route_list',
                    'routes': [{
                        'route_number': r.route_number,
                        'fare': float(r.fare),
                        'distance': float(r.distance_km) if r.distance_km else None,
                        'start_location': r.start_location,
                        'end_location': r.end_location,
                        'bus_type': Bus.query.get(r.bus_id).bus_type if r.bus_id and Bus.query.get(r.bus_id) else 'Standard'
                    } for r in cheapest_routes],
                    'suggestions': ['Book Ticket', 'Fastest Route', 'All Routes', 'New Search']
                }
            else:
                return {
                    'message': "Please search for routes first.\n\nTry: 'Find Route' or 'Route from [source] to [destination]'",
                    'type': 'text',
                    'suggestions': ['Find Route', 'Route 001', 'Help']
                }
        
        # Context-based filtering - Fastest Route (after search results)
        if message_lower in ['fastest route', 'fastest', 'quickest', 'shortest time', 'quick']:
            if self.last_search_results[user_id]['routes']:
                routes = self.last_search_results[user_id]['routes']
                source = self.last_search_results[user_id]['source']
                destination = self.last_search_results[user_id]['destination']
                
                # Sort by duration (ascending), then by distance if duration not available
                fastest_routes = sorted(
                    routes, 
                    key=lambda r: (
                        r.estimated_duration_minutes if r.estimated_duration_minutes else 999,
                        float(r.distance_km) if r.distance_km else 999
                    )
                )[:5]
                
                msg = f"FASTEST ROUTES: {source} → {destination}\n\n"
                for idx, route in enumerate(fastest_routes, 1):
                    bus = Bus.query.get(route.bus_id) if route.bus_id else None
                    bus_num = bus.bus_number if bus else route.route_number
                    bus_type = bus.bus_type if bus else 'Standard'
                    
                    msg += f"{idx}. Bus {bus_num} ({bus_type})\n"
                    
                    if route.estimated_duration_minutes:
                        msg += f"   Duration: ~{route.estimated_duration_minutes} min"
                    elif route.distance_km:
                        msg += f"   Distance: {float(route.distance_km)} km"
                    
                    msg += f" | Fare: ₹{float(route.fare)}\n\n"
                
                return {
                    'message': msg,
                    'type': 'route_list',
                    'routes': [{
                        'route_number': r.route_number,
                        'fare': float(r.fare),
                        'distance': float(r.distance_km) if r.distance_km else None,
                        'duration': r.estimated_duration_minutes,
                        'start_location': r.start_location,
                        'end_location': r.end_location,
                        'bus_type': Bus.query.get(r.bus_id).bus_type if r.bus_id and Bus.query.get(r.bus_id) else 'Standard'
                    } for r in fastest_routes],
                    'suggestions': ['Book Ticket', 'Cheapest Route', 'All Routes', 'New Search']
                }
            else:
                return {
                    'message': "Please search for routes first.\n\nTry: 'Find Route' or 'Route from [source] to [destination]'",
                    'type': 'text',
                    'suggestions': ['Find Route', 'Route 001', 'Help']
                }
        
        # Show all routes again
        if message_lower in ['all routes', 'show all', 'all']:
            if self.last_search_results[user_id]['routes']:
                routes = self.last_search_results[user_id]['routes']
                source = self.last_search_results[user_id]['source']
                destination = self.last_search_results[user_id]['destination']
                
                return self.route_search.generate_recommendations(routes, source, destination)
            else:
                return {
                    'message': "No previous search results.\n\nTry: 'Find Route' or 'Route from [source] to [destination]'",
                    'type': 'text',
                    'suggestions': ['Find Route', 'Route 001', 'Help']
                }
        
        # Bus Statistics (alternative to stats)
        if 'bus statistics' in message_lower:
            return self.handle_statistics_query(message_lower)
        
        # Route by ID - must have specific pattern (route + number only)
        if re.search(r'\broute\s+(?:id|number|no\.?)?\s*[A-Z0-9-]+\b', message_lower, re.IGNORECASE) and 'from' not in message_lower and 'to' not in message_lower:
            return self.handle_route_by_id_query(message_lower)
        
        # Bus by ID - must have specific pattern (bus + number only)
        if re.search(r'\bbus\s+(?:id|number|no\.?)?\s*[A-Z0-9-]+\b', message_lower, re.IGNORECASE) and 'from' not in message_lower and 'to' not in message_lower and 'ac' not in message_lower:
            return self.handle_bus_by_id_query(message_lower)
        
        # Statistics
        if any(word in message_lower for word in ['stats', 'statistics', 'count']):
            return self.handle_statistics_query(message_lower)
        
        # Tracking
        if 'track' in message_lower:
            return self.handle_live_tracking(message_lower)
        
        # Special queries - Cheapest route (must have from/to)
        if any(word in message_lower for word in ['cheapest', 'cheap', 'lowest fare']) and ('from' in message_lower or 'to' in message_lower):
            return self.query_handlers.handle_cheapest_route_query(user_id, message_lower, message)
        
        # Special queries - Fastest route (must have from/to)
        if any(word in message_lower for word in ['fastest', 'quick', 'shortest']) and ('from' in message_lower or 'to' in message_lower):
            return self.query_handlers.handle_fastest_route_query(user_id, message_lower, message)
        
        # Special queries - AC bus (must have to)
        if any(word in message_lower for word in ['ac bus', 'air conditioned']) and 'to' in message_lower:
            return self.query_handlers.handle_ac_bus_query(user_id, message_lower, message)
        
        # Fare inquiry (must have from/to)
        if any(word in message_lower for word in ['fare', 'price', 'cost', 'how much']) and ('from' in message_lower or 'to' in message_lower):
            return self.query_handlers.handle_fare_query(user_id, message_lower, message)
        
        # Route search (location to location) - check for from/to patterns
        if 'from' in message_lower or 'to' in message_lower or any(word in message_lower for word in ['go to', 'reach', 'going', 'travel']):
            return self.handle_route_query(user_id, message_lower, message)
        
        # Booking
        if any(word in message_lower for word in ['book', 'ticket']):
            return self.query_handlers.handle_booking_intent(user_id, self.user_context)
        
        return self.default_response()
    
    def handle_statistics_query(self, message):
        """Handle statistics"""
        try:
            buses = Bus.query.filter_by(is_active=True).count()
            routes = Route.query.filter_by(is_active=True).count()
            bookings = Booking.query.count()
            active_buses = LiveBusLocation.query.count()
            
            # Get bus type breakdown
            ac_buses = Bus.query.filter(Bus.bus_type.ilike('%AC%'), Bus.is_active==True).count()
            non_ac_buses = buses - ac_buses
            
            return {
                'message': f"YATRISETU STATISTICS\n\n"
                          f"Buses: {buses}\n"
                          f"Routes: {routes}\n"
                          f"Bookings: {bookings}",
                'type': 'statistics',
                'stats': {
                    'total_buses': buses,
                    'active_buses': active_buses,
                    'ac_buses': ac_buses,
                    'non_ac_buses': non_ac_buses,
                    'total_routes': routes,
                    'total_bookings': bookings
                },
                'suggestions': ['Find Route', 'Track Bus', 'Route 001']
            }
        except:
            return self.default_response()
    
    def handle_route_by_id_query(self, message):
        """Handle route query by ID"""
        try:
            route_match = re.search(r'route\s+(?:id|number|no\.?)?\s*([A-Z0-9-]+)', message, re.IGNORECASE)
            
            if route_match:
                route_number = route_match.group(1).upper()
                route = Route.query.filter(
                    or_(
                        Route.route_number.ilike(f'%{route_number}%'),
                        Route.route_number == route_number
                    )
                ).first()
                
                if route:
                    bus = Bus.query.get(route.bus_id) if route.bus_id else None
                    stops = Stop.query.filter_by(route_id=route.id).order_by(Stop.stop_order).all()
                    
                    msg = f"ROUTE INFORMATION\n\n"
                    msg += f"Route: {route.route_number}\n"
                    msg += f"Name: {route.route_name}\n\n"
                    msg += f"JOURNEY\n"
                    msg += f"From: {route.start_location}\n"
                    msg += f"To: {route.end_location}\n\n"
                    
                    if bus:
                        msg += f"ASSIGNED BUS\n"
                        msg += f"Bus: {bus.bus_number}\n"
                        msg += f"Type: {bus.bus_type}\n"
                        msg += f"Capacity: {bus.capacity} seats\n"
                        msg += f"Status: {'Active' if bus.is_active else 'Inactive'}\n\n"
                    
                    msg += f"Fare: ₹{float(route.fare)}\n"
                    if route.distance_km:
                        msg += f"Distance: {float(route.distance_km)} km\n"
                    if route.estimated_duration_minutes:
                        msg += f"Duration: ~{route.estimated_duration_minutes} min\n"
                    
                    if stops:
                        msg += f"\nSTOPS ({len(stops)})\n"
                        for idx, stop in enumerate(stops[:5], 1):
                            msg += f"{idx}. {stop.stop_name}\n"
                        if len(stops) > 5:
                            msg += f"... +{len(stops) - 5} more stops\n"
                    
                    return {
                        'message': msg,
                        'type': 'route_info',
                        'route_data': {
                            'route_number': route.route_number,
                            'route_name': route.route_name,
                            'start': route.start_location,
                            'end': route.end_location,
                            'fare': float(route.fare),
                            'stops_count': len(stops)
                        },
                        'suggestions': ['Book Ticket', 'Track Bus', 'New Search']
                    }
                else:
                    return {
                        'message': f"Route {route_number} not found\n\nTry: 'Route 001' or 'Route 025A'",
                        'type': 'text',
                        'suggestions': ['Find Route', 'Help']
                    }
        except Exception as e:
            print(f"Error: {e}")
            return self.default_response()
    
    def handle_bus_by_id_query(self, message):
        """Handle bus query by ID"""
        try:
            bus_match = re.search(r'bus\s+(?:id|number|no\.?)?\s*([A-Z0-9-]+)', message, re.IGNORECASE)
            
            if bus_match:
                bus_number = bus_match.group(1).upper()
                bus = Bus.query.filter(
                    or_(
                        Bus.bus_number.ilike(f'%{bus_number}%'),
                        Bus.bus_number == bus_number,
                        Bus.bus_number == f'DTC-{bus_number}'
                    )
                ).first()
                
                if bus:
                    assigned_routes = Route.query.filter_by(bus_id=bus.id, is_active=True).all()
                    location = LiveBusLocation.query.filter_by(bus_id=bus.id).first()
                    
                    msg = f"BUS INFORMATION\n\n"
                    msg += f"Bus: {bus.bus_number}\n"
                    msg += f"Registration: {bus.registration_number}\n"
                    msg += f"Type: {bus.bus_type}\n"
                    msg += f"Capacity: {bus.capacity} seats\n"
                    msg += f"Status: {'Active' if bus.is_active else 'Inactive'}\n\n"
                    
                    if location:
                        msg += f"LIVE LOCATION\n"
                        msg += f"Speed: {float(location.speed) if location.speed else 0} km/h\n"
                        msg += f"Updated: {location.last_updated.strftime('%I:%M %p')}\n\n"
                    
                    if assigned_routes:
                        msg += f"ASSIGNED ROUTES ({len(assigned_routes)})\n\n"
                        for idx, route in enumerate(assigned_routes, 1):
                            msg += f"{idx}. Route {route.route_number}\n"
                            msg += f"   {route.start_location} → {route.end_location}\n"
                            msg += f"   Fare: ₹{float(route.fare)}\n\n"
                    else:
                        msg += f"ASSIGNED ROUTES: None\n"
                    
                    route_suggestions = [f"Route {r.route_number}" for r in assigned_routes[:3]] if assigned_routes else []
                    
                    return {
                        'message': msg,
                        'type': 'bus_info',
                        'bus_data': {
                            'bus_number': bus.bus_number,
                            'bus_type': bus.bus_type,
                            'capacity': bus.capacity,
                            'is_active': bus.is_active,
                            'routes': [{
                                'route_number': r.route_number,
                                'route_name': r.route_name,
                                'start': r.start_location,
                                'end': r.end_location,
                                'fare': float(r.fare)
                            } for r in assigned_routes]
                        },
                        'suggestions': route_suggestions + ['Track Bus', 'New Search'] if route_suggestions else ['Find Route', 'New Search']
                    }
                else:
                    return {
                        'message': f"Bus {bus_number} not found\n\nTry: 'Bus DTC-001' or 'Bus 078'",
                        'type': 'text',
                        'suggestions': ['Find Route', 'Help']
                    }
        except Exception as e:
            print(f"Error: {e}")
            return self.default_response()
    
    def handle_live_tracking(self, message):
        """Handle live tracking"""
        try:
            bus_match = re.search(r'\b(DTC-\d{3}|[A-Z]+-\d{2,4}|\d{2,4})\b', message, re.IGNORECASE)
            
            if bus_match:
                bus_number = bus_match.group(1).upper()
                bus = Bus.query.filter_by(bus_number=bus_number).first()
                
                if bus:
                    location = LiveBusLocation.query.filter_by(bus_id=bus.id).first()
                    
                    if location:
                        return {
                            'message': f"Bus {bus_number}\n\n"
                                      f"Type: {bus.bus_type}\n"
                                      f"Capacity: {bus.capacity} seats\n"
                                      f"Speed: {location.speed} km/h\n"
                                      f"Updated: {location.last_updated.strftime('%I:%M %p')}",
                            'type': 'tracking',
                            'suggestions': ['Track Another', 'Find Route']
                        }
                    else:
                        return {
                            'message': f"Bus {bus_number}\n\nLive tracking unavailable",
                            'type': 'tracking',
                            'suggestions': ['Find Route']
                        }
                else:
                    return {
                        'message': f"Bus {bus_number} not found",
                        'type': 'text',
                        'suggestions': ['Try Again', 'Find Route']
                    }
            else:
                buses = Bus.query.filter_by(is_active=True).limit(5).all()
                bus_list = ', '.join([b.bus_number for b in buses])
                
                return {
                    'message': f"Track a bus\n\nExample buses: {bus_list}\n\nSay: 'Track bus [number]'",
                    'type': 'text',
                    'suggestions': [f'Track {buses[0].bus_number}' if buses else 'Find Route']
                }
        except:
            return self.default_response()
    
    def handle_route_query(self, user_id, message_lower, original_message):
        """Handle route search with real data and fuzzy matching"""
        locations = self.location_handler.extract_locations_from_message(original_message)
        
        # Check if only destination is provided
        if len(locations) == 1:
            destination = locations[0]
            dest_match, dest_score = self.location_handler.find_best_location_match(destination)
            
            # Find all routes TO this destination
            all_routes_to_dest = self.route_search.find_all_routes_to_destination(dest_match)
            
            if all_routes_to_dest:
                return self.route_search.generate_destination_based_recommendations(all_routes_to_dest, dest_match)
            else:
                return {
                    'message': f"No routes found to {dest_match}\n\nTry these popular destinations:",
                    'type': 'text',
                    'suggestions': self.location_handler.get_popular_destinations()[:6]
                }
        
        elif len(locations) >= 2:
            source, destination = locations[0], locations[1]
            
            # Normalize locations
            source_match, source_score = self.location_handler.find_best_location_match(source)
            dest_match, dest_score = self.location_handler.find_best_location_match(destination)
            
            self.user_context[user_id]['source'] = source_match
            self.user_context[user_id]['destination'] = dest_match
            
            routes = self.route_search.find_routes(source, destination, self.location_handler)
            
            # Store results for filtering
            self.last_search_results[user_id] = {
                'routes': routes,
                'source': source_match,
                'destination': dest_match
            }
            
            if routes:
                # Add confidence message if fuzzy matched
                confidence_msg = ""
                if source_score < 1.0 or dest_score < 1.0:
                    confidence_msg = f"Showing results for: {source_match} → {dest_match}\n\n"
                
                result = self.route_search.generate_recommendations(routes, source_match, dest_match)
                result['message'] = confidence_msg + result['message']
                return result
            else:
                # Suggest similar locations
                suggestions = self.location_handler.get_popular_destinations()[:6]
                return {
                    'message': f"No routes found\n\n"
                              f"From: {source_match}\n"
                              f"To: {dest_match}\n\n"
                              f"Try these popular destinations:",
                    'type': 'text',
                    'suggestions': suggestions
                }
        else:
            # Initialize user context
            if user_id not in self.user_context:
                self.user_context[user_id] = {
                    'state': 'initial',
                    'source': None,
                    'destination': None
                }
            
            self.user_context[user_id]['state'] = 'awaiting_source'
            return {
                'message': "Let's find your route!\n\nWhere are you starting from?",
                'type': 'text',
                'suggestions': self.location_handler.get_popular_destinations()[:4]
            }
    
    def handle_popular_routes(self):
        """Handle popular routes query"""
        try:
            # Get routes with most bookings
            from sqlalchemy import func
            popular_routes = db.session.query(
                Route, func.count(Booking.id).label('booking_count')
            ).join(
                Booking, Route.id == Booking.route_id, isouter=True
            ).filter(
                Route.is_active == True
            ).group_by(Route.id).order_by(
                func.count(Booking.id).desc()
            ).limit(10).all()
            
            if not popular_routes:
                return {
                    'message': "No popular routes data available yet.",
                    'type': 'text',
                    'suggestions': ['Find Route', 'Route 001', 'Stats']
                }
            
            msg = "POPULAR ROUTES\n"
            msg += "Most frequently used routes\n\n"
            
            for idx, (route, count) in enumerate(popular_routes, 1):
                bus = Bus.query.get(route.bus_id) if route.bus_id else None
                bus_num = bus.bus_number if bus else route.route_number
                
                msg += f"{idx}. {route.start_location} → {route.end_location}\n"
                msg += f"   Bus {bus_num} | ₹{float(route.fare)}"
                if count > 0:
                    msg += f" | {count} bookings"
                msg += "\n\n"
            
            return {
                'message': msg,
                'type': 'popular_routes',
                'routes': [{
                    'route_number': r.route_number,
                    'start': r.start_location,
                    'end': r.end_location,
                    'fare': float(r.fare),
                    'bookings': count
                } for r, count in popular_routes],
                'suggestions': ['Book Ticket', 'Find Route', 'Stats']
            }
        except Exception as e:
            print(f"Error getting popular routes: {e}")
            return {
                'message': "Unable to fetch popular routes at the moment.",
                'type': 'text',
                'suggestions': ['Find Route', 'Route 001']
            }
    
    def handle_booking_instructions(self):
        """Handle booking instructions query"""
        return {
            'message': "HOW TO BOOK TICKETS\n\n"
                      "STEP 1: FIND YOUR ROUTE\n"
                      "• Search: 'Route from [source] to [destination]'\n"
                      "• Or use route ID: 'Route 001'\n\n"
                      "STEP 2: SELECT ROUTE\n"
                      "• Review fare and timing\n"
                      "• Click 'Book Ticket' button\n\n"
                      "STEP 3: PASSENGER DETAILS\n"
                      "• Select passenger category\n"
                      "• Enter passenger information\n"
                      "• Choose seat (if available)\n\n"
                      "STEP 4: PAYMENT\n"
                      "• Review booking details\n"
                      "• Complete payment\n"
                      "• Receive QR code ticket\n\n"
                      "PASSENGER CATEGORIES\n"
                      "• General: Full fare\n"
                      "• Student: 50% discount\n"
                      "• Senior Citizen: 50% discount\n"
                      "• Disabled: Free travel",
            'type': 'booking_help',
            'suggestions': ['Ticket Types', 'General', 'Student', 'Senior Citizen']
        }
    
    def handle_ticket_types(self):
        """Handle ticket types query"""
        return {
            'message': "PASSENGER CATEGORIES & FARES\n\n"
                      "GENERAL PASSENGER\n"
                      "• Full fare applies\n"
                      "• No discount\n"
                      "• Valid ID required\n\n"
                      "STUDENT\n"
                      "• 50% discount on fare\n"
                      "• Valid student ID card required\n"
                      "• Age limit: Up to 25 years\n\n"
                      "SENIOR CITIZEN\n"
                      "• 50% discount on fare\n"
                      "• Age: 60 years and above\n"
                      "• Valid age proof required\n\n"
                      "DISABLED PERSON\n"
                      "• FREE travel\n"
                      "• Valid disability certificate required\n"
                      "• Companion allowed at 50% fare\n\n"
                      "REQUIRED DOCUMENTS\n"
                      "• Valid government-issued ID\n"
                      "• Category-specific proof\n"
                      "• Booking confirmation (QR code)",
            'type': 'ticket_types',
            'ticket_categories': [
                {
                    'name': 'General',
                    'discount': '0%',
                    'description': 'Full fare, no discount',
                    'requirements': 'Valid ID'
                },
                {
                    'name': 'Student',
                    'discount': '50%',
                    'description': 'Half fare for students',
                    'requirements': 'Student ID, Age ≤ 25'
                },
                {
                    'name': 'Senior Citizen',
                    'discount': '50%',
                    'description': 'Half fare for seniors',
                    'requirements': 'Age proof, Age ≥ 60'
                },
                {
                    'name': 'Disabled',
                    'discount': '100%',
                    'description': 'Free travel',
                    'requirements': 'Disability certificate'
                }
            ],
            'suggestions': ['How to Book', 'Check Fare', 'Find Route']
        }
    
    def handle_contact_support(self):
        """Handle contact support query"""
        return {
            'message': "YATRISETU SUPPORT\n\n"
                      "HELPLINE\n"
                      "• Phone: 1800-XXX-XXXX (Toll-free)\n"
                      "• Hours: 24/7 Available\n\n"
                      "EMAIL SUPPORT\n"
                      "• General: support@yatrisetu.com\n"
                      "• Bookings: bookings@yatrisetu.com\n"
                      "• Complaints: complaints@yatrisetu.com\n\n"
                      "OFFICE ADDRESS\n"
                      "YatriSetu Transport Services\n"
                      "Transport Bhawan, Sector 9\n"
                      "New Delhi - 110001\n\n"
                      "SOCIAL MEDIA\n"
                      "• Twitter: @YatriSetuOfficial\n"
                      "• Facebook: /YatriSetuIndia\n"
                      "• Instagram: @yatrisetu\n\n"
                      "EMERGENCY\n"
                      "• Accident/Emergency: 100\n"
                      "• Lost & Found: 1800-XXX-YYYY",
            'type': 'contact_support',
            'contact_info': {
                'helpline': '1800-XXX-XXXX',
                'email': 'support@yatrisetu.com',
                'hours': '24/7',
                'emergency': '100'
            },
            'suggestions': ['How to Book', 'Ticket Types', 'Find Route', 'Stats']
        }

# Create singleton instance
chatbot = SamparkChatbot()
