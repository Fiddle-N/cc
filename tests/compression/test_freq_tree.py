import pytest

from cc.compression.freq_tree import create_freq_tree, InternalNode, LeafNode


def test_create_freq_tree():
    freqs = {
        67: 32,
        68: 42,
        69: 120,
        75: 7,
        76: 42,
        77: 24,
        85: 37,
        90: 2,
    }
    freq_tree = create_freq_tree(freqs)
    assert freq_tree == InternalNode(
        LeafNode(120, 69),
        InternalNode(
            InternalNode(
                LeafNode(37, 85),
                LeafNode(42, 76),
            ),
            InternalNode(
                LeafNode(42, 68),
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


def test_create_freq_tree_single_element():
    freqs = {67: 32}
    freq_tree = create_freq_tree(freqs)
    assert freq_tree == LeafNode(32, 67)


def test_create_freq_tree_no_elements():
    with pytest.raises(ValueError):
        create_freq_tree({})
