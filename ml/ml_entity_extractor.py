"""
Entity Extraction for YatriSetu Chatbot
Extracts locations, bus numbers, and other entities from user queries
"""

import re
import spacy
from difflib import SequenceMatcher

class EntityExtractor:
    """Extract entities from user queries"""
    
    def __init__(self, use_spacy=True):
        self.use_spacy = use_spacy
        self.nlp = None
        self.locations = []
        
        if use_spacy:
            try:
                self.nlp = spacy.load('en_core_web_sm')
                print("spaCy model loaded successfully")
            except:
                print("spaCy model not found. Run: python -m spacy download en_core_web_sm")
                self.use_spacy = False
    
    def load_locations(self, locations):
        """Load known locations for matching"""
        self.locations = [loc.lower() for loc in locations]
        print(f"Loaded {len(self.locations)} locations")
    
    def extract_entities(self, text):
        """
        Extract all entities from text
        
        Returns:
            dict with keys: locations, bus_numbers, numbers
        """
        entities = {
            'locations': [],
            'bus_numbers': [],
            'numbers': [],
            'source': None,
            'destination': None
        }
        
        # Extract using spaCy if available
        if self.use_spacy and self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ['GPE', 'LOC', 'FAC']:
                    entities['locations'].append(ent.text)
        
        # Extract bus numbers (2-4 digits)
        bus_numbers = re.findall(r'\bbus\s+(\d{2,4})\b', text.lower())
        if not bus_numbers:
            bus_numbers = re.findall(r'\b(\d{2,4})\b', text)
        entities['bus_numbers'] = bus_numbers
        
        # Extract all numbers
        numbers = re.findall(r'\b\d+\b', text)
        entities['numbers'] = numbers
        
        # Extract source and destination
        source, dest = self.extract_source_destination(text)
        entities['source'] = source
        entities['destination'] = dest
        
        return entities
    
    def extract_source_destination(self, text):
        """Extract source and destination locations"""
        text_lower = text.lower()
        
        # Pattern 1: "from X to Y"
        pattern1 = r'from\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+?)(?:\s|$|[?.!])'
        match = re.search(pattern1, text_lower, re.IGNORECASE)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        
        # Pattern 2: "X to Y"
        pattern2 = r'(?:^|\s)([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+?)(?:\s|$|[?.!])'
        match = re.search(pattern2, text_lower, re.IGNORECASE)
        if match:
            source = match.group(1).strip()
            dest = match.group(2).strip()
            # Remove common prefixes
            for prefix in ['route', 'bus', 'fare', 'price', 'cost', 'go', 'going']:
                source = source.replace(prefix, '').strip()
                dest = dest.replace(prefix, '').strip()
            return source, dest
        
        # Pattern 3: "go to X from Y"
        pattern3 = r'(?:go|reach|travel)\s+to\s+([a-zA-Z\s]+?)\s+from\s+([a-zA-Z\s]+?)(?:\s|$|[?.!])'
        match = re.search(pattern3, text_lower, re.IGNORECASE)
        if match:
            return match.group(2).strip(), match.group(1).strip()
        
        # Pattern 4: "to X" (destination only)
        pattern4 = r'(?:to|reach)\s+([a-zA-Z\s]+?)(?:\s|$|[?.!])'
        match = re.search(pattern4, text_lower, re.IGNORECASE)
        if match:
            return None, match.group(1).strip()
        
        return None, None
    
    def find_similar_location(self, query, threshold=0.6):
        """
        Find most similar location from known locations
        
        Args:
            query: Location query string
            threshold: Minimum similarity score (0-1)
        
        Returns:
            (best_match, score) or (None, 0.0)
        """
        if not self.locations:
            return None, 0.0
        
        query_lower = query.lower().strip()
        best_match = None
        best_score = 0.0
        
        for location in self.locations:
            # Exact match
            if query_lower == location:
                return location, 1.0
            
            # Contains match
            if query_lower in location or location in query_lower:
                score = 0.9
                if score > best_score:
                    best_score = score
                    best_match = location
                continue
            
            # Fuzzy match
            score = SequenceMatcher(None, query_lower, location).ratio()
            if score > best_score:
                best_score = score
                best_match = location
        
        if best_score >= threshold:
            return best_match, best_score
        
        return None, best_score
    
    def extract_and_match_locations(self, text):
        """
        Extract locations and match to known locations
        
        Returns:
            dict with matched source and destination
        """
        entities = self.extract_entities(text)
        
        result = {
            'source': None,
            'destination': None,
            'source_confidence': 0.0,
            'dest_confidence': 0.0
        }
        
        if entities['source']:
            match, score = self.find_similar_location(entities['source'])
            result['source'] = match
            result['source_confidence'] = score
        
        if entities['destination']:
            match, score = self.find_similar_location(entities['destination'])
            result['destination'] = match
            result['dest_confidence'] = score
        
        return result

if __name__ == '__main__':
    # Test entity extractor
    extractor = EntityExtractor(use_spacy=False)
    
    # Load sample locations
    sample_locations = [
        'Connaught Place', 'Dwarka', 'Airport', 'IGI Airport',
        'Kashmere Gate', 'ISBT', 'Noida', 'Gurgaon'
    ]
    extractor.load_locations(sample_locations)
    
    # Test queries
    test_queries = [
        "Route from CP to Dwarka",
        "Bus to airport",
        "Track bus 101",
        "Fare from kashmiri gate to noida",
        "How to reach Gurgaon from Connaught Place"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        entities = extractor.extract_entities(query)
        print(f"Entities: {entities}")
        
        matched = extractor.extract_and_match_locations(query)
        print(f"Matched: {matched}")
