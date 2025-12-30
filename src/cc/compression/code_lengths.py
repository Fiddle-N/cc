from cc.compression.freq_tree import Node, LeafNode, InternalNode


class CodeLengthCreator:
    def __init__(self):
        self._lengths: dict[int, int] = {}

    def _traverse(
        self,
        node: Node,
        depth: int = 0,
    ):
        match node:
            case LeafNode():
                self._lengths[node.element] = depth
                return
            case InternalNode():
                self._traverse(node.left, depth + 1)
                self._traverse(node.right, depth + 1)

    def create(self, node: Node) -> dict[int, int]:
        if isinstance(node, LeafNode):
            # single element tree
            return {node.element: 1}
        self._traverse(node)
        return self._lengths


def create_code_lengths(freq_tree: Node) -> dict[int, int]:
    ctc = CodeLengthCreator()
    return ctc.create(freq_tree)
