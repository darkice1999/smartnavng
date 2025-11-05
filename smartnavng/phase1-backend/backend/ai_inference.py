import joblib
import numpy as np
from models import RoadSegment
import os

# Simple travel time prediction model
class SimpleTravelModel:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        # For demo - create a simple model if none exists
        try:
            self.model = joblib.load('/app/ai/travel_model.joblib')
        except:
            # Create simple prediction: time = (length / speed) * traffic_factor
            self.model = lambda features: (features[0] / max(features[1], 1)) * (1 + features[2] * 0.5)
    
    def predict(self, length_m, base_speed_kmh, traffic_factor):
        features = np.array([[length_m, base_speed_kmh, traffic_factor]])
        if callable(self.model):
            return self.model([length_m, base_speed_kmh, traffic_factor])
        return self.model.predict(features)[0]

# Global model instance
travel_model = SimpleTravelModel()

def predict_travel_time(road_segment: RoadSegment) -> float:
    """Predict travel time in seconds for a road segment"""
    # Simple traffic factor based on city and time (demo)
    traffic_factors = {'Lagos': 0.8, 'Abuja': 0.4, 'Port Harcourt': 0.6}
    traffic_factor = traffic_factors.get(road_segment.city, 0.5)
    
    # Convert speed from km/h to m/s
    speed_ms = (road_segment.base_speed_kmh * 1000) / 3600
    
    # Base time without AI
    base_time = road_segment.length_meters / speed_ms if speed_ms > 0 else float('inf')
    
    # Apply AI prediction
    try:
        predicted_time = travel_model.predict(
            road_segment.length_meters,
            road_segment.base_speed_kmh,
            traffic_factor
        )
        return max(predicted_time, base_time * 0.5)  # Ensure reasonable minimum
    except:
        return base_time

def calculate_road_penalty(road_segment: RoadSegment, alerts) -> float:
    """Calculate penalty factor for road conditions"""
    penalty = 1.0  # Base penalty
    
    # Check for alerts affecting this segment
    segment_alerts = [alert for alert in alerts if 
                     road_segment.segment_id in alert.affected_segments]
    
    for alert in segment_alerts:
        if alert.severity == 'low':
            penalty *= 1.2
        elif alert.severity == 'medium':
            penalty *= 1.5
        elif alert.severity == 'high':
            penalty *= 2.0
    
    return penalty