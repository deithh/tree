from __future__ import annotations
import numpy as np
import math
from typing import Type, Tuple, Optional, Union, TypeAlias


def gen_data(n: int, shuffle: bool = False) -> list:
    array = list(range(1, n + 1, 1))
    if shuffle:
        np.random.shuffle(array)
    return array


class Node:
    key = None

    def __init__(self, key: int, parent: Optional[ND] = None) -> None:
        self.key = key
        self.parent = parent
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def del_node(self) -> None:
        if self.parent is not None:
            if self.key < self.parent.key:
                self.parent.left = None
            else:
                self.parent.right = None
        if self.right is not None:
            self.right.parent = None
        if self.left is not None:
            self.left.parent = None


class AVLnode(Node):
    def __init__(self, key: int, parent: Optional[AVLnode] = None):
        super().__init__(key, parent)
        self.left: Optional[AVLnode] = None
        self.right: Optional[AVLnode] = None
        self.factor: int = 0
        self.h: int = 0


class Tree:
    def __init__(self, node_type: Type[ND] = Node):
        self.root: Optional[Node] = None
        self.h: int = -1
        self.node_type = node_type
        self._pre_order: list = []
        self._in_order: list = []
        self.edges: list = []
        self.nodes: dict = {}

    # __________________________________________TREE CONSTRUCTION

    @staticmethod
    def mid(begin: int, end: int) -> int:
        return (end - begin + 1) // 2 + begin

    def _bin_halv(self, array: list, begin: int, end: int, node: ND = None) -> None:
        if end < begin:
            return

        if node is None:
            pivot = Tree.mid(begin, end)
            self.root = self.node_type(array[pivot + begin])
            node = self.root

        else:
            pivot = Tree.mid(begin, end)
            if array[pivot] < node.key:
                node.left = self.node_type(array[pivot], node)
                node = node.left
            else:
                node.right = self.node_type(array[pivot], node)
                node = node.right

        self._bin_halv(array, begin, pivot - 1, node)
        self._bin_halv(array, pivot + 1, end, node)

    def bin_halv(self, array: list) -> None:
        self._bin_halv(sorted(array), 0, len(array) - 1)
        self.h = int(math.log2(len(array))) + 1

    def build_tree(self, array: list) -> None:
        for key in array:
            self.insert(key)

    # ______________________________ROTATIONS

    def _rr(self, node):

        gparent = node.parent
        new_mom = node.right
        new_left = node

        if gparent.left == node:
            gparent.left = new_mom
        else:
            gparent.right = new_mom

        new_mom.parent = gparent
        new_mom.left = new_left
        new_left.parent = new_mom
        new_left.right = None

    def _rl(self, node):
        pass

    def _ll(Self, node):
        gparent = node.parent
        new_mom = node.left
        new_right = node

        if gparent.left == node:
            gparent.left = new_mom
        else:
            gparent.right = new_mom

        new_mom.parent = gparent
        new_mom.right = new_right
        new_right.parent = new_mom
        new_right.left = None

    def _lr(self, node):
        pass

    # ____________________________________________GRAPH DATA
    # pre order traversal save edges in inner list
    def _list_nodes(self, node: ND) -> None:
        self.nodes[node.key] = f"{node.key}"
        if node.left is not None:
            self.edges.append((node.key, node.left.key))
            self._list_nodes(node.left)
        if node.right is not None:
            self.edges.append((node.key, node.right.key))
            self._list_nodes(node.right)

    def list_nodes(self) -> Tuple[list, dict]:
        if self.root is not None:
            self._list_nodes(self.root)
        return self.edges, self.nodes

    # _________________________________________TRAVERSALS

    def _traversal_pre_order(self, node: ND) -> None:
        self._pre_order.append(node.key)
        if node.left is not None:
            self._traversal_pre_order(node.left)
        if node.right is not None:
            self._traversal_pre_order(node.right)

    def _traversal_pre_order_i(self, node: ND) -> None:
        stack = []
        while True:
            if node is not None:
                stack.append(node)
                self._pre_order.append(node.key)
                node = node.left
            elif stack:
                node = stack.pop()
                node = node.right
            else:
                break

    def traversal_pre_order(self) -> list:
        if self.root is not None: self._traversal_pre_order_i(self.root)
        path = self._pre_order.copy()
        self.collect_garbage()
        return path

    def _traversal_in_order(self, node: ND) -> None:
        if node.left is not None:
            self._traversal_in_order(node.left)
        self._in_order.append(node.key)
        if node.right is not None:
            self._traversal_in_order(node.right)

    def _traversal_in_order_i(self, node: ND) -> None:
        stack = []
        while True:
            if node is not None:
                stack.append(node)
                node = node.left
            elif stack:
                node = stack.pop()
                self._in_order.append(node.key)
                node = node.right
            else:
                break

    def traversal_in_order(self) -> list:
        if self.root is not None:
            self._traversal_in_order_i(self.root)
        path = self._in_order.copy()
        self.collect_garbage()
        return path

    # ____________________________________TREE DELETION
    # delete tree node by node in post order
    def _free(self, node: ND) -> None:
        if node.left is not None:
            self._free(node.left)
        if node.right is not None:
            self._free(node.right)
        node.del_node()
        del node

    def free(self) -> None:
        if self.root is not None:
            self._free(self.root)
        self.root = None
        self.collect_garbage()
        self.h = -1

    # free arrays holding in and preorder paths
    def collect_garbage(self) -> None:
        self._in_order = []
        self._pre_order = []

    # _________________________________TREE SEARCHING
    def search_max(self) -> Tuple[Optional[int], Optional[list]]:
        if self.root is None:
            return None, None
        node, path = self.root, [self.root.key]

        while node.right is not None:
            node = node.right
            path.append(node.key)

        return node.key, path

    def search_min(self) -> Tuple[Optional[int], Optional[list]]:
        if self.root is None: return None, None
        node, path = self.root, [self.root.key]

        while node.left is not None:
            node = node.left
            path.append(node.key)

        return node.key, path

    def search_node(self, key: int) -> Optional[ND]:
        node = self.root

        while node:
            if key == node.key: return node
            if key > node.key:
                node = node.right
            else:
                node = node.left

        return None

    # dumb but enough
    @staticmethod
    def search_succ(node: ND) -> Optional[ND]:

        if node.right:
            current = node.right
            while current.left:
                current = current.left
            return current

    # ______________________NODE MANIPILATION
    def _del_node(self, node: ND) -> None:
        if node is self.root:
            self.root = None
        node.del_node()

    def delete(self, key: int) -> bool:
        if (node := self.search_node(key)) is None:
            return False
        if node.left is None and node.right is None:
            node.del_node()
        elif node.left is not None and node.right is not None:
            _next = self.search_succ(node)
            self.delete(_next.key)
            node.key = _next.key

        else:
            if node.left is None:
                _next = node.right
            else:
                _next = node.left
            node.left = _next.left
            node.right = _next.right
            node.key = _next.key
        return True

    def insert(self, key: int) -> None:
        if self.root is None:
            self.root = self.node_type(key)
            self.h = 0
            return
        parent = None
        node = self.root
        h = 0
        while node is not None:
            h += 1
            if key < node.key:
                node, parent = node.left, node
            else:
                node, parent = node.right, node
        if self.h < h:
            self.h = h
        if key < parent.key:
            parent.left = self.node_type(key, parent)
            return
        parent.right = self.node_type(key, parent)

    # ____________PROPERTIES
    @property
    def height(self) -> int:
        return self.h


class AVLtree(Tree):
    def __init__(self, array: list):
        super().__init__(AVLnode)
        self.bin_halv(array)
        self.back_prop()

    # like baseclass but adds balance factor to labels dict(self.nodes)
    def _list_nodes(self, node: AVLnode) -> None:
        self.nodes[node.key] = f"{node.key} | {node.factor}"
        if node.left is not None:
            self.edges.append((node.key, node.left.key))
            self._list_nodes(node.left)
        if node.right is not None:
            self.edges.append((node.key, node.right.key))
            self._list_nodes(node.right)

    def back_prop(self, node: Optional[AVLnode] = None) -> None:  # post order initial propagation of balance factor
        if node is None:
            node = self.root

        l, r = -1, -1

        if node.left is not None:
            self.back_prop(node.left)
            l = node.left.h

        if node.right is not None:
            self.back_prop(node.right)
            r = node.right.h

        node.h = max(l, r) + 1
        node.factor = l - r

    def delete(self, key: int) -> bool:
        if (node := self.search_node(key)) is None: return False
        if node.left is None and node.right is None:
            node.del_node()
        elif node.left is not None and node.right is not None:
            _next = self.search_succ(node)
            self.delete(_next.key)
            node.key = _next.key

        else:
            if node.left is None:
                _next = node.right
            else:
                _next = node.left
            node.left = _next.left
            node.right = _next.right
            node.key = _next.key
        self.back_prop()
        return True


class BSTtree(Tree):
    def __init__(self, array: list):
        super().__init__(Node)
        self.build_tree(array)

    def straighten(self) -> None:
        pass

    def dsw(self) -> None:
        self.straighten()


ND: TypeAlias = Union[Node, AVLnode]
TR: TypeAlias = Union[BSTtree, AVLtree]
