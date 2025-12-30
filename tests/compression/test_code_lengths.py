from cc.compression.freq_tree import InternalNode, LeafNode
from cc.compression.code_lengths import create_code_lengths


def test_create_code_lengths():
    freq_tree = InternalNode(
        LeafNode(120, 69),
        InternalNode(
            InternalNode(
                LeafNode(37, 85),
                LeafNode(42, 68),
            ),
            InternalNode(
                LeafNode(42, 76),
                InternalNode(
                    LeafNode(32, 67),
                    InternalNode(
                        InternalNode(LeafNode(2, 90), LeafNode(7, 75)),
                        LeafNode(24, 77),
                    ),
                ),
            ),
        ),
    )
    code_lengths = create_code_lengths(freq_tree)
    assert code_lengths == {
        69: 1,
        85: 3,
        68: 3,
        76: 3,
        67: 4,
        77: 5,
        75: 6,
        90: 6,
    }


def test_create_code_lengths_single_element():
    freq_tree = LeafNode(120, 69)
    code_lengths = create_code_lengths(freq_tree)
    assert code_lengths == {
        69: 1,
    }
