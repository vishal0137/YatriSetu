from flask import Blueprint, render_template, request, jsonify, session
from app.chatbot import chatbot
import uuid

bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@bp.route('/')
def chatbot_page():
    """Render chatbot interface"""
    # Generate session ID for user
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    return render_template('chatbot/chat.html')

@bp.route('/api/message', methods=['POST'])
def process_message():
    """Process user message and return bot response"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Get or create user session
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
        
        user_id = session['user_id']
        
        # Process message through chatbot
        response = chatbot.process_message(user_id, user_message)
        
        return jsonify({
            'success': True,
            'response': response
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation context"""
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            if user_id in chatbot.user_context:
                del chatbot.user_context[user_id]
        
        return jsonify({
            'success': True,
            'message': 'Conversation reset'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    """Get context-aware suggestions"""
    try:
        data = request.get_json()
        context = data.get('context', 'initial')
        
        suggestions_map = {
            'initial': [
                'Find a route',
                'Check fare',
                'Track bus',
                'Popular routes'
            ],
            'route_search': [
                'Fastest route',
                'Cheapest route',
                'AC buses only',
                'Alternative routes'
            ],
            'location': [
                'Connaught Place',
                'IGI Airport',
                'Kashmere Gate',
                'Anand Vihar'
            ],
            'help': [
                'How to book?',
                'Ticket types',
                'Bus statistics',
                'Contact support'
            ]
        }
        
        suggestions = suggestions_map.get(context, suggestions_map['initial'])
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/mock-conversation', methods=['GET'])
def get_mock_conversation():
    """Get a mock conversation for demo purposes"""
    try:
        mock_messages = [
            {
                'sender': 'bot',
                'message': 'Namaste! Welcome to YatriSetu! How can I help you today?',
                'suggestions': ['Find Route', 'Check Fare', 'Track Bus']
            },
            {
                'sender': 'user',
                'message': 'I want to go from Connaught Place to IGI Airport'
            },
            {
                'sender': 'bot',
                'message': 'Routes: Connaught Place → IGI Airport\nFound 3 route(s)\n\n1. Bus 780 (AC)\n   ₹50 | 18.5 km\n   Most Used\n\n2. Bus 764 (Non-AC)\n   ₹25 | 19.2 km\n\n3. Bus 615 (Non-AC)\n   ₹25 | 20.1 km',
                'routes': [
                    {
                        'route_number': '780',
                        'bus_type': 'AC',
                        'start_location': 'Connaught Place',
                        'end_location': 'IGI Airport',
                        'fare': 50,
                        'distance': 18.5,
                        'duration': 46
                    },
                    {
                        'route_number': '764',
                        'bus_type': 'Non-AC',
                        'start_location': 'Connaught Place',
                        'end_location': 'IGI Airport',
                        'fare': 25,
                        'distance': 19.2,
                        'duration': 48
                    }
                ],
                'suggestions': ['Book Ticket', 'Track Bus', 'New Search']
            }
        ]
        
        return jsonify({
            'success': True,
            'messages': mock_messages
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
