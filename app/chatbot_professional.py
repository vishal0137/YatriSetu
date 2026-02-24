# Professional Typography Replacements for Chatbot
# This file contains all the emoji-to-professional text mappings

EMOJI_REPLACEMENTS = {
    '🚌': 'BUS',
    '💰': 'FARE',
    '⚡': 'FAST',
    '📍': 'LOCATION',
    '🔥': 'POPULAR',
    '⭐': 'FEATURED',
    '💵': 'COST',
    '📏': 'DISTANCE',
    '⏱️': 'TIME',
    '🛣️': 'ROUTE',
    '🎯': 'DESTINATION',
    '📊': 'STATS',
    '🚏': 'STOPS',
    '✅': '[Active]',
    '❌': '[Inactive]',
    '🎫': 'TICKET',
    '🔍': 'SEARCH',
    '❓': 'HELP',
    '🔄': 'REFRESH',
    '❄️': 'AC',
}

def remove_emojis_from_message(message):
    """Remove all emojis from message and replace with professional text"""
    for emoji, replacement in EMOJI_REPLACEMENTS.items():
        message = message.replace(emoji, replacement)
    return message
