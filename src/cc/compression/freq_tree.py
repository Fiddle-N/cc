import heapq
from dataclasses import dataclass, field
from typing import Protocol


class Node(Protocol):
    weight: int


@dataclass(frozen=True)
class LeafNode(Node):
    weight: int
    element: int


@dataclass(frozen=True)
class InternalNode(Node):
    weight: int = field(init=False)
    left: Node
    right: Node

    def __post_init__(self):
        object.__setattr__(self, "weight", self.left.weight + self.right.weight)


@dataclass(frozen=True, eq=True, order=True)
class NodeItem:
    node: Node = field(compare=False)
    weight: int


def create_freq_tree(freqs: dict[int, int]) -> Node:
    if not freqs:
        raise ValueError("Frequency tree must be populated")

    q = []
    for char, freq in freqs.items():
        heapq.heappush(q, NodeItem(LeafNode(weight=freq, element=char), freq))

    while len(q) != 1:
        left = heapq.heappop(q)
        right = heapq.heappop(q)
        node = InternalNode(left.node, right.node)
        node_item = NodeItem(node, node.weight)
        heapq.heappush(q, node_item)

    return q[0].node
