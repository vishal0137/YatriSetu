"""
Training script for YatriSetu ML Chatbot Models
Run this to train intent classifier and prepare models
"""

import json
import os
from ml_intent_classifier import IntentClassifier

def create_training_data():
    """Create comprehensive training data for intent classification"""
    training_data = {
        "intents": [
            {
                "intent": "find_route",
                "examples": [
                    "Route from CP to Dwarka",
                    "How to reach Noida from Kashmere Gate",
                    "Bus to Airport",
                    "I want to go to Gurgaon",
                    "Show me routes to ISBT",
                    "Which bus goes to Dwarka",
                    "How can I reach Airport from CP",
                    "Take me to Noida",
                    "Going to Dwarka",
                    "Travel to Airport",
                    "Route to Gurgaon",
                    "Bus from CP to ISBT",
                    "How do I get to Noida",
                    "Show routes to Airport",
                    "I need to go to Dwarka",
                    "Find bus to Gurgaon",
                    "Show me way to ISBT",
                    "Routes available to Noida",
                    "Which route to Airport",
                    "Best route to Dwarka",
                    "Route from Kashmere Gate to CP",
                    "How to go to Gurgaon",
                    "Take me from CP to Noida",
                    "I want route to Airport",
                    "Show bus routes to Dwarka"
                ]
            },
            {
                "intent": "check_fare",
                "examples": [
                    "Fare from CP to Dwarka",
                    "How much to Airport",
                    "Price to Noida",
                    "What's the cost to Gurgaon",
                    "Ticket price from Kashmere Gate to ISBT",
                    "How much does it cost to Dwarka",
                    "What is the fare to Airport",
                    "Cost from CP to Noida",
                    "Price from Kashmere Gate to Dwarka",
                    "How much for ticket to ISBT",
                    "Fare to Gurgaon",
                    "Cost to Airport",
                    "Price from CP to Dwarka",
                    "How much is ticket to Noida",
                    "What's the price to ISBT",
                    "Ticket cost to Dwarka",
                    "Fare from Kashmere Gate to Airport",
                    "How much to go to Gurgaon",
                    "Price for bus to Noida",
                    "Cost of ticket to CP"
                ]
            },
            {
                "intent": "track_bus",
                "examples": [
                    "Track bus 101",
                    "Where is bus 205",
                    "Location of bus 150",
                    "Show me bus 101 location",
                    "Find bus 205",
                    "Bus 150 location",
                    "Where is 101",
                    "Track 205",
                    "Show bus 150",
                    "Locate bus 101",
                    "Where is bus number 205",
                    "Track bus number 150",
                    "Find location of bus 101",
                    "Show me where bus 205 is",
                    "Bus 150 current location"
                ]
            },
            {
                "intent": "cheapest_route",
                "examples": [
                    "Cheapest route to Dwarka",
                    "Lowest fare to Airport",
                    "Most affordable bus to Noida",
                    "Cheap route to Gurgaon",
                    "Economical bus to ISBT",
                    "Budget route to Dwarka",
                    "Least expensive to Airport",
                    "Cheapest way to Noida",
                    "Lowest price to Gurgaon",
                    "Most economical to ISBT",
                    "Cheapest bus to Dwarka",
                    "Lowest cost route to Airport",
                    "Budget friendly to Noida",
                    "Cheap bus to Gurgaon",
                    "Affordable route to ISBT"
                ]
            },
            {
                "intent": "fastest_route",
                "examples": [
                    "Fastest route to Airport",
                    "Quickest way to Noida",
                    "Shortest route to Dwarka",
                    "Quick route to Gurgaon",
                    "Fast bus to ISBT",
                    "Fastest way to Airport",
                    "Quickest route to Noida",
                    "Shortest path to Dwarka",
                    "Quick bus to Gurgaon",
                    "Fast route to ISBT",
                    "Fastest bus to Airport",
                    "Quickest bus to Noida",
                    "Shortest time to Dwarka",
                    "Quick way to Gurgaon",
                    "Fast way to ISBT"
                ]
            },
            {
                "intent": "ac_bus",
                "examples": [
                    "AC bus to Dwarka",
                    "Air conditioned bus to Airport",
                    "Show AC buses to Gurgaon",
                    "AC route to Noida",
                    "Air conditioned to ISBT",
                    "AC bus from CP to Dwarka",
                    "Air conditioned bus to Airport",
                    "Show me AC buses to Noida",
                    "AC route from Kashmere Gate to Gurgaon",
                    "Air conditioned bus to ISBT",
                    "AC buses available to Dwarka",
                    "Air conditioned route to Airport",
                    "Show AC bus to Noida",
                    "AC bus route to Gurgaon",
                    "Air conditioned buses to ISBT"
                ]
            },
            {
                "intent": "book_ticket",
                "examples": [
                    "Book ticket",
                    "I want to book",
                    "Reserve seat",
                    "Buy ticket",
                    "Book now",
                    "Make reservation",
                    "Book a ticket",
                    "I want to reserve",
                    "Buy bus ticket",
                    "Book seat",
                    "Make booking",
                    "Reserve ticket",
                    "I want to buy ticket",
                    "Book bus ticket",
                    "Make a reservation"
                ]
            },
            {
                "intent": "greeting",
                "examples": [
                    "Hi", "Hello", "Hey", "Namaste", "Good morning",
                    "Good evening", "Hola", "Yo", "Sup", "Hi there",
                    "Hello there", "Hey there", "Good afternoon",
                    "Greetings", "Howdy", "What's up", "Hiya"
                ]
            },
            {
                "intent": "help",
                "examples": [
                    "Help", "What can you do", "How to use",
                    "Guide me", "Assist me", "Show options",
                    "What are your features", "Help me",
                    "I need help", "Show me help", "What can I ask",
                    "How does this work", "Guide", "Assistance",
                    "Show features", "What do you do"
                ]
            },
            {
                "intent": "statistics",
                "examples": [
                    "How many buses", "Total routes", "Stats",
                    "Show statistics", "Bus count", "Route count",
                    "How many routes", "Total buses", "Show stats",
                    "Statistics", "Bus statistics", "Route statistics",
                    "How many buses available", "Total number of routes",
                    "Show me stats", "Give me statistics"
                ]
            }
        ]
    }
    
    output_path = 'training_data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Training data created: {output_path}")
    
    # Print summary
    total_examples = sum(len(intent['examples']) for intent in training_data['intents'])
    print(f"   - {len(training_data['intents'])} intents")
    print(f"   - {total_examples} training examples")
    
    return output_path

def train_models():
    """Train all ML models"""
    print("=" * 60)
    print("YatriSetu ML Chatbot - Model Training")
    print("=" * 60)
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    print("\n✅ Models directory created")
    
    # Create training data
    print("\n📝 Creating training data...")
    training_data_path = create_training_data()
    
    # Train intent classifier
    print("\n🤖 Training Intent Classifier...")
    print("-" * 60)
    classifier = IntentClassifier()
    accuracy = classifier.train(training_data_path)
    
    # Save model
    model_path = 'models/intent_classifier.pkl'
    classifier.save(model_path)
    
    print("\n" + "=" * 60)
    print("✅ Training Complete!")
    print("=" * 60)
    print(f"\nModel saved to: {model_path}")
    print(f"Training accuracy: {accuracy:.1%}")
    
    print("\n📋 Next Steps:")
    print("1. Install dependencies: pip install scikit-learn")
    print("2. Optional: pip install spacy && python -m spacy download en_core_web_sm")
    print("3. Test the model: python test_ml_chatbot.py")
    print("4. Update app to use ML: Modify app/__init__.py")
    
    print("\n💡 To use ML-enhanced chatbot:")
    print("   from ml_chatbot import MLEnhancedChatbot")
    print("   chatbot = MLEnhancedChatbot()")
    
    return classifier

def test_trained_model():
    """Test the trained model with sample queries"""
    print("\n" + "=" * 60)
    print("Testing Trained Model")
    print("=" * 60)
    
    classifier = IntentClassifier()
    
    try:
        classifier.load('models/intent_classifier.pkl')
    except:
        print("❌ Model not found. Run training first.")
        return
    
    test_queries = [
        "Route from CP to Dwarka",
        "How much to Airport",
        "Track bus 101",
        "Cheapest route to Noida",
        "AC bus to Gurgaon",
        "Book ticket",
        "Hi",
        "Help me",
        "How many buses"
    ]
    
    print("\nTest Queries:")
    print("-" * 60)
    
    for query in test_queries:
        intent, confidence = classifier.predict(query)
        print(f"Query: {query:40} → Intent: {intent:20} ({confidence:.2%})")
    
    print("\n✅ Testing complete!")

if __name__ == '__main__':
    # Train models
    classifier = train_models()
    
    # Test trained model
    test_trained_model()
