import pytest
import day_13

def test_parse_input():
    happiness_changes = [
        "Alice would gain 54 happiness units by sitting next to Bob.",
        "Alice would lose 79 happiness units by sitting next to Carol.",
        "Alice would lose 2 happiness units by sitting next to David.",
        "Bob would gain 83 happiness units by sitting next to Alice.",
        "Bob would lose 7 happiness units by sitting next to Carol.",
        "Bob would lose 63 happiness units by sitting next to David.",
        "Carol would lose 62 happiness units by sitting next to Alice.",
        "Carol would gain 60 happiness units by sitting next to Bob.",
        "Carol would gain 55 happiness units by sitting next to David.",
        "David would gain 46 happiness units by sitting next to Alice.",
        "David would lose 7 happiness units by sitting next to Bob.",
        "David would gain 41 happiness units by sitting next to Carol."
    ]

    happiness_data = {
        ("Alice", "Bob"): 54,
        ("Alice", "Carol"): -79,
        ("Alice", "David"): -2,
        ("Bob", "Alice"): 83,
        ("Bob", "Carol"): -7,
        ("Bob", "David"): -63,
        ("Carol", "Alice"): -62,
        ("Carol", "Bob"): 60,
        ("Carol", "David"): 55,
        ("David", "Alice"): 46,
        ("David", "Bob"): -7,
        ("David", "Carol"): 41
    }
    
    
    assert day_13.parse_input(happiness_changes) == happiness_data
    

def test_unique_guests():
    happiness_data = {
        ("Alice", "Bob"): 54,
        ("Alice", "Carol"): -79,
        ("Alice", "David"): -2,
        ("Bob", "Alice"): 83,
        ("Bob", "Carol"): -7,
        ("Bob", "David"): -63,
        ("Carol", "Alice"): -62,
        ("Carol", "Bob"): 60,
        ("Carol", "David"): 55,
        ("David", "Alice"): 46,
        ("David", "Bob"): -7,
        ("David", "Carol"): 41
    }
    
    assert day_13.unique_guests(happiness_data) == set(["Alice", "Bob", "Carol", "David"])


def test_measure_combo():
    happiness_data = {
        ("Alice", "Bob"): 54,
        ("Alice", "Carol"): -79,
        ("Alice", "David"): -2,
        ("Bob", "Alice"): 83,
        ("Bob", "Carol"): -7,
        ("Bob", "David"): -63,
        ("Carol", "Alice"): -62,
        ("Carol", "Bob"): 60,
        ("Carol", "David"): 55,
        ("David", "Alice"): 46,
        ("David", "Bob"): -7,
        ("David", "Carol"): 41
    }
    
    # unique_guests = set(["Alice", "Bob", "Carol", "David"])
    this_combo = ("Alice", "Bob", "Carol", "David")
    assert day_13.measure_combo(happiness_data, this_combo) == 54+ 83+ -7 + 60 + 55+ 41 + 46+ -2

    this_combo = ("Alice", "Carol", "Bob", "David")
    assert day_13.measure_combo(happiness_data, this_combo) == -79 -62 + 60 -7 + -63 + -7 + 46 + -2

def test_part_1_sample():
    happiness_data = {
        ("Alice", "Bob"): 54,
        ("Alice", "Carol"): -79,
        ("Alice", "David"): -2,
        ("Bob", "Alice"): 83,
        ("Bob", "Carol"): -7,
        ("Bob", "David"): -63,
        ("Carol", "Alice"): -62,
        ("Carol", "Bob"): 60,
        ("Carol", "David"): 55,
        ("David", "Alice"): 46,
        ("David", "Bob"): -7,
        ("David", "Carol"): 41
    }
    
    table = ('Alice',  'David', 'Carol','Bob')
    best=330
    assert day_13.find_best_combo(happiness_data)[0] == best
    # assert day_13.find_best_combo(happiness_data)[1] == table
    
    
def test_part_1():
    with open(".\\2015\Day13\Part1Input.txt",'r',encoding='ascii') as f:
        happiness_changes = f.readlines()
        best, table = day_13.find_best_combo(day_13.parse_input(happiness_changes))
        assert best == 733
    
def test_part_2():
    with open(".\\2015\Day13\Part1Input.txt",'r',encoding='ascii') as f:
        happiness_changes = f.readlines()
        happiness_details = day_13.parse_input(happiness_changes)
        
    guests = day_13.unique_guests(happiness_details)
    for guest in guests:
        happiness_details[('Self', guest)] = 0
        happiness_details[(guest, 'Self')] = 0
    
    best, table = day_13.find_best_combo(happiness_details)
    assert best == 725
    
    



if __name__ == "__main__":
    pytest.main()