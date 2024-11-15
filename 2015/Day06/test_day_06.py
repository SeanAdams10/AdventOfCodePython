import day_06
import pytest
import numpy as np

@pytest.mark.parametrize("input, expected", [
    ('turn on 0,0 through 999,999', 1000*1000),
    ('turn off 0,0 through 999,999', 0),
    ('toggle 0,0 through 999,0', 1000),
    ('turn on 0,0 through 999,998', 1000*999)
])
def test_count_lights(input: str, expected: int):
    light_manager = day_06.LightManager(1000, 1000)
    light_manager.apply_action(input)
    assert light_manager.count_lights() == expected


def test_light_manager_constructor():
    x_size, y_size = 500, 500
    light_manager = day_06.LightManager(x_size, y_size)
    assert light_manager.lights.shape == (x_size, y_size)
    assert light_manager.lights.dtype == bool
    assert np.all(light_manager.lights == False)

def test_light_manager_constructor_2():
    x_size, y_size = 45, 103
    light_manager = day_06.LightManager(x_size, y_size)
    assert light_manager.lights.shape == (x_size, y_size)
    assert light_manager.lights.dtype == bool
    assert np.all(light_manager.lights == False)

def test_light_manager_constructor_3():
    x_size, y_size = 0, 103
    with pytest.raises(ValueError):
        light_manager = day_06.LightManager(x_size, y_size)

def test_light_manager_constructor_4():
    x_size, y_size = -1, 103
    with pytest.raises(ValueError):
        light_manager = day_06.LightManager(x_size, y_size)

def test_light_manager_constructor_5():
    x_size, y_size = 100, 0
    with pytest.raises(ValueError):
        light_manager = day_06.LightManager(x_size, y_size)

def test_light_manager2():
    x_size, y_size = 1000, 1000
    light_manager = day_06.LightManager(x_size, y_size, None)
    light_manager.apply_action('turn on 0,0 through 999,999')
    assert light_manager.count_lights() == 1000*1000
    light_manager.apply_action('turn off 0,0 through 999,999')
    assert light_manager.count_lights() == 0
    light_manager.apply_action('toggle 0,0 through 999,0')
    assert light_manager.count_lights() == 2000
    light_manager.apply_action('turn on 0,0 through 999,998')
    assert light_manager.count_lights() == 1000*999 + 2000






if __name__ == "__main__":
    pytest.main()