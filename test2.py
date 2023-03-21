import time 
from models import *

array = gen_data(10000, shuffle=0)
n = 100

tree = BSTtree(array)
now = time.time()

for i in range(n):
    tree.search_max()

print((time.time()-now)/n)


