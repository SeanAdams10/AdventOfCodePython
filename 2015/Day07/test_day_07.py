# pylint: disable=missing-docstring
import pytest
import day_07
import typeguard


# @pytest.mark.parametrize("test_input, expected", [
#     ("123 -> x", ("Assign", "123", "x")),
#     ("456 -> y", ("Assign", "456", "y")),
#     ("x AND y -> d", ("AND", "x",  "y", "d")),
#     ("x OR y -> e", ("OR", "x",  "y", "e")),
#     ("x LSHIFT 2 -> f", ("LSHIFT", "x",  "2", "f")),
#     ("y RSHIFT 2 -> g", ("RSHIFT", "y",  "2", "g")),
#     ("NOT x -> h", ("NOT", "x",  "h"))
# ])
# def test_parse_input(test_input, expected):
#     assert day_07.Wiring.parse_input(test_input) == expected

def test_full():
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    tst = day_07.Wiring()
    tst.load_instructions(input_data)
    wire_result = {'x': 123, 'y': 456, 'd': 72, 'e': 507,
                   'f': 492, 'g': 114, 'h': 65412, 'i': 65079}
    for wire in wire_result:
        tst.solve_for_x(wire)
    for wire, value in wire_result.items():
        assert tst.wires[wire]["value"] == value


def test_load_instructions():
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    tst = day_07.Wiring()
    tst.load_instructions(input_data)
    assert tst.wires['x'] == {"instruction": "123 -> x", "value": -1}
    assert tst.wires['y'] == {"instruction": "456 -> y", "value": -1}
    assert tst.wires['d'] == {"instruction": "x AND y -> d", "value": -1}
    assert tst.wires['e'] == {"instruction": "x OR y -> e", "value": -1}
    assert tst.wires['f'] == {"instruction": "x LSHIFT 2 -> f", "value": -1}
    assert tst.wires['g'] == {"instruction": "y RSHIFT 2 -> g", "value": -1}
    assert tst.wires['h'] == {"instruction": "NOT x -> h", "value": -1}
    assert tst.wires['i'] == {"instruction": "NOT y -> i", "value": -1}


@ pytest.mark.parametrize("target, expected", [
    ('x', 123),
    ('y', 456),
    ('d', 72),
    ('e', 507),
    ('f', 492),
    ('g', 114),
    ('h', 65412),
    ('i', 65079)
])
def test_solve_for_x(target, expected):
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    tst = day_07.Wiring()
    tst.load_instructions(input_data)

    tst.solve_for_x(target)
    assert tst.wires[target]["value"] == expected


@ pytest.mark.parametrize("target, value, wire_expected", [
    ('x', 123, {"instruction": "123 -> x", "value": 123}),
    ('y', 456, {"instruction": "456 -> y", "value": 456}),
])
def test_assign(target, value, wire_expected):
    tst = day_07.Wiring()
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    tst.load_instructions(input_data)
    tst.assign_literal(target_wire=target, value=int(value))
    assert tst.wires[target] == wire_expected
    assert tst.wires[target]["value"] == value


def test_string_representation():
    tst = day_07.Wiring()
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    expected = {"x": 123, "y": 456, "d": 72, "e": 507,
                "f": 492, "g": 114, "h": 65412, "i": 65079}

    tst.load_instructions(input_data)
    for key, value in expected.items():
        tst.assign_literal(target_wire=key, value=value)

    expected_str = '\n'.join(
        [f"{key}: {val}" for key, val in expected.items()])

    assert str(tst) == expected_str.strip()


@ pytest.mark.parametrize("wire, value", [
    ("x", "123"),
    ("y", None),
    (1, 1),
    ([], 1),
    ('a', [])
])
def test_assign_error(wire, value) -> None:
    """
    test the type checking on the assign method
    """
    tst = day_07.Wiring()
    with pytest.raises(typeguard.TypeCheckError):
        tst.assign_literal(target_wire=wire, value=value)


@ pytest.mark.parametrize("x, y, expected", [
    (123, 456, 72),
    (1, 256, 0),
    (256, 1, 0),
    (256, 256, 256),
    (0, 0, 0)
])
def test_and(x, y, expected):
    tst = day_07.Wiring()
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    tst.load_instructions(input_data)
    tst.assign_literal(target_wire='x', value=x)
    tst.assign_literal(target_wire='y', value=y)
    tst.and_gate(x='x', y='y', target='i')
    assert tst.wires['i']["value"] == expected
    assert tst.wires['i']["instruction"] == "NOT y -> i"


@ pytest.mark.parametrize("x, y, expected", [
    (123, 456, 507),
    (1, 256, 257),
    (256, 1, 257),
    (256, 256, 256),
    (0, 0, 0)
])
def test_or(x, y, expected):
    tst = day_07.Wiring()
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    tst.load_instructions(input_data)

    tst.assign_literal(target_wire='x', value=x)
    tst.assign_literal(target_wire='y', value=y)
    tst.or_gate(x='x', y='y', target='i')
    assert tst.wires['i']["value"] == expected
    assert tst.wires['i']["instruction"] == "NOT y -> i"


@ pytest.mark.parametrize("value, expected", [
    (10, 65525),
    (0, 65535),
    (65535, 0)])
def test_not(value, expected):
    tst = day_07.Wiring()
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    tst.load_instructions(input_data)

    tst.assign_literal(target_wire='x', value=value)
    tst.not_gate(input_wire='x', target_wire='i')
    assert tst.wires['i']["value"] == expected
    assert tst.wires['i']["instruction"] == "NOT y -> i"


@ pytest.mark.parametrize("value, places, expected", [
    (10, 1, 20),
    (0, 1, 0),
    (65535, 1, 65534),
    (32767, 2, 65532),
    (32768, 1, 0)])
def test_shift_left(value, places, expected):
    tst = day_07.Wiring()
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    tst.load_instructions(input_data)

    tst.assign_literal(target_wire='x', value=value)
    tst.shift_left(input_wire='x', target_wire='i', places=places)

    assert tst.wires['i']["value"] == expected
    assert tst.wires['i']["instruction"] == "NOT y -> i"


@ pytest.mark.parametrize("value, places, expected", [
    (10, 1, 5),
    (0, 1, 0),
    (65535, 1, 32767),
    (1, 1, 0),
    (65535, 16, 0)])
def test_shift_right(value, places, expected):
    tst = day_07.Wiring()
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    tst.load_instructions(input_data)

    tst.assign_literal(target_wire='x', value=value)
    tst.shift_right(input_wire='x', target_wire='i', places=places)

    assert tst.wires['i']["value"] == expected
    assert tst.wires['i']["instruction"] == "NOT y -> i"


@ pytest.mark.parametrize("source, expected", [
    ('x', 123),
    ('y', 0),
    ('d', 65535),
])
def test_assign_wire(source, expected):
    tst = day_07.Wiring()
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    tst.load_instructions(input_data)

    tst.assign_literal(target_wire=source, value=expected)
    tst.assign_wire(source_wire=source, target_wire='i')
    assert tst.wires['i']["value"] == expected
    assert tst.wires['i']["instruction"] == "NOT y -> i"


@pytest.mark.parametrize("target, value", [
    ('x', -1),
    ('y', 65536),
    ('d', 100000),
])
def test_assign_wire_error(target, value) -> None:
    """
    test the type checking on the assign method
    """
    tst = day_07.Wiring()
    input_data = ["123 -> x", "456 -> y", "x AND y -> d", "x OR y -> e",
                  "x LSHIFT 2 -> f", "y RSHIFT 2 -> g", "NOT x -> h", "NOT y -> i"]
    tst.load_instructions(input_data)

    with pytest.raises(ValueError):
        tst.assign_literal(target_wire=target, value=value)


def test_part_1():
    with open(r"2015/Day07/Part1Input.txt", encoding="ascii") as f:
        lines = f.readlines()

    tst = day_07.Wiring()
    tst.load_instructions(lines)

    assert tst.solve_for_x("a") == 3176


def test_part_2():
    with open(r"2015/Day07/Part1Input.txt", encoding="ascii") as f:
        lines = f.readlines()

    tst = day_07.Wiring()
    tst.load_instructions(lines)

    # overwrite B with the value of a
    tst.assign_literal(target_wire='b', value=tst.solve_for_x("a"))
    for key, val in tst.wires.items():
        if key != 'b':
            val["value"] = -1

    assert tst.solve_for_x("a") == 14710


if __name__ == "__main__":
    pytest.main()
