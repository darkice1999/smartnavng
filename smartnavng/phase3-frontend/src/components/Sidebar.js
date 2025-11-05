import React from 'react';
import './Sidebar.css';

const Sidebar = ({ user, route, alerts, loading }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>SmartNavNG</h2>
        {user && (
          <div className="user-info">
            <span>Welcome, {user.username}</span>
          </div>
        )}
      </div>

      <div className="sidebar-content">
        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            Calculating optimal route...
          </div>
        )}

        {route && route.summary && (
          <div className="route-summary">
            <h3>Route Summary</h3>
            <div className="summary-item">
              <span>Distance:</span>
              <strong>{route.summary.total_distance_km} km</strong>
            </div>
            <div className="summary-item">
              <span>Estimated Time:</span>
              <strong>{route.summary.estimated_time_min} min</strong>
            </div>
            <div className="summary-item">
              <span>Segments:</span>
              <strong>{route.summary.segment_count}</strong>
            </div>
          </div>
        )}

        <div className="alerts-section">
          <h3>Active Alerts</h3>
          {alerts.features && alerts.features.length > 0 ? (
            <div className="alerts-list">
              {alerts.features.map(alert => (
                <div key={alert.properties.alert_id} className={`alert-item ${alert.properties.severity}`}>
                  <div className="alert-header">
                    <span className="alert-type">{alert.properties.type}</span>
                    <span className={`alert-severity ${alert.properties.severity}`}>
                      {alert.properties.severity}
                    </span>
                  </div>
                  <p className="alert-description">{alert.properties.description}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-alerts">No active alerts</p>
          )}
        </div>

        <div className="info-section">
          <h4>About SmartNavNG</h4>
          <p>AI-powered navigation system for Nigerian cities using real-time traffic data and road condition analysis.</p>
          
          <div className="legend">
            <h4>Map Legend</h4>
            <div className="legend-item">
              <div className="legend-color route"></div>
              <span>Optimal Route</span>
            </div>
            <div className="legend-item">
              <div className="legend-color alert">⚠️</div>
              <span>Road Alert</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;