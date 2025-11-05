import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in Leaflet with Webpack
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

const MapView = ({ route, alerts }) => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const layersRef = useRef({
    route: null,
    alerts: null
  });

  useEffect(() => {
    // Initialize map
    if (!mapInstanceRef.current) {
      mapInstanceRef.current = L.map(mapRef.current).setView([6.5244, 3.3792], 12);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(mapInstanceRef.current);
    }

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    if (!mapInstanceRef.current || !route) return;

    // Clear existing route
    if (layersRef.current.route) {
      mapInstanceRef.current.removeLayer(layersRef.current.route);
    }

    // Add new route
    if (route.features && route.features.length > 0) {
      const routeLayer = L.geoJSON(route, {
        style: {
          color: '#3498db',
          weight: 6,
          opacity: 0.8
        }
      }).addTo(mapInstanceRef.current);

      layersRef.current.route = routeLayer;
      
      // Fit map to route bounds
      const bounds = routeLayer.getBounds();
      if (bounds.isValid()) {
        mapInstanceRef.current.fitBounds(bounds, { padding: [20, 20] });
      }
    }
  }, [route]);

  useEffect(() => {
    if (!mapInstanceRef.current || !alerts) return;

    // Clear existing alerts
    if (layersRef.current.alerts) {
      mapInstanceRef.current.removeLayer(layersRef.current.alerts);
    }

    // Add new alerts
    if (alerts.features && alerts.features.length > 0) {
      const alertIcon = L.divIcon({
        className: 'alert-marker',
        html: '⚠️',
        iconSize: [20, 20],
        iconAnchor: [10, 10]
      });

      const alertsLayer = L.geoJSON(alerts, {
        pointToLayer: (feature, latlng) => {
          return L.marker(latlng, { icon: alertIcon });
        },
        onEachFeature: (feature, layer) => {
          const props = feature.properties;
          layer.bindPopup(`
            <div>
              <strong>${props.type}</strong><br/>
              Severity: ${props.severity}<br/>
              ${props.description}
            </div>
          `);
        }
      }).addTo(mapInstanceRef.current);

      layersRef.current.alerts = alertsLayer;
    }
  }, [alerts]);

  return (
    <div 
      ref={mapRef} 
      style={{ 
        height: '100%', 
        width: '100%',
        minHeight: '400px'
      }} 
    />
  );
};

export default MapView;