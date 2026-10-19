import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents, GeoJSON } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';

// Component to handle map click events
function MapEvents({ onLocationClick }) {
  useMapEvents({
    click(e) {
      onLocationClick(e.latlng);
    },
  });
  return null;
}

function App() {
  const [locationData, setLocationData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [layers, setLayers] = useState({});

  // Load available layers on mount
  useEffect(() => {
    const loadLayers = async () => {
      try {
        // In a real app, we'd have an endpoint /api/layers
        // For now, we'll fetch the GeoJSON files directly if they are served statically
        // or just mock the structure for the overlay.
        // For the skeleton, we'll assume the backend provides the GeoJSON.
        const response = await axios.get('http://localhost:8000/api/layers');
        setLayers(response.data);
      } catch (error) {
        console.error("Error loading layers:", error);
      }
    };
    loadLayers();
  }, []);

  const handleLocationClick = async (latlng) => {
    setLoading(true);
    try {
      const { lat, lng } = latlng;
      const response = await axios.get(`http://localhost:8000/api/query?lat=${lat}&lon=${lng}`);
      setLocationData(response.data);
    } catch (error) {
      console.error("Error fetching location data:", error);
      alert("Failed to fetch data from the backend API.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ height: '100vh', width: '100vw', position: 'relative' }}>
      <MapContainer 
        center={[35.7796, -78.6382]} 
        zoom={13} 
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        <MapEvents onLocationClick={handleLocationClick} />
        
        {/* Render GeoJSON layers */}
        {Object.entries(layers).map(([layerName, geoData]) => (
          <GeoJSON 
            key={layerName} 
            data={geoData} 
            style={{
              color: layerName === 'bus_routes' ? 'blue' : 'red',
              weight: 2,
              opacity: 0.6
            }} 
          />
        ))}

        {locationData && (
          <Popup position={locationData.location} onClose={() => setLocationData(null)}>
            <div style={{ minWidth: '200px' }}>
              <strong style={{ fontSize: '1.1em' }}>Location Insights</strong><br />
              <small>{locationData.location.lat.toFixed(4)}, {locationData.location.lon.toFixed(4)}</small>
              <hr />
              {loading ? (
                <p>Loading insights...</p>
              ) : (
                <div>
                  {locationData.findings.length > 0 ? (
                    locationData.findings.map((finding, index) => (
                      <div key={index} style={{ marginBottom: '10px', borderLeft: `4px solid ${finding.layer === 'bus_routes' ? 'blue' : 'red'}`, paddingLeft: '8px' }}>
                        <strong>{finding.layer.replace('_', ' ')}:</strong> {finding.count} feature(s) found.
                      </div>
                    ))
                  ) : (
                    <p>No intersecting data found at this location.</p>
                  )}
                </div>
              )}
            </div>
          </Popup>
        )}
      </MapContainer>
      
      {loading && (
        <div style={{ 
          position: 'absolute', top: 20, right: 20, zIndex: 1000, 
          background: 'white', padding: '10px', borderRadius: '5px', boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
          fontFamily: 'sans-serif'
        }}>
          Querying Backend...
        </div>
      )}
    </div>
  );
}

export default App;
