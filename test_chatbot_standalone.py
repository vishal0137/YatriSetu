"""
Standalone Chatbot Test Script
Tests chatbot functionality without database connection
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_chatbot_basic():
    """Test basic chatbot functionality"""
    print("=" * 70)
    print("YatriSetu Chatbot - Standalone Test")
    print("=" * 70)
    print()
    
    try:
        from app.models.chatbot import SamparkChatbot
        
        # Initialize chatbot
        print("Initializing chatbot...")
        chatbot = SamparkChatbot()
        print("✓ Chatbot initialized successfully")
        print()
        
        # Test cases
        test_messages = [
            "hello",
            "help",
            "show me routes from Connaught Place to Dwarka",
            "what are the popular routes?",
            "how to book a ticket?",
            "contact support",
            "statistics",
            "thank you"
        ]
        
        print("Running test messages:")
        print("-" * 70)
        
        for i, message in enumerate(test_messages, 1):
            print(f"\nTest {i}: '{message}'")
            print("-" * 70)
            
            try:
                response = chatbot.process_message("test_user", message)
                
                print(f"Response Type: {response.get('type', 'unknown')}")
                print(f"Message: {response.get('message', 'No message')[:200]}")
                
                if response.get('routes'):
                    print(f"Routes Found: {len(response['routes'])}")
                
                if response.get('suggestions'):
                    print(f"Suggestions: {len(response['suggestions'])}")
                
                print("✓ Test passed")
                
            except Exception as e:
                print(f"✗ Test failed: {str(e)}")
        
        print()
        print("=" * 70)
        print("All tests completed!")
        print("=" * 70)
        
    except ImportError as e:
        print(f"✗ Error importing chatbot: {e}")
        print("\nMake sure you're running from the project root directory.")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_chatbot_interactive():
    """Interactive chatbot test"""
    print("=" * 70)
    print("YatriSetu Chatbot - Interactive Mode")
    print("=" * 70)
    print("Type 'quit' or 'exit' to stop")
    print()
    
    try:
        from app.models.chatbot import SamparkChatbot
        
        chatbot = SamparkChatbot()
        user_id = "interactive_user"
        
        while True:
            try:
                message = input("\nYou: ").strip()
                
                if message.lower() in ['quit', 'exit', 'bye']:
                    print("\nChatbot: Goodbye! Have a great day!")
                    break
                
                if not message:
                    continue
                
                response = chatbot.process_message(user_id, message)
                
                print(f"\nChatbot: {response.get('message', 'No response')}")
                
                if response.get('routes'):
                    print(f"\nFound {len(response['routes'])} routes:")
                    for route in response['routes'][:3]:
                        print(f"  - {route.get('route_name', 'Unknown route')}")
                
                if response.get('suggestions'):
                    print("\nSuggestions:")
                    for suggestion in response['suggestions'][:3]:
                        print(f"  - {suggestion}")
                
            except KeyboardInterrupt:
                print("\n\nChatbot: Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
    
    except Exception as e:
        print(f"Error initializing chatbot: {e}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test YatriSetu Chatbot')
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    if args.interactive:
        test_chatbot_interactive()
    else:
        test_chatbot_basic()
