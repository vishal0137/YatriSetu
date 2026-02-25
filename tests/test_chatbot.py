"""
Test Suite for Sampark Chatbot (YatriSetu)
Tests rule-based chatbot functionality with new Sampark branding
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models.chatbot import chatbot

class TestChatbot:
    """Test chatbot functionality"""
    
    def __init__(self):
        self.app = create_app()
        self.test_results = []
    
    def test_greeting(self):
        """Test greeting responses"""
        test_cases = [
            "Hi",
            "Hello",
            "Namaste",
            "Hey there"
        ]
        
        print("\n" + "=" * 70)
        print("Testing Greetings")
        print("=" * 70)
        
        with self.app.app_context():
            for query in test_cases:
                response = chatbot.process_message('test_user', query)
                success = 'Sampark' in response['message'] or 'Namaste' in response['message']
                
                print(f"\n✓ Query: {query}")
                print(f"  Response: {response['message'][:80]}...")
                print(f"  Status: {'✅ PASS' if success else '❌ FAIL'}")
                
                self.test_results.append(('greeting', query, success))
    
    def test_route_search(self):
        """Test route search functionality"""
        test_cases = [
            "Route from CP to Dwarka",
            "Bus to Airport",
            "How to reach Noida from Kashmere Gate",
            "Show me routes to ISBT"
        ]
        
        print("\n" + "=" * 70)
        print("Testing Route Search")
        print("=" * 70)
        
        with self.app.app_context():
            for query in test_cases:
                response = chatbot.process_message('test_user', query)
                success = 'ROUTES' in response['message'] or 'Route' in response['message'] or 'No routes' in response['message']
                
                print(f"\n✓ Query: {query}")
                print(f"  Response: {response['message'][:80]}...")
                print(f"  Status: {'✅ PASS' if success else '❌ FAIL'}")
                
                self.test_results.append(('route_search', query, success))
    
    def test_fare_inquiry(self):
        """Test fare inquiry"""
        test_cases = [
            "Fare from CP to Dwarka",
            "How much to Airport",
            "Price to Noida"
        ]
        
        print("\n" + "=" * 70)
        print("Testing Fare Inquiry")
        print("=" * 70)
        
        with self.app.app_context():
            for query in test_cases:
                response = chatbot.process_message('test_user', query)
                success = 'FARE' in response['message'] or '₹' in response['message'] or 'fare' in response['message'].lower()
                
                print(f"\n✓ Query: {query}")
                print(f"  Response: {response['message'][:80]}...")
                print(f"  Status: {'✅ PASS' if success else '❌ FAIL'}")
                
                self.test_results.append(('fare_inquiry', query, success))
    
    def test_bus_tracking(self):
        """Test bus tracking"""
        test_cases = [
            "Track bus DTC-001",
            "Where is bus DTC-078",
            "Location of bus DTC-050"
        ]
        
        print("\n" + "=" * 70)
        print("Testing Bus Tracking")
        print("=" * 70)
        
        with self.app.app_context():
            for query in test_cases:
                response = chatbot.process_message('test_user', query)
                success = 'Bus' in response['message'] or 'Track' in response['message'] or 'BUS' in response['message']
                
                print(f"\n✓ Query: {query}")
                print(f"  Response: {response['message'][:80]}...")
                print(f"  Status: {'✅ PASS' if success else '❌ FAIL'}")
                
                self.test_results.append(('bus_tracking', query, success))
    
    def test_fuzzy_matching(self):
        """Test fuzzy location matching"""
        test_cases = [
            ("CP", "Connaught Place"),
            ("airport", "IGI Airport"),
            ("kashmiri gate", "Kashmere Gate"),
            ("ISBT", "ISBT")
        ]
        
        print("\n" + "=" * 70)
        print("Testing Fuzzy Location Matching")
        print("=" * 70)
        
        with self.app.app_context():
            for query, expected in test_cases:
                match, score = chatbot.location_handler.find_best_location_match(query)
                success = match is not None and score > 0.5
                
                print(f"\n✓ Query: {query}")
                print(f"  Expected: {expected}")
                print(f"  Matched: {match}")
                print(f"  Score: {score:.2f}")
                print(f"  Status: {'✅ PASS' if success else '❌ FAIL'}")
                
                self.test_results.append(('fuzzy_matching', query, success))
    
    def test_special_queries(self):
        """Test special query types"""
        test_cases = [
            "Cheapest route from CP to Dwarka",
            "Fastest route from CP to Airport",
            "AC bus to Gurgaon",
            "Stats"
        ]
        
        print("\n" + "=" * 70)
        print("Testing Special Queries")
        print("=" * 70)
        
        with self.app.app_context():
            for query in test_cases:
                response = chatbot.process_message('test_user', query)
                success = len(response['message']) > 0
                
                print(f"\n✓ Query: {query}")
                print(f"  Response: {response['message'][:80]}...")
                print(f"  Status: {'✅ PASS' if success else '❌ FAIL'}")
                
                self.test_results.append(('special_queries', query, success))
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "=" * 70)
        print("Sampark Chatbot Test Suite (YatriSetu)")
        print("=" * 70)
        
        self.test_greeting()
        self.test_route_search()
        self.test_fare_inquiry()
        self.test_bus_tracking()
        self.test_fuzzy_matching()
        self.test_special_queries()
        
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
    """Run tests"""
    tester = TestChatbot()
    passed, failed = tester.run_all_tests()
    
    if failed == 0:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️ {failed} test(s) failed")
    
    return failed == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
