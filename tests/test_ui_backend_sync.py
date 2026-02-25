"""
Test UI-Backend Synchronization
Verifies that all UI suggestions match backend responses exactly
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models.chatbot import chatbot

# Create Flask app context
app = create_app()
app.app_context().push()

def test_ui_backend_sync():
    """Test that UI suggestions match backend responses"""
    
    print("\n" + "="*70)
    print("Testing UI-Backend Synchronization")
    print("="*70)
    
    test_cases = [
        {
            'command': 'hi',
            'expected_type': 'greeting',
            'expected_suggestions': ['Route 001', 'Bus DTC-078', 'Find Route', 'Help']
        },
        {
            'command': 'help',
            'expected_type': 'help',
            'expected_suggestions': ['Route 001', 'Bus DTC-078', 'Find Route', 'Stats']
        },
        {
            'command': 'stats',
            'expected_type': 'statistics',
            'expected_suggestions': ['Find Route', 'Track Bus', 'Route 001']
        },
        {
            'command': 'new search',
            'expected_type': 'text',
            'expected_suggestions': ['Find Route', 'Route 001', 'Check Fare', 'Track Bus']
        },
        {
            'command': 'find route',
            'expected_type': 'text',
            'expected_suggestions': ['Connaught Place', 'IGI Airport', 'Kashmere Gate', 'Anand Vihar', 'Dwarka', 'Noida']
        },
        {
            'command': 'check fare',
            'expected_type': 'text',
            'expected_suggestions': ['Connaught Place', 'IGI Airport', 'Kashmere Gate', 'Anand Vihar', 'Dwarka', 'Noida']
        },
        {
            'command': 'popular routes',
            'expected_type': 'popular_routes',
            'expected_suggestions': ['Book Ticket', 'Find Route', 'Stats']
        },
        {
            'command': 'how to book',
            'expected_type': 'booking_help',
            'expected_suggestions': ['Ticket Types', 'General', 'Student', 'Senior Citizen']
        },
        {
            'command': 'ticket types',
            'expected_type': 'ticket_types',
            'expected_suggestions': ['How to Book', 'Check Fare', 'Find Route']
        },
        {
            'command': 'contact support',
            'expected_type': 'contact_support',
            'expected_suggestions': ['How to Book', 'Ticket Types', 'Find Route', 'Stats']
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        command = test['command']
        expected_type = test['expected_type']
        expected_suggestions = test['expected_suggestions']
        
        print(f"\n{i}. Testing: '{command}'")
        
        response = chatbot.process_message('test_user', command)
        
        # Check response type
        actual_type = response.get('type')
        type_match = actual_type == expected_type
        
        # Check suggestions
        actual_suggestions = response.get('suggestions', [])
        suggestions_match = actual_suggestions == expected_suggestions
        
        if type_match and suggestions_match:
            print(f"   ✅ PASS")
            print(f"   Type: {actual_type}")
            print(f"   Suggestions: {actual_suggestions}")
            passed += 1
        else:
            print(f"   ❌ FAIL")
            if not type_match:
                print(f"   Expected type: {expected_type}")
                print(f"   Actual type: {actual_type}")
            if not suggestions_match:
                print(f"   Expected suggestions: {expected_suggestions}")
                print(f"   Actual suggestions: {actual_suggestions}")
            failed += 1
    
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"\n✅ Passed: {passed}/{len(test_cases)}")
    print(f"❌ Failed: {failed}/{len(test_cases)}")
    
    if failed == 0:
        print(f"\n🎉 All tests passed! UI-Backend sync is perfect!")
    else:
        print(f"\n⚠️  Some tests failed. Check the output above.")
    
    print()
    
    return failed == 0

if __name__ == '__main__':
    success = test_ui_backend_sync()
    exit(0 if success else 1)
