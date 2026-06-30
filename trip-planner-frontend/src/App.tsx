import { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

type Trip = {
  id: number;
  city: string;
  days: number;
};

function App() {
  const [trips, setTrips] = useState<Trip[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/trips")
      .then((response) => response.json())
      .then((data) => setTrips(data));
  }, []);

  return (
    <div>
      <h1>Moje výlety</h1>
      <ul>
        {trips.map((trip) => (
          <li key={trip.id}>
            {trip.city} — {trip.days} dní
          </li>
        ))}
      </ul>

      <MapContainer
        center={[50.0875, 14.4214]}
        zoom={13}
        style={{ height: "500px", width: "100%" }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={[50.0875, 14.4214]}>
          <Popup>Praha</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}

export default App;
