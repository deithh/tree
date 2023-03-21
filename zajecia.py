from models import *
import numpy as np
import os

def clear(): os.system('cls')

menu = 'default'
tree = None
tree_type = None
array = []



# At end of line [possible commands]: indicates waiting for user action



def parser(command):
    global tree
    command = command.split(',')
    command = [i.lower() for i in command]
    command = [int(i) if i.isdigit() else i.replace(" ", "").replace("-", '') for i in command]

    match command:
        case ["findmax" | 'searchmax' | 'max']:

            max_val , path = tree.search_max()
            if max_val: path = " -> ".join(map(str,path))
            input(f"Max value is {max_val}\npath: {(path)} [any]: ")

        case ["findmin" | 'searchmin' | "min"]:

            min_val , path = tree.search_min()
            if min_val: path = " -> ".join(map(str,path))
            input(f"Min value is {min_val}\npath: {path} [any]: ")

        case ['inorder']:
            in_order =  " ".join(map(str,tree.traversal_in_order()))
            input(f"Tree in-order: {in_order} [any]: ")

        case['preorder']:
            pre_order = " ".join(map(str,tree.traversal_pre_order()))
            input(f"Tree pre-order: {pre_order} [any]: ")


        case ['del' | 'delete' | 'remove', *args]:
            pass

        case ['h' | "height"]:
            print("[WARN] tree height is not updated after node deletion")
            input(f"Tree height = {tree.height()} [any]:")
            
        
        case ['deltree' | 'deletetree' | 'removetree' | 'free']:
            tree.free()
            input(f"Tree is empty now [any]: ")


        case _:
            input("Command invalid [any]: ")






while True:
    match menu:
        case "default":
            clear()
            input("Binary Tree commander [any]: ")
            menu = 'choose tree'
            
        case "choose tree":
            fail = False
            while 1:
                clear()
                if fail: print('I don\'t understand. use [avl/bst/exit]')
                temp = input("Choose tree type [avl/bst/exit]: ").lower()
                if temp in ['avl','bst', 'exit']:
                    break
                fail = True
                
            if temp =='exit': break
            if temp == 'avl': tree_type = 'avl'
            else: tree_type = 'bst'
            menu = 'choose data'

        case "choose data":
            fail = False
            while 1:
                clear()
                if fail: print('I don\'t understand. use [enter/gen/exit]')
                temp = input("Enter data or generate [enter/gen/exit]: ").lower()
                if temp in ['gen','enter', 'exit']:
                    break
                fail = True
            if temp =='exit': break

            menu = temp

        case 'gen':
            fail = False
            while 1:
                clear()
                if fail: print('I don\'t understand. use [n: int > 0]')
                temp = input("Enter number of nodes [n: int > 0/exit]: ").lower()
                if temp == 'exit' or (temp.isdigit() and int(temp) > 0):
                    break
                fail = True
            if temp =='exit': break
            n = int(temp)
            fail = False
            while 1:
                clear()
                if fail: print('I don\'t understand. use [y/n]')
                temp = input("shuffle? [y/n]: ").lower()
                if temp == 'y':
                    if tree_type == 'avl': input("[WARN] AVL constructor will sort it anyway [any]: ")
                    array = gen_data(n, shuffle=True)
                    break
                if temp == 'n':
                    array = gen_data(n)
                    break
                fail = True

            menu = 'start'

        case 'enter':
            fail = False
            while 1:
                clear()
                if fail: print('List contains no-integer values or empty list')
                temp = input('Enter list of integers [int, int, .../exit]: ').split()
                if temp =='exit' or (all([x.isdigit() for x in temp]) and len(temp)):
                    break
                fail = True
            if temp =='exit': break
            array = list(map(int,temp))
            menu = 'check_input'

        case 'check_input':

            new = array.copy()

            #check if array is sorted
            if array != sorted(array):
                fail = False
                while 1:
                    clear()
                    if fail:  print('I don\'t understand. use [y/n]')
                    temp = input("Array not sorted. sort? [y/n]: ").lower()
                    if temp in ['y','n']:
                        break
                    fail = True
                if temp == 'y': new.sort()
                else: 
                    clear()
                    if tree_type == 'avl': input("[WARN] AVL constructor will sort it anyway [any]: ")

            #check for repetitions
            flag = 1
            if len(array) != len(set(array)):
                fail = False
                while 1:
                    clear()
                    if fail: print('I don\'t understand. use [y/n]')
                    temp = input("Repetitions in array are not allowed. Continue without them? [y/n]: ").lower()
                    if temp in ['y','n']:
                        break
                    fail = True
                if temp == 'y': new = list(set(new))
                else: 
                    menu = 'choose data'
                    array = []
                    flag = 0

            if flag:
                clear()
                if new != array: input(f"Array changed: {array} ->  {new} [any]: ")
                else: input(f"Array accepted: {array} [any]: ")
                menu = 'start'

        case 'start':
            clear()
            if tree_type == 'bst': tree = BSTtree(array)
            else: tree = AVLtree(sorted(array)) 
            input(f'Proceed to construct {tree_type} tree with array: {array} [any]: ')
            menu = 'choose func'

        case "choose func":
            clear()
            print(f'Active tree type: {tree_type}')

            command = input("Enter command (h for help) [valid command/h/exit]: ")
            if command =='exit': break
            parser(command)


