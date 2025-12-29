from cc.compression.freq_tree import InternalNode, LeafNode
from cc.compression.code_lengths import create_code_lengths


def test_create_code_lengths():
    freq_tree = InternalNode(
        LeafNode(120, "E"),
        InternalNode(
            InternalNode(
                LeafNode(37, "U"),
                LeafNode(42, "L"),
            ),
            InternalNode(
                LeafNode(42, "D"),
                InternalNode(
                    LeafNode(32, "C"),
                    InternalNode(
                        InternalNode(LeafNode(2, "Z"), LeafNode(7, "K")),
                        LeafNode(24, "M"),
                    ),
                ),
            ),
        ),
    )
    code_lengths = create_code_lengths(freq_tree)
    assert code_lengths == {
        "E": 1,
        "D": 3,
        "L": 3,
        "U": 3,
        "C": 4,
        "M": 5,
        "K": 6,
        "Z": 6,
    }


def test_create_code_lengths_single_element():
    freq_tree = LeafNode(120, "E")
    code_lengths = create_code_lengths(freq_tree)
    assert code_lengths == {
        "E": 1,
    }
