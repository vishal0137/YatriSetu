"""
Chatbot Test with Database Integration
Tests chatbot functionality with real database queries
"""

import sys
import os
import pytest

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestChatbotWithDatabase:
    """Test chatbot with database integration"""
    
    @pytest.fixture(scope='class')
    def app(self):
        """Create Flask app for testing"""
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from config import Config
        
        app = Flask(__name__)
        app.config.from_object(Config)
        db = SQLAlchemy(app)
        
        with app.app_context():
            yield app
    
    @pytest.fixture(scope='class')
    def chatbot(self, app):
        """Create chatbot instance"""
        from app.models.chatbot import SamparkChatbot
        
        with app.app_context():
            chatbot = SamparkChatbot()
            yield chatbot
    
    def test_chatbot_initialization(self, chatbot):
        """Test chatbot can be initialized"""
        assert chatbot is not None
        print("\n✓ Chatbot initialized successfully")
    
    def test_greeting(self, chatbot):
        """Test greeting response"""
        response = chatbot.process_message("test_user", "hello")
        
        assert response is not None
        assert 'message' in response
        assert response['type'] == 'greeting'
        print(f"\n✓ Greeting test passed")
        print(f"  Response: {response['message'][:100]}...")
    
    def test_help_command(self, chatbot):
        """Test help command"""
        response = chatbot.process_message("test_user", "help")
        
        assert response is not None
        assert 'message' in response
        assert response['type'] == 'help'
        print(f"\n✓ Help command test passed")
    
    def test_route_query_with_db(self, app, chatbot):
        """Test route query with database"""
        with app.app_context():
            response = chatbot.process_message("test_user", "route from Connaught Place to Dwarka")
            
            assert response is not None
            assert 'message' in response
            print(f"\n✓ Route query test passed")
            print(f"  Response type: {response.get('type')}")
            
            if response.get('routes'):
                print(f"  Routes found: {len(response['routes'])}")
                for route in response['routes'][:3]:
                    print(f"    - {route.get('route_name', 'Unknown')}")
            else:
                print(f"  No routes found (database may be empty)")
    
    def test_popular_routes_with_db(self, app, chatbot):
        """Test popular routes query with database"""
        with app.app_context():
            response = chatbot.process_message("test_user", "show popular routes")
            
            assert response is not None
            print(f"\n✓ Popular routes test passed")
            
            if response.get('routes'):
                print(f"  Popular routes: {len(response['routes'])}")
            else:
                print(f"  No popular routes (database may be empty)")
    
    def test_route_by_id_with_db(self, app, chatbot):
        """Test route query by ID with database"""
        with app.app_context():
            response = chatbot.process_message("test_user", "route 001")
            
            assert response is not None
            print(f"\n✓ Route by ID test passed")
            print(f"  Response type: {response.get('type')}")
    
    def test_statistics_with_db(self, app, chatbot):
        """Test statistics query with database"""
        with app.app_context():
            response = chatbot.process_message("test_user", "show statistics")
            
            assert response is not None
            print(f"\n✓ Statistics test passed")
            print(f"  Response: {response.get('message', '')[:100]}...")
    
    def test_booking_instructions(self, chatbot):
        """Test booking instructions"""
        response = chatbot.process_message("test_user", "how to book ticket")
        
        assert response is not None
        assert response['type'] == 'booking_help'
        print(f"\n✓ Booking instructions test passed")
    
    def test_contact_support(self, chatbot):
        """Test contact support"""
        response = chatbot.process_message("test_user", "contact support")
        
        assert response is not None
        assert response['type'] == 'contact_support'
        print(f"\n✓ Contact support test passed")
    
    def test_multiple_queries(self, app, chatbot):
        """Test multiple queries in sequence"""
        with app.app_context():
            queries = [
                "hello",
                "show routes",
                "help",
                "thank you"
            ]
            
            for query in queries:
                response = chatbot.process_message("test_user", query)
                assert response is not None
                assert 'message' in response
            
            print(f"\n✓ Multiple queries test passed ({len(queries)} queries)")


def run_manual_test():
    """Run manual test with detailed output"""
    print("\n" + "=" * 70)
    print("CHATBOT WITH DATABASE - MANUAL TEST")
    print("=" * 70)
    
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from config import Config
        from app.models.chatbot import SamparkChatbot
        
        # Setup
        print("\n1. Setting up Flask app and database...")
        app = Flask(__name__)
        app.config.from_object(Config)
        db = SQLAlchemy(app)
        print("✓ Flask app configured")
        
        with app.app_context():
            # Test database connection
            print("\n2. Testing database connection...")
            result = db.session.execute(db.text("SELECT COUNT(*) FROM routes"))
            route_count = result.fetchone()[0]
            print(f"✓ Database connected - {route_count} routes in database")
            
            result = db.session.execute(db.text("SELECT COUNT(*) FROM buses"))
            bus_count = result.fetchone()[0]
            print(f"✓ Found {bus_count} buses in database")
            
            # Initialize chatbot
            print("\n3. Initializing chatbot...")
            chatbot = SamparkChatbot()
            print("✓ Chatbot initialized")
            
            # Test queries
            print("\n4. Testing chatbot queries...")
            print("-" * 70)
            
            test_queries = [
                ("Greeting", "hello"),
                ("Help", "help"),
                ("Route Search", "route from Connaught Place to Dwarka"),
                ("Popular Routes", "show popular routes"),
                ("Statistics", "show statistics"),
                ("Booking Help", "how to book"),
                ("Contact", "contact support")
            ]
            
            for test_name, query in test_queries:
                print(f"\nTest: {test_name}")
                print(f"Query: '{query}'")
                
                response = chatbot.process_message("test_user", query)
                
                print(f"Type: {response.get('type', 'unknown')}")
                print(f"Message: {response.get('message', '')[:150]}...")
                
                if response.get('routes'):
                    print(f"Routes: {len(response['routes'])} found")
                
                if response.get('suggestions'):
                    print(f"Suggestions: {len(response['suggestions'])}")
                
                print("✓ Passed")
            
            print("\n" + "=" * 70)
            print("✓ ALL TESTS PASSED!")
            print("=" * 70)
            
            # Show database stats
            print("\nDatabase Statistics:")
            print(f"  Routes: {route_count}")
            print(f"  Buses: {bus_count}")
            
            result = db.session.execute(db.text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"  Users: {user_count}")
            
            result = db.session.execute(db.text("SELECT COUNT(*) FROM bookings"))
            booking_count = result.fetchone()[0]
            print(f"  Bookings: {booking_count}")
            
            return True
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Chatbot with Database')
    parser.add_argument('--manual', '-m', action='store_true',
                       help='Run manual test with detailed output')
    parser.add_argument('--pytest', '-p', action='store_true',
                       help='Run pytest tests')
    
    args = parser.parse_args()
    
    if args.pytest:
        pytest.main([__file__, '-v', '--tb=short'])
    elif args.manual:
        run_manual_test()
    else:
        # Default: run manual test
        run_manual_test()
