from models import *
import os
import sys

tree: Optional[TR] = None


def clear() -> None:
    os.system('cls')


# At end of line [possible commands]: indicates waiting for user action
def parser(command: str) -> None:
    command = command.split(',')
    command = [i.lower() for i in command]
    command = [int(i) if i.isdigit() else i.replace(" ", "").replace("-", '') for i in command]

    for instruction in command:
        if instruction in ["findmax", 'searchmax', 'max']:

            max_val, path = tree.search_max()
            if max_val:
                path = " -> ".join(map(str, path))
            input(f"Max value is {max_val}\npath: {path} [any]: ")

        elif instruction in ["findmin", 'searchmin', "min"]:

            min_val, path = tree.search_min()
            if min_val:
                path = " -> ".join(map(str, path))
            input(f"Min value is {min_val}\npath: {path} [any]: ")

        elif instruction in ['inorder']:
            in_order = " ".join(map(str, tree.traversal_in_order()))
            input(f"Tree in-order: {in_order} [any]: ")

        elif instruction in ['preorder']:
            pre_order = " ".join(map(str, tree.traversal_pre_order()))
            input(f"Tree pre-order: {pre_order} [any]: ")

        elif instruction in ['del', 'delete', 'remove']:
            args = command[1:]
            try:
                for key in map(int, args):
                    state = tree.delete(key)
                    if state:
                        input(f"Node {key} deleted [any]: ")
                    else:
                        input(f'Node {key} not found[any]: ')
            except:
                input("Error [any]:")
            break

        elif instruction in ['heigth', "height"]:
            print("[WARN] tree height is not updated after node deletion")
            input(f"Tree height = {tree.height} [any]:")

        elif instruction in ['deltree', 'deletetree', 'removetree', 'free']:
            tree.free()
            input(f"Tree is empty now [any]: ")

        elif instruction in ['balance', 'dsw']:
            tree.dsw()
            input(f"Tree is balanced now [any]: ")

        elif instruction in ['h', 'help']:
            print("min - find min node in tree and print path")
            print("max - find max node in tree and print path")
            print("free - delete entire tree (post order)")
            print("del, node1[, node2...] - delete node specified as args")
            print("preorder - print tree pre order traversal")
            print("in order - print tree in order traversal")
            print("height - print initial tree height")
            print("dsw - tree balance")
            print('instructions can be chained [,] in except of del')
            input("[any]: ")
        else:
            input("Command invalid [any]: ")


def main() -> None:
    global tree
    sys.setrecursionlimit(10000)
    menu: str = 'default'
    tree_type: str = ''
    array: list = []

    while True:

        if menu == "default":
            clear()
            input("Binary Tree commander [any]: ")
            menu = 'choose tree'

        elif menu == "choose tree":
            fail = False
            while 1:
                clear()
                if fail:
                    print('I don\'t understand. use [avl/bst/exit]')
                temp = input("Choose tree type [avl/bst/exit]: ").lower()
                if temp in ['avl', 'bst', 'exit']:
                    break
                fail = True

            if temp == 'exit':
                break
            if temp == 'avl':
                tree_type = 'avl'
            else:
                tree_type = 'bst'
            menu = 'choose data'

        elif menu == "choose data":
            fail = False
            while 1:
                clear()
                if fail:
                    print('I don\'t understand. use [enter/gen/exit]')
                temp = input("Enter data or generate [enter/gen/exit]: ").lower()
                if temp in ['gen', 'enter', 'exit']:
                    break
                fail = True
            if temp == 'exit':
                break

            menu = temp

        elif menu == 'gen':
            fail = False
            while 1:
                clear()
                if fail:
                    print('I don\'t understand. use [n: int > 0]')
                temp = input("Enter number of nodes [n: int > 0/exit]: ").lower()
                if temp == 'exit' or (temp.isdigit() and int(temp) > 0):
                    break
                fail = True
            if temp == 'exit':
                break
            n = int(temp)
            fail = False
            while 1:
                clear()
                if fail:
                    print('I don\'t understand. use [y/n]')
                temp = input("shuffle? [y/n]: ").lower()
                if temp == 'y':
                    if tree_type == 'avl':
                        input("[WARN] AVL constructor will sort it anyway [any]: ")
                    array = gen_data(n, shuffle=True)
                    break
                if temp == 'n':
                    array = gen_data(n)
                    break
                fail = True

            menu = 'start'

        elif menu == 'enter':
            fail = False
            while 1:
                clear()
                if fail:
                    print('List contains no-integer values or empty list')
                temp = input('Enter list of integers [int, int, .../exit]: ').split()
                if temp == 'exit' or (all([x.lstrip('-').isdigit() for x in temp]) and len(temp)):
                    break
                fail = True
            if temp == 'exit':
                break
            array = list(map(int, temp))
            menu = 'check_input'

        elif menu == 'check_input':

            new = array.copy()

            # check for repetitions
            flag = 1
            if len(array) != len(set(array)):
                fail = False
                while 1:
                    clear()
                    if fail:
                        print('I don\'t understand. use [y/n]')
                    temp = input(
                        "Repetitions in array are not allowed. Continue without them?\
                        \n[WARN] This will affect order of elements [y/n]: ").lower()
                    if temp in ['y', 'n']:
                        break
                    fail = True
                if temp == 'y':
                    new = list(set(new))
                else:
                    menu = 'choose data'
                    array = []
                    flag = 0

            # check if array is sorted
            if new != sorted(new):
                fail = False
                while 1:
                    clear()
                    if fail:
                        print('I don\'t understand. use [y/n]')
                    temp = input("Array not sorted. sort? [y/n]: ").lower()
                    if temp in ['y', 'n']:
                        break
                    fail = True
                if temp == 'y':
                    new.sort()
                else:
                    clear()
                    if tree_type == 'avl':
                        input("[WARN] AVL constructor will sort it anyway [any]: ")

            if flag:
                clear()
                if new != array:
                    input(f"Array changed: {array} -> {new} [any]: ")
                    array = new
                else:
                    input(f"Array accepted: {array} [any]: ")
                menu = 'start'

        elif menu == 'start':
            clear()
            if tree_type == 'bst':
                tree = BSTtree(array)
            else:
                tree = AVLtree(array)
            if len(array) < 20:
                input(f'Proceed to construct {tree_type} tree with array: {array} [any]: ')
            else:
                input(
                    f'Proceed to construct {tree_type} tree with array: [{", ".join(map(str, array[:5]))}'
                    f' ...{len(array) - 10} more... {", ".join(map(str, array[-5:]))}] [any]: ')

            menu = 'choose func'

        elif menu == "choose func":
            clear()
            print(f'Active tree type: {tree_type}')

            command = input("Enter command (h for help) [valid command/h/exit]: ")
            if command == 'exit':
                break
            parser(command)
    clear()


main()
