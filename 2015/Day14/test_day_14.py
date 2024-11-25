import day_14
import pytest



parsed_data = [
    ("Comet", 14, 10, 127),
    ("Dancer", 16, 11, 162)
]

def test_parse_data():
    base_data = [
        "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
        "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."
    ]
    
    parsed_data = [
        ("Comet", 14, 10, 127),
        ("Dancer", 16, 11, 162)
    ]
    assert day_14.parse_data(base_data) == parsed_data
    
@pytest.mark.parametrize("time, expected", [
    (1, [14, 16]),
    (10, [140, 160]),
    (11, [140, 176]),
    (12, [140, 176]),
    (138, [154, 176]),
    (1000, [1120, 1056])
])
def test_distance_calc(time, expected):
    parsed_data = [
        ("Comet", 14, 10, 127),
        ("Dancer", 16, 11, 162)
    ]

    assert day_14.distance_calc(parsed_data, time) == expected     
    

def test_part_1():
    with open("Part1Input.txt",'r', encoding='ascii') as f:
        input_data = f.readlines()
    
    pd = day_14.parse_data(input_data)
    assert max(day_14.distance_calc(pd, 2503)) == 2640

def test_part_2_sample():
   parsed_data = [
        ("Comet", 14, 10, 127),
        ("Dancer", 16, 11, 162)
        ]
   assert day_14.part_2_scoring(parsed_data, 1000) == [312, 689]
      
def test_part_2():
    with open("Part1Input.txt",'r', encoding='ascii') as f:
        input_data = f.readlines()
    
    pd = day_14.parse_data(input_data)
    assert max(day_14.part_2_scoring(pd, 2503)) == 1102