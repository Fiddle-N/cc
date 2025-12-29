from cc.compression.freq_tree import Node, LeafNode, InternalNode


class PrefCodeTableCreator:
    def __init__(self):
        self._tbl: dict[str, str] = {}

    def _traverse(
        self,
        node: Node,
        bitstr: str = "",
    ):
        match node:
            case LeafNode():
                self._tbl[node.element] = bitstr
                return
            case InternalNode():
                self._traverse(node.left, bitstr + "0")
                self._traverse(node.right, bitstr + "1")

    def create(self, node: Node) -> dict[str, str]:
        if isinstance(node, LeafNode):
            # single element tree
            return {node.element: "0"}
        self._traverse(node)
        return self._tbl


def create_pref_code_tbl(freq_tree: Node) -> dict[str, str]:
    pctc = PrefCodeTableCreator()
    return pctc.create(freq_tree)
