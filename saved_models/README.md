# Saved Models Directory

This directory should contain your trained machine learning models.

## Required Files

1. **logistic_model.pkl** - Your trained Logistic Regression model (or any scikit-learn classifier)
2. **label_encoders.pkl** - Dictionary of fitted LabelEncoder objects for categorical features

## Model Training

Your model should be trained to predict depression risk based on the following features:

### Input Features:
- **Age**: Integer (10-120)
- **Gender**: Categorical (Male, Female, Other)
- **Sleep_Hours**: Float (0-24)
- **Physical_Activity_Hours**: Float (0-24)
- **Stress_Level**: Integer (1-10)
- **Social_Support**: Integer (1-5)
- **Mood_Level**: Integer (1-5)
- **Family_History**: Categorical (Yes, No)

### Output:
- Binary classification: 0 (No Risk) or 1 (At Risk)
- Model should support `predict_proba()` method for probability scores

## Example Training Code

```python
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Load your data
df = pd.read_csv('your_data.csv')

# Encode categorical variables
encoders = {}
categorical_columns = ['Gender', 'Family_History']

for col in categorical_columns:
    encoders[col] = LabelEncoder()
    df[col] = encoders[col].fit_transform(df[col])

# Prepare features and target
X = df[['Age', 'Gender', 'Sleep_Hours', 'Physical_Activity_Hours', 
        'Stress_Level', 'Social_Support', 'Mood_Level', 'Family_History']]
y = df['Depression_Risk']  # 0 or 1

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
joblib.dump(model, 'saved_models/logistic_model.pkl')
joblib.dump(encoders, 'saved_models/label_encoders.pkl')

print(f"Model accuracy: {model.score(X_test, y_test):.2f}")
```

## Loading Models

The models are automatically loaded by the application on startup using `app/ml/model_loader.py`.

## Testing Models

You can test if your models load correctly:

```python
from app.ml.model_loader import model_loader

# Load models
model = model_loader.load_model()
encoders = model_loader.load_encoders()

print(f"Model type: {type(model)}")
print(f"Encoders: {encoders.keys()}")
```

## Model Performance

Ensure your model has been validated and tested before deployment:
- Accuracy
- Precision/Recall
- ROC-AUC score
- Confusion matrix

## Notes

- Models should be serialized using joblib or pickle
- Ensure scikit-learn version compatibility
- Test models thoroughly before production use
- Consider retraining models periodically with new data
