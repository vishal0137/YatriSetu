"""
Location Handler Module
Handles location normalization, fuzzy matching, and aliases
"""

from difflib import SequenceMatcher
from app import db
from app.models import Route, Stop

class LocationHandler:
    """Handles all location-related operations"""
    
    def __init__(self):
        self.location_cache = None
        self.location_aliases = {
            'cp': 'Connaught Place',
            'connaught': 'Connaught Place',
            'kashmiri': 'Kashmere Gate',
            'kashmere': 'Kashmere Gate',
            'airport': 'IGI Airport',
            'igi': 'IGI Airport',
            'isbt': 'ISBT Kashmere Gate',
            'anand vihar': 'Anand Vihar ISBT',
            'saket': 'Saket District Centre',
            'nehru place': 'Nehru Place',
            'rajiv chowk': 'Connaught Place',
            'new delhi': 'New Delhi Railway Station',
            'ndls': 'New Delhi Railway Station',
            'old delhi': 'Old Delhi Railway Station',
            'chandni chowk': 'Chandni Chowk',
            'red fort': 'Red Fort',
            'india gate': 'India Gate',
            'qutub minar': 'Qutub Minar',
            'lotus temple': 'Lotus Temple',
            'akshardham': 'Akshardham Temple',
            'dwarka': 'Dwarka Sector 21',
            'noida': 'Noida City Centre',
            'gurgaon': 'Gurgaon Cyber City',
            'gurugram': 'Gurgaon Cyber City',
            'vasant kunj': 'Vasant Kunj',
            'rohini': 'Rohini Sector 18',
            'pitampura': 'Pitampura',
            'janakpuri': 'Janakpuri West',
            'lajpat nagar': 'Lajpat Nagar',
            'south ex': 'South Extension',
            'hauz khas': 'Hauz Khas',
            'green park': 'Green Park',
            'karol bagh': 'Karol Bagh',
            'paharganj': 'Paharganj',
            'nizamuddin': 'Hazrat Nizamuddin',
            'okhla': 'Okhla Industrial Area',
            'kalkaji': 'Kalkaji Mandir',
            'badarpur': 'Badarpur Border',
            'faridabad': 'Faridabad New Town',
            'ghaziabad': 'Ghaziabad',
            'vaishali': 'Vaishali',
            'mayur vihar': 'Mayur Vihar',
            'laxmi nagar': 'Laxmi Nagar',
            'shahdara': 'Shahdara',
            'azadpur': 'Azadpur',
            'model town': 'Model Town',
        }
    
    def fuzzy_match(self, query, target, threshold=0.6):
        """Calculate fuzzy match score between query and target"""
        query_lower = query.lower().strip()
        target_lower = target.lower().strip()
        
        # Exact match
        if query_lower == target_lower:
            return 1.0
        
        # Contains match
        if query_lower in target_lower or target_lower in query_lower:
            return 0.9
        
        # Sequence matcher
        return SequenceMatcher(None, query_lower, target_lower).ratio()
    
    def normalize_location(self, location):
        """Normalize location name using aliases"""
        location_lower = location.lower().strip()
        
        # Check aliases first
        if location_lower in self.location_aliases:
            return self.location_aliases[location_lower]
        
        # Check partial matches in aliases
        for alias, full_name in self.location_aliases.items():
            if alias in location_lower or location_lower in alias:
                return full_name
        
        # Return title case if no match
        return location.title()
    
    def get_all_locations(self):
        """Get all unique locations from database with caching"""
        if self.location_cache is None:
            try:
                start_locs = db.session.query(Route.start_location).distinct().all()
                end_locs = db.session.query(Route.end_location).distinct().all()
                stop_locs = db.session.query(Stop.stop_name).distinct().all()
                
                locations = set()
                for loc in start_locs + end_locs:
                    if loc[0]:
                        locations.add(loc[0])
                for loc in stop_locs:
                    if loc[0]:
                        locations.add(loc[0])
                
                self.location_cache = list(locations)
            except:
                self.location_cache = []
        
        return self.location_cache
    
    def find_best_location_match(self, query):
        """Find best matching location using fuzzy matching"""
        query_normalized = self.normalize_location(query)
        all_locations = self.get_all_locations()
        
        best_match = None
        best_score = 0.0
        
        for location in all_locations:
            score = self.fuzzy_match(query_normalized, location)
            if score > best_score:
                best_score = score
                best_match = location
        
        # Return match if score is above threshold
        if best_score >= 0.6:
            return best_match, best_score
        
        # Try normalized version
        return query_normalized, 0.5
    
    def extract_location(self, message):
        """Extract a single location from message"""
        # Remove common words
        words = message.lower().split()
        stop_words = ['from', 'to', 'at', 'in', 'the', 'a', 'an', 'route', 'bus', 'go', 'going']
        location_words = [w for w in words if w not in stop_words]
        return ' '.join(location_words)
    
    def extract_locations_from_message(self, message):
        """Extract source and destination from message"""
        import re
        
        # Keywords to filter out (not locations)
        filter_keywords = [
            'bus', 'buses', 'route', 'routes', 'how', 'reach', 'go', 'going', 
            'travel', 'much', 'price', 'fare', 'cost', 'show', 'find', 'get',
            'me', 'the', 'a', 'an', 'is', 'are', 'can', 'will', 'would'
        ]
        
        def clean_location(loc):
            """Remove filter keywords from location string"""
            words = loc.strip().split()
            cleaned = [w for w in words if w.lower() not in filter_keywords]
            return ' '.join(cleaned).strip()
        
        # Pattern: "how to reach X from Y"
        pattern_reach = r'how\s+to\s+reach\s+(.+?)\s+from\s+(.+?)(?:\s|$|\.|\?)'
        match = re.search(pattern_reach, message.lower())
        if match:
            dest = clean_location(match.group(1))
            source = clean_location(match.group(2))
            return [source, dest] if source and dest else []
        
        # Pattern: "from X to Y"
        pattern1 = r'from\s+(.+?)\s+to\s+(.+?)(?:\s|$|\.|\?)'
        match = re.search(pattern1, message.lower())
        if match:
            source = clean_location(match.group(1))
            dest = clean_location(match.group(2))
            return [source, dest] if source and dest else []
        
        # Pattern: "X to Y" (but not if X is a keyword)
        pattern2 = r'(.+?)\s+to\s+(.+?)(?:\s|$|\.|\?)'
        match = re.search(pattern2, message.lower())
        if match:
            source = clean_location(match.group(1))
            dest = clean_location(match.group(2))
            # Only return if source is not empty after cleaning
            if source and dest:
                return [source, dest]
            elif dest:
                # If source was filtered out, treat as destination-only
                return [dest]
        
        # Pattern: "to Y" (destination only)
        pattern3 = r'to\s+(.+?)(?:\s|$|\.|\?)'
        match = re.search(pattern3, message.lower())
        if match:
            dest = clean_location(match.group(1))
            return [dest] if dest else []
        
        return []
    
    def get_popular_destinations(self):
        """Get list of popular destinations"""
        return [
            'Connaught Place',
            'IGI Airport',
            'Kashmere Gate',
            'Anand Vihar ISBT',
            'Dwarka Sector 21',
            'Noida City Centre',
            'Gurgaon Cyber City',
            'Nehru Place',
            'Saket District Centre',
            'Hauz Khas'
        ]
