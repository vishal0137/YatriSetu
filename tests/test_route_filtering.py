"""
Test Route Filtering Feature
Tests the context-based filtering for cheapest/fastest routes
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.chatbot import chatbot

# Create Flask app context
app = create_app()
app.app_context().push()

def test_route_filtering():
    """Test context-based route filtering"""
    
    print("\n" + "="*70)
    print("Testing Route Filtering Feature")
    print("="*70)
    
    user_id = 'test_filter_user'
    
    # Test 1: Search for routes first
    print("\n1. Searching for routes from CP to Airport...")
    response1 = chatbot.process_message(user_id, 'route from CP to Airport')
    
    if response1.get('routes'):
        print(f"   ✅ Found {len(response1['routes'])} routes")
        print(f"   Suggestions: {response1.get('suggestions', [])}")
    else:
        print(f"   ❌ No routes found")
        return False
    
    # Test 2: Filter by cheapest route
    print("\n2. Filtering by cheapest route...")
    response2 = chatbot.process_message(user_id, 'cheapest route')
    
    if response2.get('type') == 'route_list':
        print(f"   ✅ Cheapest route filter works")
        print(f"   Message preview: {response2['message'][:100]}...")
        print(f"   Suggestions: {response2.get('suggestions', [])}")
        
        # Verify suggestions match backend
        expected_suggestions = ['Book Ticket', 'Fastest Route', 'All Routes', 'New Search']
        if response2.get('suggestions') == expected_suggestions:
            print(f"   ✅ Suggestions match backend exactly")
        else:
            print(f"   ❌ Suggestions mismatch!")
            print(f"      Expected: {expected_suggestions}")
            print(f"      Got: {response2.get('suggestions')}")
            return False
    else:
        print(f"   ❌ Cheapest route filter failed")
        print(f"   Response: {response2.get('message')}")
        return False
    
    # Test 3: Filter by fastest route
    print("\n3. Filtering by fastest route...")
    response3 = chatbot.process_message(user_id, 'fastest route')
    
    if response3.get('type') == 'route_list':
        print(f"   ✅ Fastest route filter works")
        print(f"   Message preview: {response3['message'][:100]}...")
        print(f"   Suggestions: {response3.get('suggestions', [])}")
        
        # Verify suggestions match backend
        expected_suggestions = ['Book Ticket', 'Cheapest Route', 'All Routes', 'New Search']
        if response3.get('suggestions') == expected_suggestions:
            print(f"   ✅ Suggestions match backend exactly")
        else:
            print(f"   ❌ Suggestions mismatch!")
            print(f"      Expected: {expected_suggestions}")
            print(f"      Got: {response3.get('suggestions')}")
            return False
    else:
        print(f"   ❌ Fastest route filter failed")
        print(f"   Response: {response3.get('message')}")
        return False
    
    # Test 4: Show all routes again
    print("\n4. Showing all routes...")
    response4 = chatbot.process_message(user_id, 'all routes')
    
    if response4.get('routes'):
        print(f"   ✅ All routes displayed")
        print(f"   Found {len(response4['routes'])} routes")
    else:
        print(f"   ❌ All routes failed")
        return False
    
    # Test 5: Try filtering without prior search
    print("\n5. Testing filter without prior search...")
    new_user_id = 'test_no_search_user'
    response5 = chatbot.process_message(new_user_id, 'cheapest route')
    
    if 'search for routes first' in response5.get('message', '').lower():
        print(f"   ✅ Proper error message shown")
        print(f"   Message: {response5['message']}")
    else:
        print(f"   ❌ Should show error when no prior search")
        print(f"   Response: {response5.get('message')}")
        return False
    
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print("\n✅ All route filtering tests passed!")
    print()
    
    return True

if __name__ == '__main__':
    success = test_route_filtering()
    exit(0 if success else 1)
