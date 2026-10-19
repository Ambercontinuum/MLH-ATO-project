import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Popup, useMapEvents, GeoJSON } from 'react-leaflet';
import L from 'leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';

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

  useEffect(() => {
    const loadLayers = async () => {
      try {
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
    <div style={{ height: '100vh', width: '100vw', position: 'relative', fontFamily: 'sans-serif' }}>
      <MapContainer 
        center={[35.815159, -78.626145]}
        zoom={16}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />
        <MapEvents onLocationClick={handleLocationClick} />
        
        {Object.entries(layers).map(([layerName, geoData]) => (
          <GeoJSON 
            key={layerName} 
            data={geoData} 
            pointToLayer={(_, latlng) => L.circleMarker(latlng, {
              radius: 5, color: '#0052cc', fillColor: '#0052cc', fillOpacity: 0.9
            })}
            style={{
              color: layerName === 'bus_stops' ? '#0052cc' : '#d32f2f',
              weight: 2,
              opacity: 0.6
            }} 
          />
        ))}

        {locationData && (
          <Popup position={locationData.location} onClose={() => setLocationData(null)}>
            <div style={{ minWidth: '280px', maxHeight: '400px', overflowY: 'auto' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '16px' }}>CivicPulse Insight</h3>
              <p style={{ fontSize: '12px', color: '#666', margin: '0 0 12px 0' }}>
                {locationData.location.lat.toFixed(4)}, {locationData.location.lon.toFixed(4)}
              </p>
              
              <div style={{ 
                background: '#f5f5f5', padding: '10px', borderRadius: '4px', 
                borderLeft: '4px solid #333', marginBottom: '12px', fontSize: '13px', fontStyle: 'italic' 
              }}>
                {loading ? "Generating AI Brief..." : locationData.ai_brief}
              </div>

              <div style={{ fontSize: '13px' }}>
                <strong>Evidence:</strong>
                <div style={{ marginTop: '5px' }}>
                  {locationData.findings.map((finding, index) => (
                    <div key={index} style={{ 
                      marginBottom: '6px', 
                      padding: '4px', 
                      background: '#fff0f0',
                      border: '1px solid #d32f2f',
                      borderRadius: '3px'
                    }}>
                      <span style={{ fontWeight: 'bold' }}>Stop {finding.stop_id} in mapped {finding.flood_zone} area {finding.flood_area_id}</span>
                    </div>
                  ))}
                </div>
              </div>
              
              <div style={{ marginTop: '12px', fontSize: '11px', color: '#888' }}>
                Source records IDs: {locationData.source_records.map(r => r.id).join(', ')}
              </div>
              <div style={{ marginTop: '8px', fontSize: '11px' }}>
                {locationData.source_records.map((r, i) => (
                  <div key={`${r.layer}-${r.id}-${i}`}>
                    <a href={r.source_url} target="_blank" rel="noreferrer">{r.layer}: {r.id}</a>
                  </div>
                ))}
              </div>
              <p style={{ fontSize: '11px', color: '#666' }}>{locationData.limitations}</p>
            </div>
          </Popup>
        )}
      </MapContainer>
      
      {loading && (
        <div style={{ 
          position: 'absolute', top: 20, right: 20, zIndex: 1000, 
          background: 'white', padding: '10px 20px', borderRadius: '20px', 
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)', fontWeight: 'bold'
        }}>
          Analyzing intersections...
        </div>
      )}
    </div>
  );
}

export default App;
