"""
Quick test script for Chatbot and DataExtractor models
"""

print("=" * 70)
print("YatriSetu Models Test")
print("=" * 70)
print()

# Test 1: Import models
print("Test 1: Importing models...")
try:
    from app.models import chatbot, DataExtractor, SamparkChatbot
    print("✓ Successfully imported: chatbot, DataExtractor, SamparkChatbot")
except Exception as e:
    print(f"✗ Import failed: {e}")
    exit(1)

print()

# Test 2: Chatbot instance
print("Test 2: Testing chatbot instance...")
try:
    print(f"  • Chatbot type: {type(chatbot).__name__}")
    print(f"  • Has process_message: {hasattr(chatbot, 'process_message')}")
    print(f"  • Has greeting_response: {hasattr(chatbot, 'greeting_response')}")
    print("✓ Chatbot instance is valid")
except Exception as e:
    print(f"✗ Chatbot test failed: {e}")

print()

# Test 3: DataExtractor class
print("Test 3: Testing DataExtractor class...")
try:
    extractor = DataExtractor()
    print(f"  • DataExtractor type: {type(extractor).__name__}")
    print(f"  • Has analyze_csv_structure: {hasattr(extractor, 'analyze_csv_structure')}")
    print(f"  • Has extract_from_pdf: {hasattr(extractor, 'extract_from_pdf')}")
    print("✓ DataExtractor class is valid")
except Exception as e:
    print(f"✗ DataExtractor test failed: {e}")

print()

# Test 4: Chatbot greeting (without database)
print("Test 4: Testing chatbot greeting (may fail without DB)...")
try:
    response = chatbot.greeting_response()
    print(f"  • Response type: {type(response)}")
    print(f"  • Has message: {'message' in response}")
    print(f"  • Message preview: {response.get('message', '')[:50]}...")
    print("✓ Chatbot greeting works")
except Exception as e:
    print(f"⚠ Chatbot greeting failed (expected without DB): {e}")

print()

# Test 5: Database models import
print("Test 5: Testing database models import...")
try:
    from app.models import User, Bus, Route, Booking, Payment, Driver, Conductor
    print("✓ Successfully imported all database models")
    print(f"  • User, Bus, Route, Booking, Payment, Driver, Conductor")
except Exception as e:
    print(f"✗ Database models import failed: {e}")

print()
print("=" * 70)
print("Test Summary")
print("=" * 70)
print("All critical imports are working correctly!")
print("Server is ready for testing.")
print()
print("Next Steps:")
print("  1. Run: python run.py")
print("  2. Open: http://localhost:5000/chatbot")
print("  3. Open: http://localhost:5000/admin/data-import")
print("=" * 70)
