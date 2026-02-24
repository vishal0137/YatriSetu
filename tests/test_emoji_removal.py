"""
Test that suggestions don't contain emojis
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.chatbot import chatbot
import re

def has_emoji(text):
    """Check if text contains emoji"""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return bool(emoji_pattern.search(text))

def test_emoji_removal():
    """Test that all suggestions are emoji-free"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 70)
        print("Testing Emoji Removal from Suggestions")
        print("=" * 70)
        
        test_commands = [
            'hi',
            'help',
            'stats',
            'find route',
            'check fare',
            'new search',
            'popular routes',
            'how to book',
            'ticket types',
            'contact support'
        ]
        
        all_clean = True
        
        for command in test_commands:
            response = chatbot.process_message('test_user', command)
            suggestions = response.get('suggestions', [])
            
            print(f"\n✓ Command: {command}")
            print(f"  Suggestions: {suggestions[:3]}...")  # Show first 3
            
            # Check each suggestion
            for suggestion in suggestions:
                if has_emoji(suggestion):
                    print(f"  ❌ FAIL: Found emoji in '{suggestion}'")
                    all_clean = False
            
            if not any(has_emoji(s) for s in suggestions):
                print(f"  ✅ All suggestions are emoji-free")
        
        print("\n" + "=" * 70)
        print("Test Summary")
        print("=" * 70)
        
        if all_clean:
            print("\n✅ SUCCESS: All suggestions are emoji-free!")
            print("Emojis will be added in frontend display only.")
        else:
            print("\n❌ FAILURE: Some suggestions still contain emojis")
        
        return all_clean

if __name__ == '__main__':
    success = test_emoji_removal()
    sys.exit(0 if success else 1)
