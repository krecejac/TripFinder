from sqlalchemy.orm import Session
from database import engine, get_db
import models
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware # for CORS
from pydantic import BaseModel
import math
import httpx

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#abysme mohli volat z frontnendu, musime povolit CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
class Trip(BaseModel):
    city: str
    days: int

class Place(BaseModel):
    name: str
    lat: float
    lng: float

@app.get("/trips")
def list_trips(db: Session = Depends(get_db)):
    trips = db.query(models.Trip).all()
    return trips

@app.post("/trips")
def create_trip(trip: Trip, db: Session = Depends(get_db)):
    db_trip = models.Trip(city=trip.city, days=trip.days)
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

@app.post("/plan")
def plan_trip(places: list[Place], days: int):
    ordered = sort_by_nearest(places)
    result = split_places(ordered, days)
    return {"days": days, "itinerary": result}

@app.post("/trips/{trip_id}/places")
def add_place(trip_id: int, place: Place, db: Session = Depends(get_db)):
    db_place = models.Place(
        name=place.name,
        lat=place.lat,
        lng=place.lng,
        trip_id=trip_id
    )
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

@app.get("/trips/{trip_id}/places")
def list_places(trip_id: int, db: Session = Depends(get_db)):
    places = db.query(models.Place).filter(models.Place.trip_id == trip_id).all()
    return places

@app.delete("/places/{place_id}")
def delete_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    db.delete(place)
    db.commit()
    return {"deleted": place_id}

@app.patch("/places/{place_id}")
def update_place(place_id: int, place: Place, db: Session = Depends(get_db)):
    db_place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    db_place.name = place.name
    db_place.lat = place.lat
    db_place.lng = place.lng
    db.commit()
    db.refresh(db_place)
    return db_place

def split_places(places, days):
    n = len(places)
    result = []
    for i in range(days):
        start = i * n // days
        end = (i + 1) * n // days
        result.append(places[start:end])
    return result

def distance(place1, place2):
    # Calculate the distance between two places using the Euclidian formula
    return math.sqrt((place1.lat - place2.lat) ** 2 + (place1.lng - place2.lng) ** 2)

def nearest(point, candidates):
    nearest_place = None
    nearest_dist = float('inf')
    for place in candidates:
        d = distance(point, place)
        if d < nearest_dist:
            nearest_dist = d
            nearest_place = place
    return nearest_place

def sort_by_nearest(places):
    remaining = places.copy()
    ordered = []
    start = remaining.pop(0)
    ordered.append(start)
    while remaining:
        next_place = nearest(start, remaining)
        ordered.append(next_place)
        remaining.remove(next_place)
        start = next_place
    return ordered

def geocode(city: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json"}
    headers = {"User-Agent": "TripPlanner"}
    response = httpx.get(url, params=params, headers=headers)
    data = response.json()
    first = data[0]
    return {"lat": float(first["lat"]), "lng": float(first["lon"])}

@app.get("/geocode/{city}")
def geocode_endpoint(city: str):
    return geocode(city)

def find_places(lat: float, lng: float):
    query = f"""
    [out:json];
    (
      node[natural=beach](around:15000,{lat},{lng});
      node[tourism=viewpoint](around:15000,{lat},{lng});
    );
    out 20;
    """
    url = "https://overpass-api.de/api/interpreter"
    try:
        response = httpx.post(
            url,
            content=query,
            headers={"User-Agent": "TripPlanner"},
            timeout=30.0,
        )
        data = response.json()
    except (httpx.HTTPError, ValueError):
        raise HTTPException(status_code=503, detail="Overpass je nedostupny, zkus to znovu")

    places = []
    for element in data["elements"]:
        tags = element.get("tags", {})
        if "name" in tags:
            places.append({
                "name": tags["name"],
                "lat": element["lat"],
                "lng": element["lon"],
            })
    return places

@app.get("/find/{city}")
def find_endpoint(city: str):
    coords = geocode(city)
    return find_places(coords["lat"], coords["lng"])