// src/Map.js

import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Custom Hook to Handle Map Clicks and Marker Creation
const MapClickHandler = ({ addMarker }) => {
  useMapEvents({
    click(e) {
      addMarker(e.latlng);
    },
  });
  return null;
};

const Map = () => {
  const [markers, setMarkers] = useState([]);

  // Function to add marker to the state
  const addMarker = (latlng) => {
    const newMarker = {
      id: markers.length + 1,
      position: latlng,
      name: `Marker ${markers.length + 1}`,
    };
    setMarkers([...markers, newMarker]);
  };

  // Function to remove a marker
  const removeMarker = (id) => {
    setMarkers(markers.filter((marker) => marker.id !== id));
  };

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <MapContainer center={[40.655769, -73.938503]} zoom={13} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
        />
        <MapClickHandler addMarker={addMarker} />
        {markers.map((marker) => (
          <Marker key={marker.id} position={marker.position} eventHandlers={{
            click: () => {
              removeMarker(marker.id);
            },
          }}>
            <Popup>
              {marker.name} <br />
              <button onClick={() => removeMarker(marker.id)}>Delete Marker</button>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default Map;
