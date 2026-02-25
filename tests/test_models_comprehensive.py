"""
Comprehensive Tests for YatriSetu Models Package
Tests all models in app/models/ folder
"""

import pytest
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestModelsPackage:
    """Test models package structure and imports"""
    
    def test_models_package_exists(self):
        """Test that models package exists"""
        import app.models
        assert app.models is not None
    
    def test_models_init_imports(self):
        """Test that __init__.py exports all required models"""
        from app.models import (
            User, Bus, Route, Booking, Chatbot
        )
        
        assert User is not None
        assert Bus is not None
        assert Route is not None
        assert Booking is not None
        assert Chatbot is not None
    
    def test_models_version(self):
        """Test that package has version"""
        from app.models import __version__
        assert __version__ == '1.0.0'
    
    def test_models_author(self):
        """Test that package has author"""
        from app.models import __author__
        assert 'YatriSetu' in __author__


class TestDatabaseModels:
    """Test database ORM models"""
    
    def test_user_model_exists(self):
        """Test User model exists"""
        from app.models.database_models import User
        assert User is not None
    
    def test_user_model_attributes(self):
        """Test User model has required attributes"""
        from app.models.database_models import User
        
        required_attrs = ['id', 'email', 'phone', 'full_name', 'hashed_password', 'role']
        for attr in required_attrs:
            assert hasattr(User, attr), f"User model missing attribute: {attr}"
    
    def test_bus_model_exists(self):
        """Test Bus model exists"""
        from app.models.database_models import Bus
        assert Bus is not None
    
    def test_bus_model_attributes(self):
        """Test Bus model has required attributes"""
        from app.models.database_models import Bus
        
        required_attrs = ['id', 'bus_number', 'registration_number', 'capacity', 'bus_type']
        for attr in required_attrs:
            assert hasattr(Bus, attr), f"Bus model missing attribute: {attr}"
    
    def test_route_model_exists(self):
        """Test Route model exists"""
        from app.models.database_models import Route
        assert Route is not None
    
    def test_route_model_attributes(self):
        """Test Route model has required attributes"""
        from app.models.database_models import Route
        
        required_attrs = ['id', 'route_number', 'route_name', 'start_location', 'end_location']
        for attr in required_attrs:
            assert hasattr(Route, attr), f"Route model missing attribute: {attr}"
    
    def test_booking_model_exists(self):
        """Test Booking model exists"""
        from app.models.database_models import Booking
        assert Booking is not None
    
    def test_stop_model_exists(self):
        """Test Stop model exists"""
        from app.models.database_models import Stop
        assert Stop is not None
    
    def test_driver_model_exists(self):
        """Test Driver model exists"""
        from app.models.database_models import Driver
        assert Driver is not None
    
    def test_conductor_model_exists(self):
        """Test Conductor model exists"""
        from app.models.database_models import Conductor
        assert Conductor is not None
    
    def test_payment_model_exists(self):
        """Test Payment model exists"""
        from app.models.database_models import Payment
        assert Payment is not None
    
    def test_wallet_model_exists(self):
        """Test Wallet model exists"""
        from app.models.database_models import Wallet
        assert Wallet is not None
    
    def test_live_bus_location_model_exists(self):
        """Test LiveBusLocation model exists"""
        from app.models.database_models import LiveBusLocation
        assert LiveBusLocation is not None


class TestChatbotModel:
    """Test Chatbot model"""
    
    def test_chatbot_import(self):
        """Test Chatbot can be imported"""
        from app.models import Chatbot
        assert Chatbot is not None
    
    def test_chatbot_instantiation(self):
        """Test Chatbot can be instantiated"""
        from app.models import Chatbot
        chatbot = Chatbot()
        assert chatbot is not None
    
    def test_chatbot_has_process_message(self):
        """Test Chatbot has process_message method"""
        from app.models import Chatbot
        chatbot = Chatbot()
        assert hasattr(chatbot, 'process_message')
        assert callable(chatbot.process_message)
    
    def test_chatbot_process_message_returns_dict(self):
        """Test process_message returns dictionary"""
        from app.models import Chatbot
        chatbot = Chatbot()
        
        response = chatbot.process_message("test_user", "hello")
        assert isinstance(response, dict)
    
    def test_chatbot_has_required_methods(self):
        """Test Chatbot has all required methods"""
        from app.models import Chatbot
        chatbot_instance = Chatbot()
        
        required_methods = [
            'process_message',
            'handle_route_query',
            'handle_statistics_query',
            'handle_route_by_id_query',
            'handle_bus_by_id_query',
            'handle_live_tracking',
            'handle_popular_routes',
            'handle_booking_instructions',
            'handle_ticket_types',
            'handle_contact_support',
            'greeting_response',
            'help_response',
            'default_response'
        ]
        
        for method in required_methods:
            assert hasattr(chatbot_instance, method), f"Chatbot missing method: {method}"


class TestModelIntegration:
    """Test integration between models"""
    
    def test_chatbot_uses_database_models(self):
        """Test Chatbot can access database models"""
        try:
            from app.models.chatbot import Chatbot
            from app.models.database_models import Route, Bus
            
            # This should not raise an error
            chatbot = Chatbot()
            assert True
        except ImportError as e:
            pytest.fail(f"Chatbot cannot import database models: {e}")
    
    def test_all_models_accessible_from_package(self):
        """Test all models can be imported from package"""
        try:
            from app.models import (
                User, Bus, Route, Booking, Payment, 
                Stop, Driver, Conductor, Wallet, LiveBusLocation,
                Chatbot
            )
            assert True
        except ImportError as e:
            pytest.fail(f"Cannot import all models from package: {e}")


class TestModelDocumentation:
    """Test model documentation"""
    
    def test_chatbot_has_docstring(self):
        """Test Chatbot class has docstring"""
        from app.models.chatbot import Chatbot
        assert Chatbot.__doc__ is not None
    
    def test_models_readme_exists(self):
        """Test models README.md exists"""
        readme_path = os.path.join('app', 'models', 'README.md')
        assert os.path.exists(readme_path), "models/README.md not found"


class TestErrorHandling:
    """Test error handling in models"""
    
    def test_chatbot_handles_empty_message(self):
        """Test Chatbot handles empty message"""
        from app.models import Chatbot
        chatbot_instance = Chatbot()
        
        response = chatbot_instance.process_message("test_user", "")
        assert isinstance(response, dict)


def run_all_tests():
    """Run all tests and print results"""
    print("=" * 70)
    print("YatriSetu Models Package - Comprehensive Test Suite")
    print("=" * 70)
    
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == '__main__':
    run_all_tests()
