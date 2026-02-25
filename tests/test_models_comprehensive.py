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
            User, Bus, Route, Booking,
            Chatbot, DataExtractor, UnifiedDataProcessor
        )
        
        assert User is not None
        assert Bus is not None
        assert Route is not None
        assert Booking is not None
        assert Chatbot is not None
        assert DataExtractor is not None
        assert UnifiedDataProcessor is not None
    
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
        """Test User model can be imported"""
        from app.models.database_models import User
        assert User is not None
        assert hasattr(User, '__tablename__')
        assert User.__tablename__ == 'users'
    
    def test_user_model_attributes(self):
        """Test User model has required attributes"""
        from app.models.database_models import User
        
        required_attrs = [
            'id', 'email', 'phone', 'full_name', 
            'hashed_password', 'role', 'is_active',
            'created_at', 'updated_at'
        ]
        
        for attr in required_attrs:
            assert hasattr(User, attr), f"User model missing attribute: {attr}"
    
    def test_bus_model_exists(self):
        """Test Bus model can be imported"""
        from app.models.database_models import Bus
        assert Bus is not None
        assert hasattr(Bus, '__tablename__')
        assert Bus.__tablename__ == 'buses'
    
    def test_bus_model_attributes(self):
        """Test Bus model has required attributes"""
        from app.models.database_models import Bus
        
        required_attrs = [
            'id', 'bus_number', 'registration_number',
            'capacity', 'bus_type', 'is_active',
            'created_at', 'updated_at'
        ]
        
        for attr in required_attrs:
            assert hasattr(Bus, attr), f"Bus model missing attribute: {attr}"
    
    def test_route_model_exists(self):
        """Test Route model can be imported"""
        from app.models.database_models import Route
        assert Route is not None
        assert hasattr(Route, '__tablename__')
        assert Route.__tablename__ == 'routes'
    
    def test_route_model_attributes(self):
        """Test Route model has required attributes"""
        from app.models.database_models import Route
        
        required_attrs = [
            'id', 'route_number', 'route_name',
            'start_location', 'end_location',
            'distance_km', 'estimated_duration_minutes',
            'fare', 'is_active', 'created_at', 'updated_at'
        ]
        
        for attr in required_attrs:
            assert hasattr(Route, attr), f"Route model missing attribute: {attr}"
    
    def test_booking_model_exists(self):
        """Test Booking model can be imported"""
        from app.models.database_models import Booking
        assert Booking is not None
        assert hasattr(Booking, '__tablename__')
        assert Booking.__tablename__ == 'bookings'
    
    def test_stop_model_exists(self):
        """Test Stop model can be imported"""
        from app.models.database_models import Stop
        assert Stop is not None
        assert hasattr(Stop, '__tablename__')
        assert Stop.__tablename__ == 'stops'
    
    def test_driver_model_exists(self):
        """Test Driver model can be imported"""
        from app.models.database_models import Driver
        assert Driver is not None
        assert hasattr(Driver, '__tablename__')
        assert Driver.__tablename__ == 'drivers'
    
    def test_conductor_model_exists(self):
        """Test Conductor model can be imported"""
        from app.models.database_models import Conductor
        assert Conductor is not None
        assert hasattr(Conductor, '__tablename__')
        assert Conductor.__tablename__ == 'conductors'
    
    def test_payment_model_exists(self):
        """Test Payment model can be imported"""
        from app.models.database_models import Payment
        assert Payment is not None
        assert hasattr(Payment, '__tablename__')
        assert Payment.__tablename__ == 'payments'
    
    def test_wallet_model_exists(self):
        """Test Wallet model can be imported"""
        from app.models.database_models import Wallet
        assert Wallet is not None
        assert hasattr(Wallet, '__tablename__')
        assert Wallet.__tablename__ == 'wallets'
    
    def test_live_bus_location_model_exists(self):
        """Test LiveBusLocation model can be imported"""
        from app.models.database_models import LiveBusLocation
        assert LiveBusLocation is not None
        assert hasattr(LiveBusLocation, '__tablename__')
        assert LiveBusLocation.__tablename__ == 'live_bus_locations'


class TestChatbotModel:
    """Test Chatbot processing model"""
    
    def test_chatbot_import(self):
        """Test Chatbot can be imported"""
        from app.models.chatbot import Chatbot
        assert Chatbot is not None
    
    def test_chatbot_instantiation(self):
        """Test Chatbot can be instantiated"""
        from app.models.chatbot import Chatbot
        chatbot = Chatbot()
        assert chatbot is not None
    
    def test_chatbot_has_process_message(self):
        """Test Chatbot has process_message method"""
        from app.models.chatbot import Chatbot
        chatbot = Chatbot()
        assert hasattr(chatbot, 'process_message')
        assert callable(chatbot.process_message)
    
    def test_chatbot_process_message_returns_dict(self):
        """Test process_message returns dictionary"""
        from app.models import Chatbot
        chatbot_instance = Chatbot()
        
        # Test with simple message (requires user_id and message)
        response = chatbot_instance.process_message("test_user", "Hello")
        assert isinstance(response, dict)
        assert 'message' in response or 'response' in response
    
    def test_chatbot_has_required_methods(self):
        """Test Chatbot has all required methods"""
        from app.models import Chatbot
        chatbot_instance = Chatbot()
        
        required_methods = [
            'process_message',
            'greeting_response'
        ]
        
        for method in required_methods:
            assert hasattr(chatbot_instance, method), f"Chatbot missing method: {method}"


class TestDataExtractor:
    """Test DataExtractor model"""
    
    def test_data_extractor_import(self):
        """Test DataExtractor can be imported"""
        from app.models.data_extractor import DataExtractor
        assert DataExtractor is not None
    
    def test_data_extractor_instantiation(self):
        """Test DataExtractor can be instantiated"""
        from app.models.data_extractor import DataExtractor
        extractor = DataExtractor()
        assert extractor is not None
    
    def test_data_extractor_has_extracted_data(self):
        """Test DataExtractor has extracted_data attribute"""
        from app.models.data_extractor import DataExtractor
        extractor = DataExtractor()
        
        assert hasattr(extractor, 'extracted_data')
        assert isinstance(extractor.extracted_data, dict)
        assert 'buses' in extractor.extracted_data
        assert 'routes' in extractor.extracted_data
        assert 'fares' in extractor.extracted_data
        assert 'stops' in extractor.extracted_data
    
    def test_data_extractor_has_preview_data(self):
        """Test DataExtractor has preview_data attribute"""
        from app.models.data_extractor import DataExtractor
        extractor = DataExtractor()
        
        assert hasattr(extractor, 'preview_data')
        assert isinstance(extractor.preview_data, dict)
    
    def test_data_extractor_has_validation_errors(self):
        """Test DataExtractor has validation_errors attribute"""
        from app.models.data_extractor import DataExtractor
        extractor = DataExtractor()
        
        assert hasattr(extractor, 'validation_errors')
        assert isinstance(extractor.validation_errors, list)
    
    def test_data_extractor_has_duplicate_checks(self):
        """Test DataExtractor has duplicate_checks attribute"""
        from app.models.data_extractor import DataExtractor
        extractor = DataExtractor()
        
        assert hasattr(extractor, 'duplicate_checks')
        assert isinstance(extractor.duplicate_checks, list)
    
    def test_data_extractor_has_required_methods(self):
        """Test DataExtractor has all required methods"""
        from app.models.data_extractor import DataExtractor
        extractor = DataExtractor()
        
        required_methods = [
            'analyze_csv_structure',
            'extract_buses_from_csv',
            'extract_routes_from_csv',
            'extract_fares_from_csv',
            'extract_stops_from_csv',
            'extract_from_pdf',
            'check_duplicates_in_database',
            'get_preview_data',
            'update_preview_record',
            'get_validation_report',
            'export_to_csv',
            'insert_to_database'
        ]
        
        for method in required_methods:
            assert hasattr(extractor, method), f"DataExtractor missing method: {method}"
            assert callable(getattr(extractor, method))
    
    def test_data_extractor_expected_schemas(self):
        """Test DataExtractor has expected schemas"""
        from app.models.data_extractor import DataExtractor
        extractor = DataExtractor()
        
        assert hasattr(extractor, 'expected_schemas')
        assert 'buses' in extractor.expected_schemas
        assert 'routes' in extractor.expected_schemas
        assert 'fares' in extractor.expected_schemas
        assert 'stops' in extractor.expected_schemas
    
    def test_data_extractor_valid_categories(self):
        """Test DataExtractor has valid categories"""
        from app.models.data_extractor import DataExtractor
        extractor = DataExtractor()
        
        assert hasattr(extractor, 'valid_categories')
        assert 'bus_type' in extractor.valid_categories
        assert 'status' in extractor.valid_categories
        assert 'passenger_type' in extractor.valid_categories
    
    def test_data_extractor_validation_report(self):
        """Test get_validation_report returns correct structure"""
        from app.models.data_extractor import DataExtractor
        extractor = DataExtractor()
        
        report = extractor.get_validation_report()
        assert isinstance(report, dict)
        assert 'total_errors' in report
        assert 'total_warnings' in report
        assert 'errors' in report
        assert 'warnings' in report
        assert 'duplicates' in report
        assert 'extracted_counts' in report


class TestUnifiedDataProcessor:
    """Test UnifiedDataProcessor model"""
    
    def test_unified_processor_import(self):
        """Test UnifiedDataProcessor can be imported"""
        from app.models.unified_data_processor import UnifiedDataProcessor
        assert UnifiedDataProcessor is not None
    
    def test_unified_processor_instantiation(self):
        """Test UnifiedDataProcessor can be instantiated"""
        from app.models.unified_data_processor import UnifiedDataProcessor
        processor = UnifiedDataProcessor()
        assert processor is not None
    
    def test_unified_processor_has_required_methods(self):
        """Test UnifiedDataProcessor has all required methods"""
        from app.models.unified_data_processor import UnifiedDataProcessor
        processor = UnifiedDataProcessor()
        
        required_methods = [
            'process_pdf',
            'export_to_csv',
            'get_all_data',
            'get_validation_report'
        ]
        
        for method in required_methods:
            assert hasattr(processor, method), f"UnifiedDataProcessor missing method: {method}"
            assert callable(getattr(processor, method))
    
    def test_unified_processor_has_data_storage(self):
        """Test UnifiedDataProcessor has data storage"""
        from app.models.unified_data_processor import UnifiedDataProcessor
        processor = UnifiedDataProcessor()
        
        data = processor.get_all_data()
        assert isinstance(data, dict)


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
    
    def test_data_extractor_uses_database_models(self):
        """Test DataExtractor can access database models"""
        try:
            from app.models.data_extractor import DataExtractor
            from app.models.database_models import Bus, Route, Stop
            
            # This should not raise an error
            extractor = DataExtractor()
            assert True
        except ImportError as e:
            pytest.fail(f"DataExtractor cannot import database models: {e}")
    
    def test_all_models_accessible_from_package(self):
        """Test all models can be imported from package"""
        try:
            from app.models import (
                User, Bus, Route, Booking, Payment, 
                Stop, Driver, Conductor, Wallet, LiveBusLocation,
                Chatbot, DataExtractor, UnifiedDataProcessor
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
    
    def test_data_extractor_has_docstring(self):
        """Test DataExtractor class has docstring"""
        from app.models.data_extractor import DataExtractor
        assert DataExtractor.__doc__ is not None
    
    def test_unified_processor_has_docstring(self):
        """Test UnifiedDataProcessor class has docstring"""
        from app.models.unified_data_processor import UnifiedDataProcessor
        assert UnifiedDataProcessor.__doc__ is not None
    
    def test_models_readme_exists(self):
        """Test models README.md exists"""
        readme_path = os.path.join('app', 'models', 'README.md')
        assert os.path.exists(readme_path), "models/README.md not found"


class TestErrorHandling:
    """Test error handling in models"""
    
    def test_data_extractor_handles_invalid_file(self):
        """Test DataExtractor handles invalid file gracefully"""
        from app.models.data_extractor import DataExtractor
        extractor = DataExtractor()
        
        with pytest.raises(Exception):
            extractor.analyze_csv_structure('nonexistent_file.csv')
    
    def test_data_extractor_handles_invalid_category(self):
        """Test DataExtractor handles invalid category"""
        from app.models.data_extractor import DataExtractor
        extractor = DataExtractor()
        
        with pytest.raises(ValueError):
            extractor.export_to_csv('invalid_category', 'output.csv')
    
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
    print()
    
    # Run pytest
    pytest_args = [
        __file__,
        '-v',  # Verbose
        '--tb=short',  # Short traceback
        '-s',  # Show print statements
    ]
    
    result = pytest.main(pytest_args)
    
    print()
    print("=" * 70)
    if result == 0:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed. Please review the output above.")
    print("=" * 70)
    
    return result


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
