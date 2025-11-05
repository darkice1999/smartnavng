import joblib
import numpy as np
import os

class TravelTimePredictor:
    def __init__(self, model_path='/app/ai/travel_model.joblib'):
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                print("Travel time model loaded successfully")
            else:
                print("Model file not found, using fallback prediction")
                self.model = None
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def predict(self, length_m, base_speed_kmh, traffic_factor=0.5, time_of_day=12, day_of_week=0):
        """Predict travel time for a road segment"""
        if self.model is None:
            # Fallback prediction
            base_time = length_m / (base_speed_kmh * 1000 / 3600) if base_speed_kmh > 0 else float('inf')
            return base_time * (1 + traffic_factor * 0.5)
        
        features = np.array([[length_m, base_speed_kmh, traffic_factor, time_of_day, day_of_week]])
        return self.model.predict(features)[0]

# Global instance
predictor = TravelTimePredictor()