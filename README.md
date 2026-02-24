# YatriSetu - Smart Transit Platform for Delhi Transport Corporation

## Executive Summary

YatriSetu is a centralized smart transit platform designed for Delhi Transport Corporation (DTC) to modernize public transport services in Delhi through integrated technology solutions.

## Project Objectives

The YatriSetu platform implements a centralized smart transit system for Delhi Transport Corporation (DTC) with the following objectives:

| Objective | Description |
|-----------|-------------|
| Real-time GPS tracking | Provides live bus location tracking for passenger convenience |
| Intelligent route planning | Enables efficient travel planning with multiple route options |
| Online ticket booking | Supports digital ticket booking with QR-based validation |
| Digital wallet integration | Implements unified, cashless payment system |
| Centralized admin dashboard | Offers comprehensive monitoring and analytics capabilities |
| AI chatbot assistant | Provides intelligent route guidance with multiple optimization criteria |

### AI Chatbot Capabilities

| Feature | Description |
|---------|-------------|
| Shortest route suggestions | Optimizes travel time |
| Lowest fare recommendations | Minimizes travel cost |
| Route connectivity analysis | Ensures minimum transfers |
| Step-by-step guidance | Provides detailed navigation instructions |

### Overall Goal

Improve passenger convenience, enhance operational efficiency, and modernize public transport services in Delhi.

## Problem Statement

Delhi Transport Corporation (DTC) buses serve millions of commuters daily. However, passengers face significant challenges:

| Challenge | Impact |
|-----------|--------|
| Inconsistent arrival times | Increased waiting time and uncertainty |
| Difficult route planning | Inefficient travel decisions |
| Inconvenient fare payment | Cash-dependent transactions |
| Limited real-time information | Reduced service reliability |

### Current Solution Limitations

Existing transport solutions provide fragmented features:

| Solution Type | Limitations |
|---------------|-------------|
| Schedule information systems | No real-time tracking or predictive analytics |
| GPS tracking systems | Not integrated with ticketing and payments |
| Private bus platforms | Focus on intercity travel, not local transit |
| Government portals | Lack digital ticketing and unified payments |

### Identified Gap

The absence of a comprehensive, unified platform specifically designed for Delhi Transport Corporation creates the need for YatriSetu - an integrated system combining real-time tracking, AI-based prediction, online ticket booking, and unified digital payments.

## Proposed Solution

### Market Analysis

During the research phase, several existing transport management systems were analyzed:

| Platform Type | Capabilities | Limitations |
|---------------|-------------|-------------|
| RedBus | Centralized booking | Focus on private/intercity buses |
| Government portals | Route and schedule information | No integrated digital ticketing |
| GPS tracking systems | Real-time location | Not connected with payments/validation |

### Solution Foundation

These observations highlight that although partial digital solutions exist, there is no comprehensive and unified platform specifically designed for Delhi Transport Corporation. YatriSetu addresses this gap by integrating:

- Real-time GPS tracking
- AI-based route prediction
- Online ticket booking
- Unified digital payment system
- Centralized administrative dashboard

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

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Python Flask | Web application framework |
| Database | PostgreSQL | Relational database management |
| Frontend | HTML5, CSS3, JavaScript | User interface |
| UI Framework | Bootstrap 5 | Responsive design |
| Data Visualization | Chart.js | Analytics and reporting |
| Icons | Font Awesome | UI iconography |

## Prerequisites

Refer to [PREREQUISITES.md](docs/PREREQUISITES.md) for comprehensive setup instructions.

### System Requirements

| Component | Minimum Version |
|-----------|----------------|
| Python | 3.8+ |
| PostgreSQL | 14+ |
| RAM | 4GB |
| Storage | 2GB free space |

## Quick Start

### Installation Steps

| Step | Command | Description |
|------|---------|-------------|
| 1 | Clone repository | Download project files |
| 2 | `python -m venv venv` | Create virtual environment |
| 3 | `venv\Scripts\activate` | Activate environment (Windows) |
| 4 | `pip install -r requirements.txt` | Install dependencies |
| 5 | Configure `config.py` | Set database connection |
| 6 | `psql -U postgres -d yatrisetu < YATRISETU_DB.sql` | Import database |
| 7 | `python run.py` | Start application |

### Application Access

| Interface | URL |
|-----------|-----|
| Home | http://localhost:5000 |
| AI Chatbot | http://localhost:5000/chatbot |
| Admin Dashboard | http://localhost:5000/admin |

## AI Chatbot Usage

The AI chatbot provides intelligent assistance across multiple domains:

### Route Planning

| User Query | System Response |
|------------|----------------|
| "Route from Connaught Place to Dwarka" | Displays shortest route, fare, duration, and distance |

### Fare Inquiry

| User Query | System Response |
|------------|----------------|
| "Fare to Kashmere Gate" | Shows fare breakdown by passenger category |

### Booking Assistance

| User Query | System Response |
|------------|----------------|
| "Book ticket" | Guides through booking process |

### Sample Queries

- "How to reach Anand Vihar from ISBT?"
- "Cheapest route to Dwarka"
- "Show me routes with minimum transfers"
- "Ticket price for students"

## Features

### AI Chatbot (WhatsApp-style Interface)

| Feature | Description |
|---------|-------------|
| Intelligent Route Assistant | Natural language processing for query understanding |
| Shortest Route Suggestions | Optimized based on duration and distance |
| Lowest Fare Recommendations | Passenger category discounts applied |
| Strong Route Connectivity | Ensures minimum transfers |
| Step-by-Step Guidance | Detailed navigation to destination |
| Real-time Responses | Typing indicators for user feedback |
| Quick Suggestions | Common query shortcuts |
| Conversation Context | Maintains session state |

### Admin Dashboard

| Feature | Description |
|---------|-------------|
| Real-time bus tracking | Live GPS location monitoring |
| Booking statistics | Comprehensive booking analytics |
| Revenue monitoring | Financial performance tracking |
| User management | Account administration |
| Route management | Route configuration and updates |
| Fleet management | Bus inventory and status |
| Payment transactions | Transaction monitoring and reporting |

## Documentation

Comprehensive documentation is available in the `docs/` directory:

| Document | Description |
|----------|-------------|
| [GETTING_STARTED.md](docs/GETTING_STARTED.md) | Complete setup and installation guide |
| [QUICKSTART.md](docs/QUICKSTART.md) | Quick setup for experienced developers |
| [PREREQUISITES.md](docs/PREREQUISITES.md) | System requirements and dependencies |
| [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | Architecture and codebase organization |
| [USE_CASE_DIAGRAM.md](docs/USE_CASE_DIAGRAM.md) | System use cases and actor interactions |
| [CHATBOT_QUICK_REFERENCE.md](docs/CHATBOT_QUICK_REFERENCE.md) | Chatbot commands and API reference |
| [ML_QUICKSTART.md](docs/ML_QUICKSTART.md) | Machine learning implementation guide |
| [TESTING_GUIDE.md](docs/TESTING_GUIDE.md) | Testing procedures and guidelines |

## License

Copyright 2026 YatriSetu. All rights reserved.
