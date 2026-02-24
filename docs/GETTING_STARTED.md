# Getting Started with YatriSetu

## Project Overview

YatriSetu is organized with a clean, professional structure designed for scalability and maintainability.

### Directory Structure

```
YatriSetu_Prototype/
├── app/              # Main Flask application
├── ml/               # Machine Learning models (database-trained)
├── tests/            # Comprehensive test suite
├── docs/             # Project documentation
└── models/           # Trained ML models
```

## Installation Methods

### Method 1: Basic Setup (Without ML)

```bash
# Install core dependencies
pip install -r requirements.txt

# Start development server
python run.py
```

### Method 2: Complete Setup (With ML Enhancement)

```bash
# Install all dependencies including ML libraries
pip install scikit-learn numpy

# Train models from database
python ml/db_trainer.py

# Start development server
python run.py
```

## Project Organization

### Application Structure

| Directory | Purpose |
|-----------|---------|
| app/ | Core Flask application code |
| ml/ | Machine learning models with database training |
| tests/ | Complete test suite for all components |
| docs/ | Comprehensive project documentation |
| models/ | Storage for trained ML models |

### Database-Driven ML Training

The ML system provides automated training capabilities:

1. Extracts location data from database
2. Extracts bus numbers and route information
3. Generates training examples automatically
4. Trains intent classification models
5. Persists models for production use

**Execution Command:**

```bash
python ml/db_trainer.py
```

### Testing Framework

```bash
# Test chatbot functionality
python tests/test_chatbot.py

# Test ML models
python tests/test_ml_models.py
```

## Key Files Reference

### Application Files

| File | Description |
|------|-------------|
| app/chatbot.py | Enhanced rule-based chatbot implementation |
| app/models.py | Database models and ORM definitions |
| run.py | Application entry point |

### ML System Files

| File | Description |
|------|-------------|
| ml/db_trainer.py | Database-driven model training |
| ml/ml_intent_classifier.py | Intent classification engine |
| ml/ml_entity_extractor.py | Entity extraction module |

### Test Files

| File | Description |
|------|-------------|
| tests/test_chatbot.py | Chatbot functionality tests |
| tests/test_ml_models.py | ML model validation tests |

### Documentation Files

| File | Description |
|------|-------------|
| docs/PROJECT_STRUCTURE.md | Complete architecture documentation |
| docs/ML_QUICKSTART.md | ML implementation guide |
| docs/CHATBOT_QUICK_REFERENCE.md | Chatbot feature reference |

## ML Training Process

### Training Workflow

The database trainer (`ml/db_trainer.py`) executes the following workflow:

```
Database Connection
    ↓
Data Extraction (locations, buses, routes)
    ↓
Training Example Generation
    ↓
Intent Classifier Training
    ↓
Model Persistence
```

### Training Execution

```bash
python ml/db_trainer.py
```

### Expected Output

```
============================================================
Generating Training Data from Database
============================================================

Extracting data from database...
   Found 165 unique locations
   Found 150 buses
   Found 165 routes

Generating intent examples...
   Generated 450+ training examples
   Across 10 intent categories

Training Intent Classifier...
Training on 450 examples, 10 intents...
Cross-validation accuracy: 0.956 (+/- 0.018)

============================================================
Training Complete
============================================================

Summary:
   Model accuracy: 95.6%
   Training examples: 450
   Locations: 165
   Buses: 150
   Routes: 165
```

## Testing Procedures

### Chatbot Testing

```bash
python tests/test_chatbot.py
```

**Test Coverage:**

- Greeting responses
- Route search functionality
- Fare inquiry system
- Bus tracking capabilities
- Fuzzy matching algorithms
- Special query handling

### ML Model Testing

```bash
python tests/test_ml_models.py
```

**Test Coverage:**

- Intent classification accuracy
- Entity extraction precision
- Location matching algorithms
- Confidence score validation

## Development Workflows

### Standard Development Workflow

```bash
# 1. Implement code changes
# 2. Execute tests
python tests/test_chatbot.py

# 3. Retrain ML models if necessary
python ml/db_trainer.py

# 4. Validate ML changes
python tests/test_ml_models.py

# 5. Start development server
python run.py
```

### ML Training Workflow

```bash
# 1. Update database (routes, locations, etc.)
# 2. Retrain models
python ml/db_trainer.py

# 3. Validate new models
python tests/test_ml_models.py

# 4. Models automatically integrated with chatbot
```

## Configuration

### Database Configuration

Create `.env` file in project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=yatrisetu_db
DB_USER=postgres
DB_PASSWORD=your_password
```

### ML Configuration

Models are persisted in the `models/` directory:

- `models/intent_classifier.pkl` - Trained classification model
- `models/training_metadata.json` - Training metadata and statistics

## Feature Comparison

### Rule-Based Chatbot (Current Implementation)

| Feature | Status |
|---------|--------|
| Fuzzy location matching | Implemented |
| Location aliases (100+) | Implemented |
| Real-time database queries | Implemented |
| Response time | <10ms |
| Accuracy | ~90% |

### ML Enhancement (Optional)

| Feature | Status |
|---------|--------|
| Intent classification | Available |
| Database-driven training | Available |
| Entity extraction | Available |
| Confidence scoring | Available |
| Accuracy | 95%+ |
| Response time | <50ms |

## Learning Path

### For New Developers

1. Review this document
2. Execute `python run.py`
3. Test chatbot functionality
4. Examine `app/chatbot.py` implementation

### For ML Implementation

1. Study `docs/ML_QUICKSTART.md`
2. Execute `python ml/db_trainer.py`
3. Test with `python tests/test_ml_models.py`
4. Review `ml/db_trainer.py` source code

### For Contributors

1. Review `docs/PROJECT_STRUCTURE.md`
2. Examine test examples in `tests/`
3. Follow established code patterns
4. Include tests for new features

## Deployment Checklist

### Production Preparation

| Task | Status |
|------|--------|
| Update `.env` with production values | Required |
| Set `FLASK_ENV=production` | Required |
| Configure production database | Required |
| Train ML models | Recommended |
| Execute test suite | Required |
| Configure monitoring | Required |
| Enable SSL/TLS | Required |
| Set up automated backups | Required |

## Performance Considerations

### System Performance

| Component | Performance |
|-----------|-------------|
| Rule-based chatbot | <10ms response time |
| ML enhancement | +40ms overhead |
| Database queries | Optimized with indexes |
| Caching | Recommended for popular queries |

### ML Training Performance

| Metric | Value |
|--------|-------|
| Training frequency | Weekly/Monthly |
| Training duration | <30 seconds |
| Model size | ~10MB |
| Accuracy improvement | Scales with data volume |

## Summary

### Project Status

| Component | Status |
|-----------|--------|
| Project structure | Clean and organized |
| ML training | Automated from database |
| Test suite | Comprehensive coverage |
| Documentation | Complete |
| Production readiness | Ready |

### Next Steps

1. Explore codebase structure
2. Execute test suite
3. Train ML models (optional)
4. Deploy to production environment

## Support Resources

| Resource | Location |
|----------|----------|
| Quick start guide | docs/ML_QUICKSTART.md |
| Architecture documentation | docs/PROJECT_STRUCTURE.md |
| Feature reference | docs/CHATBOT_QUICK_REFERENCE.md |
| Project status | docs/PROJECT_STATUS.md |
