from main import split_places

def test_split_empty():
    assert split_places([], 3) == [[],[],[]]

def test_split_single_place():
    assert split_places(["A"], 1) == [["A"]]

def test_split_even():
    assert split_places(["A", "B", "C", "D"], 2) == [["A", "B"], ["C", "D"]]

def test_split_uneven():
    assert split_places(["A", "B", "C", "D", "E"], 2) == [["A", "B"], ["C", "D", "E"]]

