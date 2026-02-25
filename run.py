from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 70)
    print("YatriSetu - Smart Transit Platform")
    print("=" * 70)
    print("Starting server...")
    print()
    print("Available Endpoints:")
    print("  • Home Page:          http://localhost:5000/")
    print("  • AI Chatbot:         http://localhost:5000/chatbot")
    print("  • Admin Dashboard:    http://localhost:5000/admin")
    print("  • Data Import:        http://localhost:5000/admin/data-import")
    print()
    print("Testing Features:")
    print("  ✓ Chatbot - Natural language route queries")
    print("  ✓ Data Extractor - CSV/PDF file processing")
    print("  ✓ Admin Panel - Complete dashboard access")
    print()
    print("Press CTRL+C to quit")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)
