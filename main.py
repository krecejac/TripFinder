from fastapi import FastAPI
from pydantic import BaseModel
import math

app = FastAPI()

class Trip(BaseModel):
    city: str
    days: int

class Place(BaseModel):
    name: str
    lat: float
    lng: float

#random commentt
@app.post("/plan")
def plan_trip(places: list[Place], days: int):
    ordered = sort_by_nearest(places)
    result = split_places(ordered, days)
    return {"days": days, "itinerary": result}

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