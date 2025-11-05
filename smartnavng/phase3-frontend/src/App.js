import React, { useState, useEffect } from 'react';
import MapView from './components/MapView';
import RouteForm from './components/RouteForm';
import Sidebar from './components/Sidebar';
import { login } from './services/api';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [route, setRoute] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Auto-login with demo credentials
    const autoLogin = async () => {
      try {
        const result = await login('demo', 'demo123');
        setToken(result.access_token);
        localStorage.setItem('token', result.access_token);
        setUser({ username: 'demo' });
      } catch (error) {
        console.error('Auto-login failed:', error);
      }
    };

    if (!token) {
      autoLogin();
    } else {
      setUser({ username: 'demo' });
    }
  }, [token]);

  const handleRouteCalculated = (routeData) => {
    setRoute(routeData);
  };

  const handleAlertsLoaded = (alertsData) => {
    setAlerts(alertsData);
  };

  if (!token) {
    return (
      <div className="app-loading">
        <div className="loading-spinner"></div>
        <p>Loading SmartNavNG...</p>
      </div>
    );
  }

  return (
    <div className="app">
      <Sidebar 
        user={user}
        route={route}
        alerts={alerts}
        loading={loading}
      />
      
      <div className="app-main">
        <div className="app-header">
          <h1>SmartNavNG</h1>
          <p>AI-Powered Navigation for Nigerian Cities</p>
        </div>
        
        <RouteForm 
          onRouteCalculated={handleRouteCalculated}
          onAlertsLoaded={handleAlertsLoaded}
          setLoading={setLoading}
          token={token}
        />
        
        <MapView 
          route={route}
          alerts={alerts}
        />
      </div>
    </div>
  );
}

export default App;