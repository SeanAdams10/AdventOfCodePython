# pylint: disable=missing-docstring
import pytest
import day_18


@pytest.fixture
def setup_sample():
    yield ['.#.#.#', '...##.', '#....#', '..#...', '#.#..#', '####..']


def test_parse_input():
    in_data = ['.#', '#.']
    target = {(0, 0): (False, (0, 1), (1, 1), (1, 0)),
              (0, 1): (True, (0, 0), (1, 0), (1, 1)),
              (1, 0): (True, (0, 0), (0, 1), (1, 1)),
              (1, 1): (False, (0, 0), (0, 1), (1, 0))}
    grd = day_18.LightGrid(in_data)
    result = grd.working
    for key in target:
        target_light, *target_neighbours = target[key]
        result_light, *result_neighbours = result[key]
        assert target_light == result_light
        assert sorted(target_neighbours) == sorted(result_neighbours)


@pytest.mark.parametrize('pos ,grid, target', [
    ((0, 0), (2, 2), [(0, 1), (1, 1), (1, 0)]),
    ((0, 1), (2, 2), [(0, 0), (1, 0), (1, 1)]),
    ((1, 0), (2, 2), [(0, 0), (0, 1), (1, 1)]),
    ((1, 1), (2, 2), [(0, 0), (0, 1), (1, 0)]),
    ((0, 0), (0, 0), []),
    ((0, 0), (1, 2), [(0, 1)]),
    ((1, 1), (4, 4), [(0, 0), (0, 1), (0, 2),
     (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]),
])
def test_create_neighbours(pos, grid, target):
    grd = day_18.LightGrid(['#.', '.#'])
    target = sorted(target)
    actual = sorted(grd._create_neighbours(grid, pos))
    assert actual == target


if __name__ == '__main__':
    pytest.main()
