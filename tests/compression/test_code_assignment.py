from cc.compression.code_assignment import assign


def test_assign():
    code_lengths = {
        69: 1,
        67: 4,
        77: 5,
        75: 6,
        68: 3,
        90: 6,
        76: 3,
        85: 3,
    }
    assert assign(code_lengths) == {
        69: (0, 1),
        68: (4, 3),
        76: (5, 3),
        85: (6, 3),
        67: (14, 4),
        77: (30, 5),
        75: (62, 6),
        90: (63, 6),
    }
