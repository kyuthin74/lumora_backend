import pandas as pd
import numpy as np
from typing import Dict, Tuple
from app.ml.model_loader import model_loader
from app.models.depression_risk import DepressionRiskInput, DepressionRiskResult
from app.utils.helpers import determine_risk_level, generate_risk_recommendation


def preprocess_input(input_data: DepressionRiskInput) -> pd.DataFrame:
    """
    Preprocess input data for model prediction
    Convert input to DataFrame and encode categorical variables
    """
    # Convert to dictionary
    data_dict = {
        'Age': input_data.age,
        'Gender': input_data.gender,
        'Sleep_Hours': input_data.sleep_hours,
        'Physical_Activity_Hours': input_data.physical_activity_hours,
        'Stress_Level': input_data.stress_level,
        'Social_Support': input_data.social_support,
        'Mood_Level': input_data.mood_level,
        'Family_History': input_data.family_history
    }
    
    # Create DataFrame
    df = pd.DataFrame([data_dict])
    
    # Get encoders
    encoders = model_loader.get_encoders()
    
    # Encode categorical variables
    categorical_columns = ['Gender', 'Family_History']
    
    for col in categorical_columns:
        if col in encoders:
            try:
                # Transform using the fitted encoder
                df[col] = encoders[col].transform(df[col])
            except ValueError:
                # Handle unseen labels by using the most frequent class
                df[col] = encoders[col].transform([encoders[col].classes_[0]])[0]
    
    return df


def predict_depression_risk(input_data: DepressionRiskInput) -> DepressionRiskResult:
    """
    Predict depression risk based on input data
    Returns risk level, score, and recommendation
    """
    try:
        # Preprocess input
        processed_data = preprocess_input(input_data)
        
        # Get model
        model = model_loader.get_model()
        
        # Make prediction
        prediction_proba = model.predict_proba(processed_data)
        
        # Get probability of positive class (depression risk)
        # Assuming binary classification where class 1 is "at risk"
        if len(prediction_proba[0]) > 1:
            risk_score = float(prediction_proba[0][1])
        else:
            risk_score = float(prediction_proba[0][0])
        
        # Determine risk level
        risk_level = determine_risk_level(risk_score)
        
        # Calculate confidence (how certain the model is)
        confidence = float(max(prediction_proba[0]))
        
        # Generate recommendation
        recommendation = generate_risk_recommendation(risk_level, risk_score)
        
        return DepressionRiskResult(
            risk_level=risk_level,
            risk_score=risk_score,
            confidence=confidence,
            recommendation=recommendation
        )
        
    except Exception as e:
        # Fallback in case of prediction error
        print(f"Prediction error: {str(e)}")
        return DepressionRiskResult(
            risk_level="Unknown",
            risk_score=0.5,
            confidence=0.0,
            recommendation="Unable to assess risk at this time. Please try again or consult a healthcare professional."
        )


def predict_from_mood_entry(mood_entry_data: dict) -> Tuple[float, str]:
    """
    Predict depression risk from mood entry data
    Returns (risk_score, risk_level)
    """
    try:
        # Convert mood entry to risk input format
        # This is a simplified mapping - adjust based on your actual model
        risk_input = DepressionRiskInput(
            age=mood_entry_data.get('age', 30),  # Default age if not provided
            gender=mood_entry_data.get('gender', 'Other'),
            sleep_hours=mood_entry_data.get('sleep_hours', 7.0),
            physical_activity_hours=mood_entry_data.get('physical_activity_minutes', 30) / 60,
            stress_level=mood_entry_data.get('stress_level', 5),
            social_support=mood_entry_data.get('social_interaction_level', 3),
            mood_level=mood_entry_data.get('mood_level', 3),
            family_history=mood_entry_data.get('family_history', 'No')
        )
        
        result = predict_depression_risk(risk_input)
        return result.risk_score, result.risk_level
        
    except Exception as e:
        print(f"Mood entry prediction error: {str(e)}")
        return 0.5, "Unknown"


def batch_predict(input_data_list: list) -> list:
    """
    Make predictions for multiple inputs
    Returns list of DepressionRiskResult
    """
    results = []
    for input_data in input_data_list:
        result = predict_depression_risk(input_data)
        results.append(result)
    return results
