"""
Service for depression risk prediction using ML model
"""
import joblib
import numpy as np
from typing import Dict, Tuple
import os
from app.config import settings


class PredictionService:
    """Service for predicting depression risk from test data"""
    
    def __init__(self):
        self.model = None
        self.encoders = None
        self.load_models()
    
    def load_models(self):
        """Load the trained model and label encoders"""
        try:
            model_path = os.path.join(os.getcwd(), "saved_models", "logistic_model.pkl")
            encoders_path = os.path.join(os.getcwd(), "saved_models", "label_encoders.pkl")
            
            self.model = joblib.load(model_path)
            self.encoders = joblib.load(encoders_path)
            print(f"✓ Model and encoders loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def preprocess_depression_test(self, test_data: Dict) -> np.ndarray:
        """
        Preprocess depression test data for model prediction
        
        Args:
            test_data: Dictionary containing depression test responses
            
        Returns:
            Preprocessed numpy array ready for prediction
        """
        # Map database column names to model feature names
        feature_mapping = {
            'mood': 'Mood',
            'sleep_hour': 'SleepHour',
            'appetite': 'Appetite',
            'exercise': 'Exercise',
            'screen_time': 'ScreenTime',
            'academic_work': 'AcademicWork',
            'socialize': 'Social',
            'energy_level': 'Energy',
            'trouble_concentrating': 'TroubleConcentration',
            'negative_thoughts': 'NegativeThought',
            'decision_making': 'DecisionMaking',
            'bothered_things': 'BotherStatus',
            'stressful_events': 'StressfulEvent',
            'future_hope': 'FutureHope',
            'sleepy_tired': 'SleepyTired'
            
        }
        
        # Create processed data dict
        processed_data = {}
        
        for db_field, model_feature in feature_mapping.items():
            value = test_data.get(db_field)
            
            # Encode categorical features
            if model_feature in self.encoders and value is not None:
                try:
                    encoded_value = self.encoders[model_feature].transform([str(value)])[0]
                    processed_data[model_feature] = encoded_value
                except Exception as e:
                    print(f"Warning: Could not encode {model_feature}={value}: {e}")
                    processed_data[model_feature] = 0  # Default value
            else:
                # For numeric features (Energy)
                print(f"Processing feature {model_feature} with value {value}")
                processed_data[model_feature] = value if value is not None else 0
        
        # Check if model expects additional features not in database
        # and set defaults for them
        print("processed data after encoding:", processed_data)
        for feature_name in self.encoders.keys():
            if feature_name not in processed_data:
                print(f"Warning: Feature {feature_name} not found in test data, using default=0")
                processed_data[feature_name] = 0
        
        print("encode :", self.encoders.keys())
        
        # Define feature order (must match training order)
        # Get feature order from encoders or use the standard order
        feature_order = [
            'Mood', 'SleepHour', 'Appetite', 'Exercise', 'ScreenTime',
            'AcademicWork', 'Social', 'Energy', 'TroubleConcentration',
            'NegativeThought', 'DecisionMaking', 'BotherStatus',
            'StressfulEvent','SleepyTired', 'FutureHope'
        ]
        
        # Create ordered feature array
        ordered_values = [processed_data.get(feat, 0) for feat in feature_order]
        
        return np.array([ordered_values])
    
    def predict_depression_risk(self, test_data: Dict) -> Tuple[float, str]:
        """
        Predict depression risk from test data
        
        Args:
            test_data: Dictionary containing depression test responses
            
        Returns:
            Tuple of (risk_score, risk_level)
            - risk_score: Probability between 0.0 and 1.0
            - risk_level: "Low", "Medium", or "High"
        """
        # Preprocess the input
        X_processed = self.preprocess_depression_test(test_data)
        print(f"Preprocessed data for prediction: {X_processed}")
        # Make prediction (probability of positive class)
        risk_score = float(self.model.predict_proba(X_processed)[:, 1][0])
        
        # Determine risk level based on score
        if risk_score < 0.4:
            risk_level = "Low"
        elif risk_score < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return risk_score, risk_level

# Create singleton instance
prediction_service = PredictionService()
