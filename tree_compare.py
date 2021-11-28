import pickle
from random import randint
from Tree import Tree

tree1 = None
tree2 = None

with open("2bit_adder.pkl", "rb") as f:
    tree1 = pickle.load(f)

with open("2bit_adder_v2.pkl", "rb") as f:
    tree2 = pickle.load(f)



for x in range(1000):

    in1 = bool(randint(0,1))
    in2 = bool(randint(0,1))
    in3 = bool(randint(0,1))
    in4 = bool(randint(0,1))
    in5 = bool(randint(0,1))

    tree1.reset()
    tree2.reset()

    outputs1 = tree1.calculate([in1, in2, in3, in4, in5])
    outputs2 = tree2.calculate([in1, in2, in3, in4, in5])

    print(outputs1)
    print(outputs2)
    print("\n")

    if outputs1 != outputs2:
        print("DOES NOT EQUAL")
