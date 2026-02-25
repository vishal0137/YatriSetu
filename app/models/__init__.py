"""
YatriSetu Models Package
Contains all core models for the YatriSetu Smart Transit Platform
"""

# Database ORM Models
from .database_models import User, Bus, Route, Booking, Payment, LiveBusLocation, Wallet, Stop, Driver, Conductor

# Core Processing Models
from .chatbot import SamparkChatbot, chatbot

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
    'chatbot'
]

__version__ = '1.0.0'
__author__ = 'YatriSetu Development Team'
