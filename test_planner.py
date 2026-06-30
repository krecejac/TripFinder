from main import split_places, distance, nearest, Place
import math
from pytest import approx

#Splitting places per day
def test_split_empty():
    assert split_places([], 3) == [[],[],[]]

def test_split_single_place():
    assert split_places(["A"], 1) == [["A"]]

def test_split_even():
    assert split_places(["A", "B", "C", "D"], 2) == [["A", "B"], ["C", "D"]]

def test_split_uneven():
    assert split_places(["A", "B", "C", "D", "E"], 2) == [["A", "B"], ["C", "D", "E"]]

# Distances
def test_distance_basic():
    a = Place(name="A", lat=0, lng=0)
    b = Place(name="B", lat=3, lng=4)
    assert distance(a, b) == 5

def test_distance_float():
    a = Place(name="A", lat=0, lng=0)
    b = Place(name="B", lat=0.1, lng=0.2)
    assert distance(a, b) == approx(math.sqrt(0.05))

# Nearest neighbor
def test_nearest_basic():
    a = Place(name="A", lat=0, lng=0)
    b = Place(name="B", lat=1, lng=1)
    c = Place(name="C", lat=2, lng=2)
    assert nearest(a, [b, c]) == b

def test_nearest_empty():
    a = Place(name="A", lat=0, lng=0)
    assert nearest(a, []) is None

def test_nearest_multiple():
    a = Place(name="A", lat=0, lng=0)
    b = Place(name="B", lat=1, lng=1)
    c = Place(name="C", lat=2, lng=2)
    d = Place(name="D", lat=0.5, lng=0.5)
    assert nearest(a, [b, c, d]) == d

def test_nearest_same_distance():
    a = Place(name="A", lat=0, lng=0)
    b = Place(name="B", lat=1, lng=1)
    c = Place(name="C", lat=-1, lng=-1)
    assert nearest(a, [b, c]) in [b, c]

def test_nearest_identical():
    a = Place(name="A", lat=0, lng=0)
    b = Place(name="B", lat=0, lng=0)
    assert nearest(a, [b]) == b

