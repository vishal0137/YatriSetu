from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    try:
        db.init_app(app)
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        print("Server will run without database connection.")
    
    # Register blueprints
    from app.routes import admin, chatbot, data_import
    app.register_blueprint(admin.bp)
    app.register_blueprint(chatbot.bp)
    app.register_blueprint(data_import.data_import_bp)
    
    # Root route
    @app.route('/')
    def index():
        return '''
        <html>
        <head>
            <title>YatriSetu</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                .container {
                    text-align: center;
                    background: white;
                    padding: 50px;
                    border-radius: 20px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                }
                h1 {
                    color: #2563eb;
                    margin-bottom: 10px;
                }
                .bus-logo {
                    font-size: 80px;
                    margin-bottom: 20px;
                }
                p {
                    color: #666;
                    margin-bottom: 30px;
                }
                .btn {
                    display: inline-block;
                    padding: 15px 30px;
                    margin: 10px;
                    text-decoration: none;
                    border-radius: 25px;
                    font-weight: bold;
                    transition: all 0.3s;
                }
                .btn-primary {
                    background: #2563eb;
                    color: white;
                }
                .btn-primary:hover {
                    background: #1e40af;
                    transform: translateY(-2px);
                }
                .btn-secondary {
                    background: #10b981;
                    color: white;
                }
                .btn-secondary:hover {
                    background: #059669;
                    transform: translateY(-2px);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="bus-logo">🚌</div>
                <h1>YatriSetu</h1>
                <p>Smart Transit Platform for Delhi DTC</p>
                <a href="/chatbot" class="btn btn-secondary">💬 AI Chatbot</a>
                <a href="/admin" class="btn btn-primary">📊 Admin Dashboard</a>
            </div>
        </body>
        </html>
        '''
    
    return app
