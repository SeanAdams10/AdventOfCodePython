# pylint: disable=missing-docstring
import pytest
from shapely.geometry import Polygon
import day_12_v2 as day_12
from collections import deque





@pytest.mark.parametrize("coords, expected_length", [
    ([(2, 1.333), (2, 2), (0, 2), (0, 0), (2, 0), (2, 1.333)], 4),
    ([(0, 0), (2, 0), (2, 0.666), (2, 1.333), (2, 2), (0, 2), (0, 0)], 4),
    ([(4, 4), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4)], 4)
    # Add more test cases here if needed
])
def test_simplify_poly(coords, expected_length):
    dq_coords = deque(coords[:-1])
    for _ in range(len(coords)):
        tst_coords = list(dq_coords) + [dq_coords[0]]
        result_list = day_12.simplify_polygon(tst_coords)
        result = Polygon(result_list)
        assert len(result.exterior.coords) - 1 == expected_length
        dq_coords.rotate(1)

@pytest.mark.parametrize("p1, p2, p3, expected", [
    ((0, 0), (1, 1), (2, 2), True),
    ((0, 0), (1, 1), (2, 3), False),
    ((0, 0), (1, 1), (3, 3), True),
    ((0, 0), (1, 1), (4, 4), True),
    ((1, 1), (0, 0), (3, 3), True),
])
def test_are_collinear(p1, p2, p3, expected):
    assert day_12.are_collinear(p1, p2, p3) == expected



def test_read_input():
    data = ['OXO', 'XOX', 'OXO']
    result = day_12.read_input(data)
    assert len(result) == 9
    assert result[0].value == 'O'
    assert result[1].value == 'X'
    assert result[0].cells[0] ==(0,0)
    # assert result[0].group is None
    assert result[0].borders == 4
    assert result[0].area == 1

def test_clean_inner_and_outer():
    exterior = [(5.0, 5.0), (5.0, 4.0), (5.0, 3.0), (5.0, 2.0), (5.0, 1.0), (5.0, 0.0), (4.0, 0.0), (3.0, 0.0), (2.0, 0.0), (1.0, 0.0), (0.0, 0.0), (0.0, 1.0), (0.0, 2.0), (0.0, 3.0), (0.0, 4.0), (0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0), (5.0, 5.0)]
    interior_1 = [(2.0, 4.0), (1.0, 4.0), (1.0, 3.0), (1.0, 2.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0), (4.0, 2.0), (4.0, 3.0), (4.0, 4.0), (3.0, 4.0), (2.0, 4.0)]
    test_poly = Polygon(exterior, [interior_1])
    result = day_12.simplfy_inner_and_outer(test_poly)
    assert len(result.exterior.coords) -1 == 4
    assert len(result.interiors[0].coords) -1 == 4


if __name__ == "__main__":
    pytest.main()
