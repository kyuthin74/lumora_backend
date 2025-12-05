# Lumora Backend - Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment
```powershell
# Copy example environment file
copy .env.example .env

# Edit .env file with your settings (optional for basic setup)
# The defaults will work for local development
```

### 3. Run the Application
```powershell
# Start the server
uvicorn app.main:app --reload

# Or use Python directly
python -m app.main
```

### 4. Access the API
- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## First API Calls

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "Test User",
    "password": "SecurePass123"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=SecurePass123"
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 3. Create Mood Entry
```bash
curl -X POST "http://localhost:8000/mood/entries" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "mood_level": "good",
    "sleep_hours": 7.5,
    "sleep_quality": "good",
    "physical_activity_minutes": 45,
    "social_interaction_level": 4,
    "stress_level": 5,
    "notes": "Feeling great today!"
  }'
```

### 4. Get Depression Risk Assessment
```bash
curl -X POST "http://localhost:8000/risk/predict" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 28,
    "gender": "Male",
    "sleep_hours": 7.5,
    "physical_activity_hours": 0.75,
    "stress_level": 5,
    "social_support": 4,
    "mood_level": 4,
    "family_history": "No"
  }'
```

## Using the Interactive API Docs

1. Go to http://localhost:8000/docs
2. Click "Authorize" button (lock icon)
3. Login to get a token
4. Paste the token and click "Authorize"
5. Now you can test all endpoints directly!

## Testing Without ML Models

The app will work without ML models, but predictions will return placeholder values. To add models:

1. Train your model (see `saved_models/README.md`)
2. Save to `saved_models/logistic_model.pkl`
3. Save encoders to `saved_models/label_encoders.pkl`
4. Restart the application

## Common Issues

### Port Already in Use
```powershell
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### Import Errors
```powershell
# Ensure you're in the project root and venv is activated
cd lumora_backend
.\venv\Scripts\activate
```

### Database Locked (SQLite)
```powershell
# Delete the database file and restart
rm lumora.db
python -m app.main
```

## Next Steps

1. **Frontend Integration**: Connect your React/Vue/Angular frontend
2. **Email Setup**: Configure SMTP for alert emails
3. **Chatbot**: Add OpenAI API key for AI chatbot
4. **Production**: Use PostgreSQL and deploy to cloud

## Development Tips

### Watch Logs
```powershell
# The app logs to console - watch for errors and info
```

### Database Inspection
```powershell
# SQLite browser
pip install sqlite-web
sqlite_web lumora.db
```

### API Testing Tools
- Postman
- Insomnia  
- Thunder Client (VS Code extension)
- Built-in Swagger UI at /docs

## Support

For issues or questions:
- Check README.md for detailed documentation
- Review API documentation at /docs
- Check the logs for error messages

Happy coding! 🚀
