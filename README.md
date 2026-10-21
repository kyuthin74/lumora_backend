# Lumora Mental Health Backend

A comprehensive FastAPI backend for mental health tracking and depression risk assessment.

## Features

- 🔐 **User Authentication**: Secure JWT-based authentication
- 📊 **Mood Tracking**: Daily mood check-ins with detailed metrics
- 🧠 **Depression Risk Assessment**: ML-powered risk prediction
- 📈 **Data Visualization**: Chart data for trends and insights
- 🚨 **Alert System**: Automated alerts for high-risk situations
- 💬 **AI Chatbot**: Supportive mental health chatbot
- 📧 **Email Notifications**: Automated email alerts for critical situations

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy (supports SQLite, PostgreSQL)
- **ML**: scikit-learn, pandas, numpy
- **Authentication**: JWT (python-jose, passlib)
- **Email**: aiosmtplib
- **AI Chatbot**: OpenAI API (optional)

## Project Structure

```
lumora_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI application
│   ├── config.py                 # Configuration settings
│   ├── database.py               # Database connection
│   ├── models/                   # Pydantic models
│   │   ├── user.py
│   │   ├── mood.py
│   │   ├── depression_risk.py
│   │   ├── chart.py
│   │   └── chatbot.py
│   ├── schemas/                  # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── mood_entry.py
│   │   ├── depression_risk_result.py
│   │   └── alert.py
│   ├── api/                      # API routes
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── mood.py
│   │   ├── depression_risk.py
│   │   ├── alerts.py
│   │   ├── charts.py
│   │   └── chatbot.py
│   ├── crud/                     # Database operations
│   │   ├── user.py
│   │   ├── mood_entry.py
│   │   ├── depression_risk_result.py
│   │   └── alert.py
│   ├── ml/                       # Machine Learning
│   │   ├── model_loader.py
│   │   └── prediction.py
│   ├── services/                 # Business logic
│   │   ├── email_service.py
│   │   ├── alert_service.py
│   │   └── chatbot_service.py
│   └── utils/                    # Utility functions
│       ├── security.py
│       ├── validators.py
│       └── helpers.py
├── saved_models/                 # ML models directory
│   ├── randomforest_model.pkl
│   └── label_encoders.pkl
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.11
- pip
- (Optional) Virtual environment tool

### Setup

1. **Clone the repository**
   ```bash
   cd lumora_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**
   ```bash
   # Copy and edit with your settings
   cp .env.example .env
   ```

5. **Configure environment variables**
   ```env
   # Database
   DATABASE_URL=sqlite:///./lumora.db
   # or for PostgreSQL:
   # DATABASE_URL=postgresql://user:password@localhost/lumora_db
   
   # Security
   SECRET_KEY=your-secret-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   
   # ML Models
   MODEL_PATH=saved_models/randomforest_model.pkl
   ENCODERS_PATH=saved_models/label_encoders.pkl
   
   # Email (optional)
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   SMTP_FROM_EMAIL=your-email@gmail.com
   
   # Alerts
   HIGH_RISK_THRESHOLD=0.7
   ALERT_EMAIL_ENABLED=false
   
   # OpenAI (optional)
   OPENAI_API_KEY=your-openai-api-key
   ```

6. **Prepare ML models**
   - Place your trained model files in `saved_models/` directory
   - Required files: `randomforest_model.pkl` and `label_encoders.pkl`

7. **Initialize database**
   ```bash
   # Database will be created automatically on first run
   python -m app.main
   ```

## Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Python directly
```bash
python -m app.main
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login (form data)
- `POST /auth/login-json` - Login (JSON)
- `GET /auth/me` - Get current user
- `POST /auth/refresh` - Refresh token

### User Management
- `GET /user/profile` - Get user profile
- `PUT /user/profile` - Update profile
- `DELETE /user/profile` - Delete account

### Mood Tracking
- `POST /mood/entries` - Create mood entry
- `GET /mood/entries` - Get mood entries
- `GET /mood/entries/{id}` - Get specific entry
- `PUT /mood/entries/{id}` - Update entry
- `DELETE /mood/entries/{id}` - Delete entry
- `GET /mood/statistics` - Get mood statistics

### Depression Risk Assessment
- `POST /risk/predict` - Predict depression risk
- `GET /risk/history` - Get risk history
- `GET /risk/history/{id}` - Get specific result
- `GET /risk/latest` - Get latest assessment
- `GET /risk/trend` - Get risk trend

### Alerts
- `GET /alerts` - Get all alerts
- `GET /alerts/unread-count` - Get unread count
- `GET /alerts/{id}` - Get specific alert
- `PATCH /alerts/{id}/read` - Mark as read
- `PATCH /alerts/{id}/resolve` - Mark as resolved
- `DELETE /alerts/{id}` - Delete alert

### Charts & Visualization
- `GET /charts/mood` - Get mood chart data
- `GET /charts/activity` - Get activity chart data
- `GET /charts/risk` - Get risk chart data
- `GET /charts/comprehensive` - Get all chart data

### Chatbot
- `POST /chatbot/chat` - Chat with AI assistant
- `GET /chatbot/suggestions` - Get personalized suggestions

## Authentication

All endpoints except `/auth/signup` and `/auth/login` require authentication.

Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Database Models

### User
- Email, password, full name
- Timestamps (created_at, updated_at)

### MoodEntry
- Mood level, sleep hours, sleep quality
- Physical activity, social interaction
- Stress level, notes
- Depression risk score (calculated)

### DepressionRiskResult
- Risk level (Low/Medium/High)
- Risk score (0-1)
- Input data (for audit)

### Alert
- Alert type, severity
- Message, read/resolved status
- Email notification status

## ML Model Integration

The app expects trained scikit-learn models:

1. **randomforest_model.pkl**: Trained classification model
2. **label_encoders.pkl**: Dictionary of LabelEncoders for categorical features

### Expected Input Features:
- Age
- Gender
- Sleep Hours
- Physical Activity Hours
- Stress Level (1-10)
- Social Support (1-5)
- Mood Level (1-5)
- Family History (Yes/No)

## Email Configuration

For Gmail:
1. Enable 2-factor authentication
2. Generate app-specific password
3. Use app password in SMTP_PASSWORD

## Security Best Practices

1. **Change SECRET_KEY** in production
2. Use **HTTPS** in production
3. Use **PostgreSQL** instead of SQLite in production
4. Enable **rate limiting**
5. Regularly **update dependencies**
6. Use **environment variables** for sensitive data

## Crisis Resources

The app includes crisis resources:
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text "HELLO" to 741741

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
```

### Type Checking
```bash
mypy app/
```

## Deployment

### Using Docker (recommended)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
Set all required environment variables in your deployment platform.

## Troubleshooting

### Database Issues
- Check DATABASE_URL format
- Ensure database file permissions (SQLite)
- Verify PostgreSQL connection (if used)

### ML Model Issues
- Verify model files exist in saved_models/
- Check model file permissions
- Ensure model was trained with same scikit-learn version

### Email Issues
- Verify SMTP credentials
- Check firewall settings
- Use app-specific password for Gmail

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License - see LICENSE file for details

## Support

For support, email: support@lumora.example.com

## Acknowledgments

- FastAPI framework
- scikit-learn for ML capabilities
- OpenAI for chatbot integration (optional)

---

**Note**: This application is for educational/support purposes and should not replace professional mental health care. Always consult healthcare professionals for medical advice.
