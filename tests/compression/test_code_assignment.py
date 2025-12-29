from cc.compression.code_assignment import assign


def test_assign():
    code_lengths = {
        "E": 1,
        "C": 4,
        "M": 5,
        "K": 6,
        "L": 3,
        "Z": 6,
        "D": 3,
        "U": 3,
    }
    assert assign(code_lengths) == {
        "E": "0",
        "D": "100",
        "L": "101",
        "U": "110",
        "C": "1110",
        "M": "11110",
        "K": "111110",
        "Z": "111111",
    }
