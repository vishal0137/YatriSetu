"""
Test Suite for ML Models
Tests intent classification and entity extraction
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.ml_intent_classifier import IntentClassifier
from ml.ml_entity_extractor import EntityExtractor

class TestMLModels:
    """Test ML model functionality"""
    
    def __init__(self):
        self.classifier = None
        self.extractor = None
        self.test_results = []
    
    def load_models(self):
        """Load trained models"""
        print("\n" + "=" * 70)
        print("Loading ML Models")
        print("=" * 70)
        
        try:
            self.classifier = IntentClassifier()
            self.classifier.load('models/intent_classifier.pkl')
            print("✅ Intent classifier loaded")
        except Exception as e:
            print(f"❌ Failed to load intent classifier: {e}")
            return False
        
        try:
            self.extractor = EntityExtractor(use_spacy=False)
            # Load sample locations
            sample_locations = [
                'Connaught Place', 'Dwarka', 'Airport', 'IGI Airport',
                'Kashmere Gate', 'ISBT', 'Noida', 'Gurgaon'
            ]
            self.extractor.load_locations(sample_locations)
            print("✅ Entity extractor loaded")
        except Exception as e:
            print(f"❌ Failed to load entity extractor: {e}")
            return False
        
        return True
    
    def test_intent_classification(self):
        """Test intent classification accuracy"""
        test_cases = [
            ("Route from CP to Dwarka", "find_route"),
            ("How much to Airport", "check_fare"),
            ("Track bus 101", "track_bus"),
            ("Cheapest route to Noida", "cheapest_route"),
            ("Fastest way to Airport", "fastest_route"),
            ("AC bus to Gurgaon", "ac_bus"),
            ("Book ticket", "book_ticket"),
            ("Hi", "greeting"),
            ("Help me", "help"),
            ("How many buses", "statistics")
        ]
        
        print("\n" + "=" * 70)
        print("Testing Intent Classification")
        print("=" * 70)
        
        for query, expected_intent in test_cases:
            intent, confidence = self.classifier.predict(query)
            success = intent == expected_intent and confidence > 0.6
            
            print(f"\n✓ Query: {query}")
            print(f"  Expected: {expected_intent}")
            print(f"  Predicted: {intent}")
            print(f"  Confidence: {confidence:.2%}")
            print(f"  Status: {'✅ PASS' if success else '❌ FAIL'}")
            
            self.test_results.append(('intent_classification', query, success))
    
    def test_entity_extraction(self):
        """Test entity extraction"""
        test_cases = [
            ("Route from CP to Dwarka", ["cp", "dwarka"]),
            ("Track bus 101", ["101"]),
            ("Fare from Kashmere Gate to Noida", ["kashmere gate", "noida"]),
            ("How to reach Airport from ISBT", ["airport", "isbt"])
        ]
        
        print("\n" + "=" * 70)
        print("Testing Entity Extraction")
        print("=" * 70)
        
        for query, expected_entities in test_cases:
            entities = self.extractor.extract_entities(query)
            
            # Check if source or destination extracted
            has_entities = (
                entities['source'] is not None or 
                entities['destination'] is not None or
                len(entities['bus_numbers']) > 0
            )
            
            print(f"\n✓ Query: {query}")
            print(f"  Expected: {expected_entities}")
            print(f"  Extracted: {entities}")
            print(f"  Status: {'✅ PASS' if has_entities else '❌ FAIL'}")
            
            self.test_results.append(('entity_extraction', query, has_entities))
    
    def test_location_matching(self):
        """Test fuzzy location matching"""
        test_cases = [
            ("cp", "connaught place"),
            ("airport", "airport"),
            ("kashmiri gate", "kashmere gate"),
            ("isbt", "isbt")
        ]
        
        print("\n" + "=" * 70)
        print("Testing Location Matching")
        print("=" * 70)
        
        for query, expected in test_cases:
            match, score = self.extractor.find_similar_location(query)
            success = match is not None and score > 0.6
            
            print(f"\n✓ Query: {query}")
            print(f"  Expected: {expected}")
            print(f"  Matched: {match}")
            print(f"  Score: {score:.2f}")
            print(f"  Status: {'✅ PASS' if success else '❌ FAIL'}")
            
            self.test_results.append(('location_matching', query, success))
    
    def test_confidence_scores(self):
        """Test confidence scoring"""
        test_cases = [
            ("Route from CP to Dwarka", 0.8),  # Should be high confidence
            ("xyz abc def", 0.6),  # Should be low confidence
        ]
        
        print("\n" + "=" * 70)
        print("Testing Confidence Scores")
        print("=" * 70)
        
        for query, min_confidence in test_cases:
            intent, confidence = self.classifier.predict(query, threshold=0.5)
            
            if query == "xyz abc def":
                # This should have low confidence
                success = confidence < 0.7
            else:
                # This should have high confidence
                success = confidence >= min_confidence
            
            print(f"\n✓ Query: {query}")
            print(f"  Intent: {intent}")
            print(f"  Confidence: {confidence:.2%}")
            print(f"  Expected: {'Low' if query == 'xyz abc def' else 'High'}")
            print(f"  Status: {'✅ PASS' if success else '❌ FAIL'}")
            
            self.test_results.append(('confidence_scores', query, success))
    
    def run_all_tests(self):
        """Run all ML tests"""
        print("\n" + "=" * 70)
        print("YatriSetu ML Models Test Suite")
        print("=" * 70)
        
        if not self.load_models():
            print("\n❌ Failed to load models. Train models first:")
            print("   python ml/db_trainer.py")
            return 0, 1
        
        self.test_intent_classification()
        self.test_entity_extraction()
        self.test_location_matching()
        self.test_confidence_scores()
        
        # Summary
        total = len(self.test_results)
        passed = sum(1 for _, _, success in self.test_results if success)
        failed = total - passed
        
        print("\n" + "=" * 70)
        print("Test Summary")
        print("=" * 70)
        print(f"\n✅ Passed: {passed}/{total} ({passed/total*100:.1f}%)")
        print(f"❌ Failed: {failed}/{total}")
        
        if failed > 0:
            print("\nFailed tests:")
            for category, query, success in self.test_results:
                if not success:
                    print(f"  • {category}: {query}")
        
        return passed, failed

def main():
    """Run ML tests"""
    tester = TestMLModels()
    passed, failed = tester.run_all_tests()
    
    if failed == 0:
        print("\n🎉 All ML tests passed!")
    else:
        print(f"\n⚠️ {failed} test(s) failed")
    
    return failed == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
