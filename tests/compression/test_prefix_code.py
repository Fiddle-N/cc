from cc.compression.freq_tree import InternalNode, LeafNode
from cc.compression.prefix_code import create_pref_code_tbl


def test_create_pref_code_tbl():
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
    pref_code_tbl = create_pref_code_tbl(freq_tree)
    assert pref_code_tbl == {
        "E": "0",
        "U": "100",
        "L": "101",
        "D": "110",
        "C": "1110",
        "Z": "111100",
        "K": "111101",
        "M": "11111",
    }


def test_create_pref_code_tbl_single_element():
    freq_tree = LeafNode(120, "E")
    pref_code_tbl = create_pref_code_tbl(freq_tree)
    assert pref_code_tbl == {
        "E": "0",
    }
