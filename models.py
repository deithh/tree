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

    def update(self) -> int:
        self.factor = (self.left.h if self.left else - 1) - (self.right.h if self.right else - 1)
        self.h = max(self.left.h if self.left else -1, self.right.h if self.right else -1) + 1
        return self.factor


class Tree:
    def __init__(self, node_type: Type[ND] = Node):
        self.root: Optional[ND] = None
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
        if not len(array):
            return
        self._bin_halv(sorted(array), 0, len(array) - 1)
        self.h = int(math.log2(len(array))) + 1

    def build_tree(self, array: list) -> None:
        for key in array:
            self.insert(key)

    # ______________________________ROTATIONS

    def _rr(self, key: int | ND) -> None:
        if type(key) == int:
            if (node := self.search_node(key)) is None:
                return
        else:
            node = key
        new_mom = node.right
        prev_mom = node

        if prev_mom is self.root:
            self.root = new_mom

        if gparent := prev_mom.parent:
            if gparent.left == prev_mom:
                gparent.left = new_mom
            else:
                gparent.right = new_mom

        new_mom.parent = gparent
        prev_mom.right = new_mom.left
        new_mom.left = prev_mom
        prev_mom.parent = new_mom

        if prev_mom.right:
            prev_mom.right.parent = prev_mom

    def _ll(self, key: int | ND) -> None:
        if type(key) == int:
            if (node := self.search_node(key)) is None:
                return
        else:
            node = key
        new_mom = node.left
        prev_mom = node

        if prev_mom is self.root:
            self.root = new_mom

        if gparent := prev_mom.parent:
            if gparent.left == prev_mom:
                gparent.left = new_mom
            else:
                gparent.right = new_mom

        new_mom.parent = gparent
        prev_mom.left = new_mom.right
        new_mom.right = prev_mom
        prev_mom.parent = new_mom

        if prev_mom.left:
            prev_mom.left.parent = prev_mom

    def straighten(self) -> int:
        h = 0
        if (node := self.root) is None:
            return h
        while node:
            if node.left:
                self._ll(node)
                node = node.parent
            else:
                node = node.right
                h += 1
        return h

    def dsw(self) -> None:
        n = self.straighten()  # nodes count
        lim = n - self._expected(n)
        self.compress(lim)
        n-=lim
        while (n := n//2) >= 1:
            self.compress(n)

    def compress(self, times: int) -> None:
        node = self.root
        for i in range(times):
            self._rr(node)
            node = node.parent
            node = node.right
            if node is None: break
            if node.right is None: break

    @staticmethod
    def _expected(count: int) -> int:
        h = math.ceil(math.log2(count))
        return 2**(h-1) - 1
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
        if self.root is not None:
            self._traversal_pre_order_i(self.root)
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
        if self.root is None:
            return None, None
        node, path = self.root, [self.root.key]

        while node.left is not None:
            node = node.left
            path.append(node.key)

        return node.key, path

    def search_node(self, key: int) -> Optional[ND]:
        node = self.root

        while node:
            if key == node.key:
                return node
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

    # ______________________NODE MANIPULATION
    def _del_node(self, node: ND) -> None:
        if node is self.root:
            self.root = None
        node.del_node()

    def delete(self, key: int | ND) -> bool:
        node = key
        if type(key) == int:
            if (node := self.search_node(key)) is None:
                return False
        parent = node.parent

        if node.left is None and node.right is None:
            node.del_node()

        elif node.left is not None and node.right is not None:
            _next = self.search_succ(node)
            node.key = _next.key
            self.delete(_next)

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
            if key == node.key:
                return
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

    def __str__(self):
        return "AVL"

    # like baseclass but adds balance factor to labels dict(self.nodes)
    def _list_nodes(self, node: AVLnode) -> None:
        self.nodes[node.key] = f"{node.key} | {node.factor}"
        if node.left is not None:
            self.edges.append((node.key, node.left.key))
            self._list_nodes(node.left)
        if node.right is not None:
            self.edges.append((node.key, node.right.key))
            self._list_nodes(node.right)

    def _back_prop(self, node: Optional[AVLnode] = None) -> None:  # post order initial propagation of balance factor
        if node is None:
            node = self.root

        if node.left is not None:
            self._back_prop(node.left)

        if node.right is not None:
            self._back_prop(node.right)

        node.update()

    def back_prop(self):
        node = self.root
        if node is None:
            return
        self._back_prop(node)

    def delete(self, key: int | ND) -> bool:
        node = key
        if type(key) == int:
            if (node := self.search_node(key)) is None:
                return False
        parent = node.parent

        if node.left is None and node.right is None:
            node.del_node()

        elif node.left is not None and node.right is not None:
            _next = self.search_succ(node)
            node.key = _next.key
            self.delete(_next)

        else:
            if node.left is None:
                _next = node.right
            else:
                _next = node.left
            node.left = _next.left
            node.right = _next.right
            node.key = _next.key

        if parent and parent.left:
            parent.left.update()
        if parent and parent.right:
            parent.right.update()

        while parent:
            if (factor := parent.update()) in [1, -1]:
                return True
            elif factor in [-2, 2]:
                self.rotate(parent)
                pass
            parent = parent.parent
        return True

    def rotate(self, node: ND):
        l, r = node.left.factor if node.left else - 1, node.right.factor if node.right else - 1
        if node.left:
            if node.factor == 2 and l == 1:
                self._ll(node)
            elif node.factor == 2 and l == -1:
                self._lr(node)

        elif node.right:
            if node.factor == -2 and r == -1:
                self._rr(node)
            elif node.factor == -2 and r == 1:
                self._rl(node)

    def _rr(self, key: int | ND) -> None:
        if type(key) == int:
            if (node := self.search_node(key)) is None:
                return
        else:
            node = key
        new_mom = node.right
        prev_mom = node

        if prev_mom is self.root:
            self.root = new_mom

        if gparent := prev_mom.parent:
            if gparent.left == prev_mom:
                gparent.left = new_mom
            else:
                gparent.right = new_mom

        new_mom.parent = gparent
        prev_mom.right = new_mom.left
        new_mom.left = prev_mom
        prev_mom.parent = new_mom

        if prev_mom.right:
            prev_mom.right.parent = prev_mom

        prev_mom.update()
        new_mom.update()

    def _ll(self, key: int | ND) -> None:
        if type(key) == int:
            if (node := self.search_node(key)) is None:
                return
        else:
            node = key
        new_mom = node.left
        prev_mom = node

        if prev_mom is self.root:
            self.root = new_mom

        if gparent := prev_mom.parent:
            if gparent.left == prev_mom:
                gparent.left = new_mom
            else:
                gparent.right = new_mom

        new_mom.parent = gparent
        prev_mom.left = new_mom.right
        new_mom.right = prev_mom
        prev_mom.parent = new_mom

        if prev_mom.left:
            prev_mom.left.parent = prev_mom
        prev_mom.update()
        new_mom.update()

    def _rl(self, key: int | ND) -> None:
        node = key
        if type(key) == int:
            node = self.search_node(key)
        self._ll(node.right)
        self._rr(node)

    def _lr(self, key: int | ND) -> None:
        node = key
        if type(key) == int:
            node = self.search_node(key)
        self._rr(node.left)
        self._ll(node)

    def dsw(self):
        super().dsw()
        self.back_prop()


class BSTtree(Tree):
    def __init__(self, array: list):
        super().__init__(Node)
        self.build_tree(array)

    def __str__(self):
        return "BST"


ND: TypeAlias = Union[Node, AVLnode]
TR: TypeAlias = Union[BSTtree, AVLtree]
