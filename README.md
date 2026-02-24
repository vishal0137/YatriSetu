# YatriSetu - Smart Transit Platform for Delhi Transport Corporation

## Project Overview

YatriSetu is a centralized smart transit platform designed for Delhi Transport Corporation (DTC) to modernize public transport services in Delhi.

### Objective

The objective of YatriSetu is to design and implement a centralized smart transit platform for Delhi Transport Corporation (DTC) that:

- Provides real-time GPS-based bus tracking
- Enables intelligent route planning for efficient travel
- Supports online ticket booking with QR-based validation
- Integrates a digital wallet for unified, cashless payments
- Offers a centralized admin dashboard for monitoring operations and analytics
- Implements an AI chatbot route assistant to:
  - Suggest the shortest route
  - Recommend the lowest fare options
  - Ensure strong route connectivity & minimum transfers
  - Guide users step-by-step to their destination

**Overall Goal:** Improve passenger convenience, enhance operational efficiency, and modernize public transport services in Delhi.

### Problem Statement

Delhi Transport Corporation (DTC) buses serve lakhs of commuters daily, yet passengers face uncertainty due to inconsistent arrival times, difficulty in route planning, and inconvenient fare payment methods.

Existing transport solutions provide limited features such as schedule information or GPS tracking, but they lack integration with predictive analytics, digital ticketing, and unified payment systems. Additionally, transport authorities lack centralized tools for real-time monitoring and data-driven decision-making.

As a result, commuters experience longer waiting times, inefficient travel planning, and reduced service reliability.

Therefore, a centralized smart transit platform is needed to integrate real-time tracking, intelligent route guidance, and seamless digital ticketing to improve commuter convenience and operational efficiency.

### Proposed Solution

During the research phase, several existing transport management systems were analyzed. Platforms like RedBus provide centralized booking services but mainly focus on private and intercity buses. Government transport portals offer route and schedule information; however, they lack integrated digital ticketing and predictive analytics. Standalone GPS-based tracking systems are available, but they are not fully connected with payment and ticket validation systems.

These observations highlight that although partial digital solutions exist, there is no comprehensive and unified platform specifically designed for Delhi Transport Corporation buses in Delhi. The absence of an integrated system combining real-time tracking, AI-based prediction, online ticket booking, and unified digital payments forms the foundation for the proposed solution, YatriSetu.

## Project Structure

```
YatriSetu_Prototype/
├── venv/                      # Virtual environment
├── app/                       # Main application
│   ├── static/               # Static files (CSS, JS, images)
│   ├── templates/            # HTML templates
│   ├── routes/               # Route handlers
│   └── models/               # Database models
├── database/                  # Database files
│   └── YATRISETU_DB.sql     # PostgreSQL database dump
├── docs/                      # Documentation
├── requirements.txt           # Python dependencies
├── config.py                  # Configuration file
├── run.py                     # Application entry point
└── README.md                  # This file
```

## Technology Stack

- **Backend:** Python Flask
- **Database:** PostgreSQL
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts:** Chart.js
- **Icons:** Font Awesome

## Prerequisites

See [PREREQUISITES.md](PREREQUISITES.md) for detailed setup instructions.

## Quick Start

1. Clone the repository
2. Set up virtual environment: `python -m venv venv`
3. Activate virtual environment: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Configure database connection in `config.py`
6. Import database: `psql -U postgres -d yatrisetu < YATRISETU_DB.sql`
7. Run application: `python run.py`
8. Access application:
   - **Home:** http://localhost:5000
   - **AI Chatbot:** http://localhost:5000/chatbot
   - **Admin Dashboard:** http://localhost:5000/admin

## AI Chatbot Usage

The AI chatbot provides intelligent assistance for:

### Route Planning
```
You: "Route from Connaught Place to Dwarka"
Bot: Shows shortest route, fare, duration, and distance
```

### Fare Inquiry
```
You: "Fare to Kashmere Gate"
Bot: Shows fare breakdown by passenger category
```

### Booking Assistance
```
You: "Book ticket"
Bot: Guides through booking process
```

### Sample Queries
- "How to reach Anand Vihar from ISBT?"
- "Cheapest route to Dwarka"
- "Show me routes with minimum transfers"
- "Ticket price for students"

## Features

### AI Chatbot (WhatsApp-style Interface)
- **Intelligent Route Assistant** with natural language processing
- **Shortest Route Suggestions** based on duration and distance
- **Lowest Fare Recommendations** with passenger category discounts
- **Strong Route Connectivity** ensuring minimum transfers
- **Step-by-Step Guidance** to destination
- **Real-time Responses** with typing indicators
- **Quick Suggestions** for common queries
- **Conversation Context** maintenance

### Admin Dashboard
- Real-time bus tracking overview
- Booking statistics and analytics
- Revenue monitoring
- User management
- Route management
- Fleet management
- Payment transaction monitoring

## License

© 2026 YatriSetu. All rights reserved.
