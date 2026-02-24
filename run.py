from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("YatriSetu Admin Dashboard")
    print("=" * 60)
    print("Starting server...")
    print("Admin Dashboard: http://localhost:5000/admin")
    print("Press CTRL+C to quit")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
