# pylint: disable=missing-docstring
import pytest
from floor_counter import FloorCounter


def test_initial_floor():
    fc = FloorCounter()
    assert fc.floor == 0


def test_process_instructions_empty():
    fc = FloorCounter()
    assert fc.process_instructions('') == 0


def test_process_instructions_balanced():
    fc = FloorCounter()
    assert fc.process_instructions('()') == 0


def test_process_instructions_single_up():
    fc = FloorCounter()
    assert fc.process_instructions('(') == 1


def test_process_instructions_double_up():
    fc = FloorCounter()
    assert fc.process_instructions('(())') == 0


def test_process_instructions_up_and_down():
    fc = FloorCounter()
    assert fc.process_instructions('()()') == 0


def test_process_instructions_multiple_up():
    fc = FloorCounter()
    assert fc.process_instructions('(((') == 3


def test_process_instructions_multiple_down():
    fc = FloorCounter()
    assert fc.process_instructions(')))') == -3


def test_process_instructions_mixed():
    fc = FloorCounter()
    assert fc.process_instructions('(()))(') == 0


def test_process_instructions_imbalanced_up():
    fc = FloorCounter()
    assert fc.process_instructions('(()(()') == 2


def test_process_instructions_imbalanced_down():
    fc = FloorCounter()
    assert fc.process_instructions('())())') == -2


def test_basement_1():
    fc = FloorCounter()
    assert fc.basement(')') == 1


def test_basement_2():
    fc = FloorCounter()
    assert fc.basement('()') is None


def test_basement_3():
    fc = FloorCounter()
    assert fc.basement('(') is None


def test_basement_4():
    fc = FloorCounter()
    assert fc.basement('())') == 3


def test_basement_5():
    fc = FloorCounter()
    assert fc.basement('()())') == 5


if __name__ == "__main__":
    pytest.main()
