"""
Database-driven ML Training for YatriSetu Chatbot
Automatically generates training data from database and user interactions
"""

import json
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db, create_app
from app.models.database_models import Route, Bus, Stop, Booking, User
from ml.ml_intent_classifier import IntentClassifier
from ml.ml_entity_extractor import EntityExtractor

class DatabaseTrainer:
    """Train ML models using database data"""
    
    def __init__(self):
        self.app = create_app()
        self.training_data = {
            "intents": [],
            "entities": {
                "locations": [],
                "bus_numbers": [],
                "route_numbers": []
            }
        }
    
    def extract_locations_from_db(self):
        """Extract all unique locations from database"""
        with self.app.app_context():
            locations = set()
            
            # From routes
            routes = Route.query.all()
            for route in routes:
                if route.start_location:
                    locations.add(route.start_location)
                if route.end_location:
                    locations.add(route.end_location)
            
            # From stops
            stops = Stop.query.all()
            for stop in stops:
                if stop.stop_name:
                    locations.add(stop.stop_name)
            
            return sorted(list(locations))
    
    def extract_bus_numbers_from_db(self):
        """Extract all bus numbers from database"""
        with self.app.app_context():
            buses = Bus.query.all()
            return [bus.bus_number for bus in buses]
    
    def extract_route_numbers_from_db(self):
        """Extract all route numbers from database"""
        with self.app.app_context():
            routes = Route.query.all()
            return [route.route_number for route in routes]
    
    def generate_route_queries(self, locations):
        """Generate route search queries from locations"""
        examples = []
        
        # Take sample locations (not all combinations)
        sample_locations = locations[:20] if len(locations) > 20 else locations
        
        for i, loc1 in enumerate(sample_locations):
            for loc2 in sample_locations[i+1:i+4]:  # Limit combinations
                examples.extend([
                    f"Route from {loc1} to {loc2}",
                    f"How to reach {loc2} from {loc1}",
                    f"Bus to {loc2}",
                    f"Show me routes to {loc2}",
                    f"I want to go to {loc2}",
                ])
        
        # Add generic examples
        examples.extend([
            "Show me all routes",
            "Which buses are available",
            "Find bus route",
            "How do I get there",
            "Take me to destination",
            "Going to the city",
            "Travel route",
            "Bus from here to there"
        ])
        
        return examples[:100]  # Limit to 100 examples
    
    def generate_fare_queries(self, locations):
        """Generate fare inquiry queries"""
        examples = []
        
        sample_locations = locations[:15] if len(locations) > 15 else locations
        
        for i, loc1 in enumerate(sample_locations):
            for loc2 in sample_locations[i+1:i+3]:
                examples.extend([
                    f"Fare from {loc1} to {loc2}",
                    f"How much to {loc2}",
                    f"Price to {loc2}",
                    f"Cost from {loc1} to {loc2}",
                ])
        
        examples.extend([
            "What's the fare",
            "How much does it cost",
            "Ticket price",
            "Show me prices",
            "Cost of journey",
            "Fare information"
        ])
        
        return examples[:80]
    
    def generate_tracking_queries(self, bus_numbers):
        """Generate bus tracking queries"""
        examples = []
        
        sample_buses = bus_numbers[:10] if len(bus_numbers) > 10 else bus_numbers
        
        for bus_num in sample_buses:
            examples.extend([
                f"Track bus {bus_num}",
                f"Where is bus {bus_num}",
                f"Location of bus {bus_num}",
                f"Show me bus {bus_num}",
            ])
        
        examples.extend([
            "Track my bus",
            "Where is the bus",
            "Bus location",
            "Show bus position",
            "Live tracking",
            "Current location"
        ])
        
        return examples[:60]
    
    def generate_training_data_from_db(self):
        """Generate complete training data from database"""
        print("=" * 70)
        print("Generating Training Data from Database")
        print("=" * 70)
        
        # Extract entities from database
        print("\n📊 Extracting data from database...")
        locations = self.extract_locations_from_db()
        bus_numbers = self.extract_bus_numbers_from_db()
        route_numbers = self.extract_route_numbers_from_db()
        
        print(f"   ✅ Found {len(locations)} unique locations")
        print(f"   ✅ Found {len(bus_numbers)} buses")
        print(f"   ✅ Found {len(route_numbers)} routes")
        
        # Store entities
        self.training_data["entities"]["locations"] = locations
        self.training_data["entities"]["bus_numbers"] = bus_numbers
        self.training_data["entities"]["route_numbers"] = route_numbers
        
        # Generate intent examples
        print("\n🤖 Generating intent examples...")
        
        intents = [
            {
                "intent": "find_route",
                "examples": self.generate_route_queries(locations)
            },
            {
                "intent": "check_fare",
                "examples": self.generate_fare_queries(locations)
            },
            {
                "intent": "track_bus",
                "examples": self.generate_tracking_queries(bus_numbers)
            },
            {
                "intent": "cheapest_route",
                "examples": [
                    f"Cheapest route to {loc}" for loc in locations[:10]
                ] + [
                    "Lowest fare", "Most affordable", "Budget route",
                    "Economical bus", "Cheap way to travel"
                ]
            },
            {
                "intent": "fastest_route",
                "examples": [
                    f"Fastest route to {loc}" for loc in locations[:10]
                ] + [
                    "Quickest way", "Shortest route", "Fast bus",
                    "Quick route", "Fastest way"
                ]
            },
            {
                "intent": "ac_bus",
                "examples": [
                    f"AC bus to {loc}" for loc in locations[:10]
                ] + [
                    "Air conditioned bus", "AC route", "Show AC buses",
                    "Air conditioned", "AC available"
                ]
            },
            {
                "intent": "book_ticket",
                "examples": [
                    "Book ticket", "Reserve seat", "Buy ticket",
                    "Make booking", "Book now", "I want to book",
                    "Reserve ticket", "Purchase ticket"
                ]
            },
            {
                "intent": "greeting",
                "examples": [
                    "Hi", "Hello", "Hey", "Namaste", "Good morning",
                    "Good evening", "Hola", "Yo", "Sup", "Hi there"
                ]
            },
            {
                "intent": "help",
                "examples": [
                    "Help", "What can you do", "How to use",
                    "Guide me", "Assist me", "Show options",
                    "What are your features", "Help me"
                ]
            },
            {
                "intent": "statistics",
                "examples": [
                    "How many buses", "Total routes", "Stats",
                    "Show statistics", "Bus count", "Route count"
                ]
            }
        ]
        
        self.training_data["intents"] = intents
        
        # Print summary
        total_examples = sum(len(intent["examples"]) for intent in intents)
        print(f"   ✅ Generated {total_examples} training examples")
        print(f"   ✅ Across {len(intents)} intent categories")
        
        return self.training_data
    
    def save_training_data(self, filepath="ml/training_data_from_db.json"):
        """Save training data to file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.training_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Training data saved to: {filepath}")
        return filepath
    
    def train_models(self):
        """Train ML models using database-generated data"""
        print("\n" + "=" * 70)
        print("Training ML Models from Database")
        print("=" * 70)
        
        # Generate training data
        self.generate_training_data_from_db()
        
        # Save training data
        training_file = self.save_training_data()
        
        # Train intent classifier
        print("\n🤖 Training Intent Classifier...")
        print("-" * 70)
        
        classifier = IntentClassifier()
        accuracy = classifier.train(training_file)
        
        # Save model
        os.makedirs('models', exist_ok=True)
        model_path = 'models/intent_classifier.pkl'
        classifier.save(model_path)
        
        # Train entity extractor
        print("\n🔍 Training Entity Extractor...")
        print("-" * 70)
        
        extractor = EntityExtractor(use_spacy=False)
        locations = self.training_data["entities"]["locations"]
        extractor.load_locations(locations)
        
        print(f"   ✅ Loaded {len(locations)} locations for matching")
        
        # Save metadata
        metadata = {
            "trained_at": datetime.now().isoformat(),
            "database_stats": {
                "locations": len(self.training_data["entities"]["locations"]),
                "buses": len(self.training_data["entities"]["bus_numbers"]),
                "routes": len(self.training_data["entities"]["route_numbers"])
            },
            "model_accuracy": accuracy,
            "total_examples": sum(len(intent["examples"]) for intent in self.training_data["intents"])
        }
        
        with open('models/training_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("\n" + "=" * 70)
        print("✅ Training Complete!")
        print("=" * 70)
        print(f"\n📊 Summary:")
        print(f"   • Model accuracy: {accuracy:.1%}")
        print(f"   • Training examples: {metadata['total_examples']}")
        print(f"   • Locations: {metadata['database_stats']['locations']}")
        print(f"   • Buses: {metadata['database_stats']['buses']}")
        print(f"   • Routes: {metadata['database_stats']['routes']}")
        print(f"\n💾 Files saved:")
        print(f"   • {model_path}")
        print(f"   • {training_file}")
        print(f"   • models/training_metadata.json")
        
        return classifier, extractor, metadata
    
    def add_user_query_to_training(self, query, intent, confidence_threshold=0.8):
        """
        Add user query to training data if confidence is low
        This enables continuous learning from user interactions
        """
        # Load existing training data
        training_file = "ml/training_data_from_db.json"
        
        if os.path.exists(training_file):
            with open(training_file, 'r') as f:
                data = json.load(f)
        else:
            data = self.training_data
        
        # Find intent and add example
        for intent_data in data["intents"]:
            if intent_data["intent"] == intent:
                if query not in intent_data["examples"]:
                    intent_data["examples"].append(query)
                    
                    # Save updated data
                    with open(training_file, 'w') as f:
                        json.dump(data, f, indent=2)
                    
                    return True
        
        return False
    
    def retrain_from_user_feedback(self):
        """
        Retrain models using accumulated user queries
        Call this periodically (e.g., weekly) to improve model
        """
        print("\n🔄 Retraining models with user feedback...")
        
        # This would load user queries from a feedback table
        # For now, we'll just retrain with existing data
        
        return self.train_models()

def main():
    """Main training function"""
    trainer = DatabaseTrainer()
    classifier, extractor, metadata = trainer.train_models()
    
    print("\n" + "=" * 70)
    print("🎉 Success! ML models trained from database")
    print("=" * 70)
    print("\n📋 Next steps:")
    print("   1. Test the model: python ml/test_ml_models.py")
    print("   2. Use in chatbot: See docs/ML_QUICKSTART.md")
    print("   3. Retrain periodically with: python ml/db_trainer.py")

if __name__ == '__main__':
    main()
