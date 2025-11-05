import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os

def generate_sample_data():
    """Generate sample training data for travel time prediction"""
    np.random.seed(42)
    
    data = {
        'length_meters': np.random.uniform(100, 5000, 1000),
        'base_speed_kmh': np.random.uniform(20, 80, 1000),
        'traffic_factor': np.random.uniform(0.1, 1.0, 1000),
        'time_of_day': np.random.randint(0, 24, 1000),
        'day_of_week': np.random.randint(0, 7, 1000)
    }
    
    # Simulate travel time: base time + traffic effects + noise
    base_time = data['length_meters'] / (data['base_speed_kmh'] * 1000 / 3600)
    traffic_effect = base_time * data['traffic_factor'] * 0.8
    time_of_day_effect = base_time * (1 + 0.3 * np.sin(data['time_of_day'] / 24 * 2 * np.pi))
    
    data['travel_time_seconds'] = base_time + traffic_effect + time_of_day_effect + np.random.normal(0, 30, 1000)
    
    return pd.DataFrame(data)

def train_travel_model():
    """Train and save the travel time prediction model"""
    print("Generating training data...")
    df = generate_sample_data()
    
    # Features and target
    features = ['length_meters', 'base_speed_kmh', 'traffic_factor', 'time_of_day', 'day_of_week']
    X = df[features]
    y = df['travel_time_seconds']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    print("Training Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Model MAE: {mae:.2f} seconds")
    
    # Save model
    os.makedirs('/app/ai', exist_ok=True)
    model_path = '/app/ai/travel_model.joblib'
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    return model

if __name__ == '__main__':
    train_travel_model()