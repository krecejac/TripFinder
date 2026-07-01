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

  const [tripsPlaces, setTripsPlaces] = useState<{ [key: number]: any[] }>({});

  useEffect(() => {
    trips.forEach((trip) => {
      fetch(`http://127.0.0.1:8000/trips/${trip.id}/places`)
        .then((response) => response.json())
        .then((data) => {
          setTripsPlaces((prev) => ({ ...prev, [trip.id]: data }));
        });
    });
  }, [trips]);

  const [selectedTripId, setSelectedTripId] = useState<number | null>(null);

  const [newName, setNewName] = useState("");
  const [newLat, setNewLat] = useState("");
  const [newLng, setNewLng] = useState("");

  const addPlace = () => {
    if (selectedTripId === null) return;
    fetch(`http://127.0.0.1:8000/trips/${selectedTripId}/places`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: newName,
        lat: parseFloat(newLat),
        lng: parseFloat(newLng),
      }),
    })
      .then((response) => response.json())
      .then((newPlace) => {
        setTripsPlaces((prev) => ({
          ...prev,
          [selectedTripId as number]: [
            ...(prev[selectedTripId as number] || []),
            newPlace,
          ],
        }));
        setNewName("");
        setNewLat("");
        setNewLng("");
      });
  };

  return (
    <div>
      <h1>Moje výlety</h1>
      <div>
        <input
          placeholder="Název místa"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <input
          placeholder="Lat"
          value={newLat}
          onChange={(e) => setNewLat(e.target.value)}
        />
        <input
          placeholder="Lng"
          value={newLng}
          onChange={(e) => setNewLng(e.target.value)}
        />
        <button onClick={addPlace}>Přidat místo</button>
      </div>
      <ul>
        {trips.map((trip) => (
          <li
            key={trip.id}
            onClick={() => setSelectedTripId(trip.id)}
            style={{
              cursor: "pointer",
              fontWeight: selectedTripId === trip.id ? "bold" : "normal",
            }}
          >
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
        {Object.entries(tripsPlaces).flatMap(([tripId, places]) =>
          places.map((place: any) => (
            <Marker key={place.id} position={[place.lat, place.lng]}>
              <Popup>{place.name}</Popup>
            </Marker>
          )),
        )}
      </MapContainer>
    </div>
  );
}

export default App;
