import joblib
import os
from app.config import settings
from typing import Optional, Dict, Any


class ModelLoader:
    """Singleton class for loading and managing ML model and encoders"""
    
    _instance = None
    _model = None
    _encoders = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def load_model(self) -> Any:
        """Load the trained model"""
        if self._model is None:
            model_path = settings.MODEL_PATH
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}")
            
            self._model = joblib.load(model_path)
            print(f"Model loaded from {model_path}")
        
        return self._model
    
    def load_encoders(self) -> Dict[str, Any]:
        """Load the label encoders"""
        if self._encoders is None:
            encoders_path = settings.ENCODERS_PATH
            if not os.path.exists(encoders_path):
                raise FileNotFoundError(f"Encoders file not found at {encoders_path}")
            
            self._encoders = joblib.load(encoders_path)
            print(f"Encoders loaded from {encoders_path}")
        
        return self._encoders
    
    def get_model(self) -> Optional[Any]:
        """Get the loaded model"""
        if self._model is None:
            self.load_model()
        return self._model
    
    def get_encoders(self) -> Optional[Dict[str, Any]]:
        """Get the loaded encoders"""
        if self._encoders is None:
            self.load_encoders()
        return self._encoders
    
    def reload(self):
        """Reload model and encoders"""
        self._model = None
        self._encoders = None
        self.load_model()
        self.load_encoders()


# Create singleton instance
model_loader = ModelLoader()
