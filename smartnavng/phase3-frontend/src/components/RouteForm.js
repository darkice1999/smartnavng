import React, { useState, useEffect } from 'react';
import { getRoute, getAlerts } from '../services/api';
import './RouteForm.css';

const RouteForm = ({ onRouteCalculated, onAlertsLoaded, setLoading, token }) => {
  const [cities] = useState(['Lagos', 'Abuja', 'Port Harcourt']);
  const [formData, setFormData] = useState({
    startLat: '6.5244',
    startLng: '3.3792',
    endLat: '6.5274',
    endLng: '3.3822',
    city: 'Lagos'
  });

  useEffect(() => {
    loadAlerts();
  }, [formData.city]);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const loadAlerts = async () => {
    try {
      const alerts = await getAlerts(formData.city, token);
      onAlertsLoaded(alerts);
    } catch (error) {
      console.error('Error loading alerts:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const route = await getRoute(
        parseFloat(formData.startLat),
        parseFloat(formData.startLng),
        parseFloat(formData.endLat),
        parseFloat(formData.endLng),
        formData.city,
        token
      );
      
      onRouteCalculated(route.route);
      await loadAlerts();
    } catch (error) {
      console.error('Error calculating route:', error);
      alert('Error calculating route. Please check the console for details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="route-form-container">
      <form onSubmit={handleSubmit} className="route-form">
        <h3>Plan Your Route</h3>
        
        <div className="form-group">
          <label>City:</label>
          <select 
            name="city" 
            value={formData.city}
            onChange={handleInputChange}
          >
            {cities.map(city => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
        </div>

        <div className="coordinates-group">
          <div className="form-group">
            <label>Start Latitude:</label>
            <input
              type="number"
              step="any"
              name="startLat"
              value={formData.startLat}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Start Longitude:</label>
            <input
              type="number"
              step="any"
              name="startLng"
              value={formData.startLng}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label>End Latitude:</label>
            <input
              type="number"
              step="any"
              name="endLat"
              value={formData.endLat}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label>End Longitude:</label>
            <input
              type="number"
              step="any"
              name="endLng"
              value={formData.endLng}
              onChange={handleInputChange}
              required
            />
          </div>
        </div>

        <button type="submit" className="calculate-btn">
          Calculate Optimal Route
        </button>
      </form>
    </div>
  );
};

export default RouteForm;