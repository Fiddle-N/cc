import pytest

from cc.compression.freq_tree import create_freq_tree, InternalNode, LeafNode


def test_create_freq_tree():
    freqs = {
        "C": 32,
        "D": 42,
        "E": 120,
        "K": 7,
        "L": 42,
        "M": 24,
        "U": 37,
        "Z": 2,
    }
    freq_tree = create_freq_tree(freqs)
    assert freq_tree == InternalNode(
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


def test_create_freq_tree_single_element():
    freqs = {"C": 32}
    freq_tree = create_freq_tree(freqs)
    assert freq_tree == LeafNode(32, "C")


def test_create_freq_tree_no_elements():
    with pytest.raises(ValueError):
        create_freq_tree({})
