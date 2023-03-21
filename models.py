import numpy as np
import sys 

sys.setrecursionlimit(100000)

def gen_data(n, shuffle = False):
    array =list(range(1, n+1, 1))
    if shuffle: np.random.shuffle(array)
    return array

class Node:
    def __init__(self, value, parent = None):
        
        self.value = value
        self.parent = parent
        # Left child
        self.left = None
        # right child
        self.right = None

    def del_node(self):
        if self.parent is not None:
            if self.value < self.parent.value:
                self.parent.left = None
            else:
                self.parent.right = None
        return self.left, self.right
        

class AVLnode(Node):
    def __init__(self, value, parent = None):
        super().__init__(value, parent)        
        self.factor = 0
        self.h = 0



class Tree:
    def __init__(self):
        self.root = None
        self.h = -1
        self._pre_order = []
        self._in_order = []
        self.edges = []
        self.nodes = {}

    def _RR(self, node):

        gparent = node.parent 
        new_mom = node.right
        new_left = node

        if gparent.left == node: gparent.left = new_mom
        else: gparent.right = new_mom

            
        new_mom.parent = gparent
        new_mom.left = new_left
        new_left.parent = new_mom
        new_left.right = None

    def _RL(self, node):
        pass
    def _LL(Self, node):
        gparent = node.parent 
        new_mom = node.left
        new_right = node

        if gparent.left == node: gparent.left = new_mom
        else: gparent.right = new_mom

            
        new_mom.parent = gparent
        new_mom.right = new_right
        new_right.parent = new_mom
        new_right.left = None

        
    def _LR(self, node):
        pass
    #pre order travelsal save edges in inner list
    def _list_nodes(self, node = None):
        self.nodes[node.value] = f"{node.value}"
        if node.left != None:
            self.edges.append((node.value, node.left.value))
            self._list_nodes(node.left)
        if node.right != None:
            self.edges.append((node.value, node.right.value))
            self._list_nodes(node.right)

    def list_nodes(self, node = None):
        if node == None: node = self.root
        self._list_nodes(node)

    def height(self):
        return self.h

    def dsw(self):
        pass

    def _search(self, node, key):
        if node.value == key: return node

        if key < node.value:
            if node.left is None:
                return
            self._search(node.left, key)
        else:
            if node.right is None:
                return
            self._search(node.right, key)

    def search(self, key):
        if (node:= self._search(self.root, key)) != None:
            return Node
        raise "not found"

    def _traversal_pre_order(self, node = None):
        if node == None: node = self.root

        self._pre_order.append(node.value)
        if node.left != None: self._traversal_pre_order(node.left)
        if node.right != None: self._traversal_pre_order(node.right)

    def traversal_pre_order(self):
        self.collect_garbage()
        if self.root is not None: self._traversal_pre_order()
        return self._pre_order

    def _traversal_in_order(self, node = None):
        if node == None: node = self.root

        if node.left != None: self._traversal_in_order(node.left)
        self._in_order.append(node.value)
        if node.right != None: self._traversal_in_order(node.right)

    def traversal_in_order(self):
        self.collect_garbage()
        if self.root is not None: self._traversal_in_order()
        return self._in_order

    #delete tree node by node in post order
    def _free(self, node = None):
        if node == None: node = self.root

        if node.left != None: self._free(node.left)
        if node.right != None: self._free(node.right)
        node.del_node()
        del node

    def free(self):
        if self.root is not None: self._free()
        self.root = None
        self.collect_garbage()
        self.h = -1

    #free arrays holding in and pre order paths
    def collect_garbage(self):
        self._in_order = []
        self._pre_order = []

    def search_min(self, node = None, path = None):
        if self.root is None: return None, None
        if node == None: node, path = self.root, [self.root.value]

        while node.left != None:
            node = node.left
            path.append(node.value)
        
        return node.value, path  #minimal value and path

    def search_max(self, node = None, path = None):
        if self.root is None: return None, None
        if node == None: node, path = self.root, [self.root.value]

        while node.right != None:
            node = node.right
            path.append(node.value)
        
        return node.value, path #maximal calue and path
    
    def delete(self, key):
        pass

class AVLtree(Tree):
    def __init__(self, array):
        super().__init__()
        self.bin_halv(array, 0, len(array)-1)
        self.back_prop()


    #like baseclass but adds balance factor to labels dict(self.nodes)    
    def _list_nodes(self, node):
        self.nodes[node.value] = f"{node.value} | {node.factor}"
        if node.left != None:
            self.edges.append((node.value, node.left.value))
            self._list_nodes(node.left)
        if node.right != None:
            self.edges.append((node.value, node.right.value))
            self._list_nodes(node.right)

    def mid(self, array, begin, end):
        return (end - begin + 1)//2 + begin

    def bin_halv(self, array, begin, end, node = None):
        if end<begin: return
        if node == None:
            pivot = self.mid(array, begin, end)
            self.root = AVLnode(array[pivot+begin])
            node = self.root

        else:
            pivot = self.mid(array,begin, end)
            if array[pivot] < node.value:
                node.left = AVLnode(array[pivot], node)
                node = node.left
            else:
                node.right = AVLnode(array[pivot], node)
                node = node.right

        self.bin_halv(array, begin, pivot - 1, node)
        self.bin_halv(array, pivot +1, end, node)
 
    def back_prop(self, node = None):
        if node == None: node = self.root

        l, r = -1, -1

        if node.left != None:
            self.back_prop(node.left)
            l = node.left.h

        if node.right != None:
            self.back_prop(node.right)
            r = node.right.h

        node.h = max(l, r)+1
        node.factor = l-r        

    def delete(self, key):
        super().delete(key)
        pass

class BSTtree(Tree):
    def __init__(self, array):
        super().__init__()
        self.build_tree(array)

    def build_tree(self, array):
        for key in array:
            self.insert(key)

    def insert(self, key):
        if self.root is None: 
            self.root = Node(key)
            self.h = 0
            return
        parent = None
        node = self.root
        h = 0
        while node is not None:
            h+=1
            if key<node.value:
                node, parent = node.left, node
            else:
                node, parent = node.right, node
        if self.h<h: self.h = h
        if key<parent.value:
            parent.left = Node(key, parent)
            return
        parent.right = Node(key, parent)





    
