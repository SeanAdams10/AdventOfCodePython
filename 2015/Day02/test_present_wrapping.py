import pytest
from present_wrapping import PresentWrapping


def test_present_wrapping():
    pw = PresentWrapping(2, 3, 4)
    assert pw.calculate_wrapping_paper() == 58


def test_present_wrapping_2():
    pw = PresentWrapping(1, 1, 10)
    assert pw.calculate_wrapping_paper() == 43


def test_present_wrapping_3():
    pw = PresentWrapping(1, 1, 1)
    assert pw.calculate_wrapping_paper() == 7


def test_present_wrapping_3():
    with pytest.raises(TypeError):
        pw = PresentWrapping(1, 1)


def test_ribbon_1():
    pw = PresentWrapping(2, 3, 4)
    assert pw.calculate_ribbon() == 34


def test_ribbon_2():
    pw = PresentWrapping(1, 1, 10)
    assert pw.calculate_ribbon() == 14
