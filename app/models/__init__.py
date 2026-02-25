"""
YatriSetu Models Package
Contains all core models and processors for the YatriSetu Smart Transit Platform
"""

# Database ORM Models
from .database_models import User, Bus, Route, Booking, Payment, LiveBusLocation, Wallet, Stop, Driver, Conductor

# Core Processing Models
from .chatbot import SamparkChatbot, chatbot
from .data_extractor import DataExtractor
from .unified_data_processor import UnifiedDataProcessor

# Backward compatibility alias
Chatbot = SamparkChatbot

__all__ = [
    # Database Models
    'User',
    'Bus', 
    'Route',
    'Booking',
    'Payment',
    'LiveBusLocation',
    'Wallet',
    'Stop',
    'Driver',
    'Conductor',
    # Processing Models
    'SamparkChatbot',
    'Chatbot',  # Alias for backward compatibility
    'chatbot',
    'DataExtractor',
    'UnifiedDataProcessor'
]

__version__ = '1.0.0'
__author__ = 'YatriSetu Development Team'
