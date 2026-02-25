"""
YatriSetu Models Package
Contains all core models and processors for the YatriSetu Smart Transit Platform
"""

# Database ORM Models
from .database_models import User, Bus, Route, Booking

# Core Processing Models
from .chatbot import Chatbot
from .data_extractor import DataExtractor
from .unified_data_processor import UnifiedDataProcessor

__all__ = [
    # Database Models
    'User',
    'Bus', 
    'Route',
    'Booking',
    # Processing Models
    'Chatbot',
    'DataExtractor',
    'UnifiedDataProcessor'
]

__version__ = '1.0.0'
__author__ = 'YatriSetu Development Team'
