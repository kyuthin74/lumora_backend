# In your FastAPI application file (e.g., main.py)
import joblib
import numpy as np
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

# Load the model and encoders ONCE when the application starts
model = joblib.load('logistic_model.pkl')
fitted_encoders = joblib.load('label_encoders.pkl')

class DepressionRiskInput(BaseModel):
    # Define the fields matching your categorical features
    # Example (adjust field names and types based on your actual features):
    Mood: str
    SleepHour: str
    Appetite: str
    Exercise: str
    ScreenTime: str
    AcademicWork: str
    Social: str
    Energy: int
    TroubleConcentration: str
    NegativeThought: str
    DecisionMaking: str
    BotherStatus: str
    StressfulEvent: str
    SleepyTired: str
    FutureHope: str

def preprocess_input(input_data: DepressionRiskInput):
    # Convert input data to a dictionary
    input_dict = input_data.dict()
    
    # Create a copy to avoid modifying the original input
    processed_data = input_dict.copy()

    for feature_name, encoder in fitted_encoders.items():
        if feature_name in processed_data:
            # Reshape the single value for the encoder
            categorical_value = [processed_data[feature_name]]
            # Transform the categorical value using the loaded encoder
            encoded_value = encoder.transform(categorical_value)[0] # Get the first (and only) transformed value
            processed_data[feature_name] = encoded_value
        else:
            # Handle case where a required feature might be missing
            print(f"Warning: Feature {feature_name} not found in input data.")
            # You might want to raise an exception or use a default value depending on your logic

    # Convert the processed dictionary to the format expected by your model (e.g., numpy array)
    # Ensure the order of features matches the order used during training (X.columns)
    feature_order = ['Mood', 'SleepHour', 'Appetite', 'Exercise', 'ScreenTime', 'AcademicWork', 'Social', 
                     'Energy', 'TroubleConcentration', 'NegativeThought', 
                     'DecisionMaking', 'BotherStatus', 'StressfulEvent', 
                     'SleepyTired', 'FutureHope'
                    ] 
    ordered_values = [processed_data[feat] for feat in feature_order]
    return np.array([ordered_values])

@app.post("/predict_depression_risk/")
def predict_depression_risk(input_data: DepressionRiskInput):
    try:
        # Preprocess the input
        X_processed = preprocess_input(input_data)
        
        # Make prediction (assuming your model outputs probability for class 1)
        prediction_proba = model.predict_proba(X_processed)[:, 1] # Probability of positive class
        risk_score = float(prediction_proba[0]) # Extract the single probability value

        # Optionally, apply your threshold 't' to get a binary prediction
        # threshold = 0.37 # Use the threshold you determined during training
        # prediction = 1 if risk_score >= threshold else 0

        return {"depression_risk_probability": risk_score}
        # Or return {"prediction": prediction, "risk_score": risk_score}
    except Exception as e:
        return {"error": str(e)}