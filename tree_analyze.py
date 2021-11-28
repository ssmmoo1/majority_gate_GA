import pickle
from Node import Gate
from Tree import Tree
file = "2bit_adder_11_4.pkl"
#file = "xor.pkl"


tree = None
with open(file, "rb") as f:
    tree = pickle.load(f)

#tree.prune_tree()
print(f"Gate Count: {tree.get_num_gates()}")
print(f"Critical Path: {tree.get_crit_path()}")
tree.visualize_tree()