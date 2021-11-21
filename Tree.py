from random import randint, sample, seed, uniform, sample
import tkinter
from Node import Gate, Node

class Tree:

    # Generate a random tree or a cross bred tree
    def __init__(self, num_inputs, num_outputs, num_levels=5, width=5, t1=None, t2=None):

        self.num_inputs = num_inputs  # the number of single bit inputs to the circuit
        self.num_outputs = num_outputs  # the number of single bit outputs to the circuit
        self.num_levels = num_levels  # the number of levels allowed in the circuit, includes the input and output levels. so gates levels is num_levels-2
        self.width = width  # the number of gates allowed in each level

        self.score = 0  # the initial fitness score

        assert (self.num_levels >= 3), "Must have at least 3 levels"  # 1 inputs, 1 gate, 1 output

        self.layers = [[None for col in range(self.width)] for row in range(self.num_levels)]  # init 2d array

        # setup input layer
        self.layers[0] = [Node(Gate.INPUT, output=False, row=0, col=0), Node(Gate.INPUT, output=True, row=0,
                                                                                  col=1)]  # create two extra nodes for a 1 and 0 constant values
        for n in range(num_inputs):
            self.layers[0].append(Node(Gate.INPUT, row=0, col=n + 2))  # create input nodes

        # setup middle layers
        if t1 is not None and t2 is not None:  # If there are two parents, then combine them to create this tree
            self.gen_middle_breed(t1, t2)
        else:  # if parents are not provided, then randomly generate the middle layer
            self.gen_middle_rand()

        # setup output layers
        self.layers[num_levels - 1] = []  # reinit this because output length may not be the same as the width
        for n in range(num_outputs):
            self.layers[num_levels - 1].append(
                Node(Gate.OUTPUT, parents=self.assign_parents(num_levels - 1, 1), row=num_levels - 1, col=n))

    def gen_middle_breed(self, t1, t2):
        for row in range(1, self.num_levels - 1):  # iterate through middle layers (gate layers)
            for col in range(self.width):
                # three possibilities - parent a, parent b, random, 45,45,10
                r_num = uniform(0, 1)
                n_type = Gate.NONE
                if r_num <= 0.35:  # get parent 1 type at the same location
                    n_type = t1.layers[row][col].type
                elif r_num > 0.35 and r_num <= 0.70:  # get parent 2 type at the same location
                    n_type = t2.layers[row][col].type
                else:  # random type
                    n_type = Gate.get_random_gate()

                temp_node = Node(n_type, self.assign_parents(row, Gate.gate_inputs[n_type]), row=row, col=col)
                self.layers[row][col] = temp_node

    def gen_middle_rand(self):
        # setup the mid layers
        for row in range(1, self.num_levels - 1):  # iterate through all middle layers
            for col in range(self.width):
                n_type = Gate.get_random_gate()  # assign a random gate type
                temp_node = Node(n_type, self.assign_parents(row, Gate.gate_inputs[n_type]), row=row,
                                 col=col)  # assign random parents based on gate type
                self.layers[row][col] = temp_node  # put the node in the tree

    def __str__(self):
        type_map = {Gate.INPUT: "I", Gate.OUTPUT: "O", Gate.MAJORITY: "M", Gate.NOT: "N",
                    Gate.NONE: "-"}
        str_rep = ""
        for row in self.layers:
            for col in row:
                if col is not None:
                    str_rep += type_map[col.type]
                else:
                    str_rep += " "
            str_rep += "\n"

        return str_rep

    def reset(self):
        # reset the input nodes except or static 0 and 1
        for n in range(2, len(self.layers[0])):
            self.layers[0][n].set_output(None)

        # reset the rest of the nodes to none output so they get recalculated
        for row in range(1, len(self.layers)):
            for col in range(len(self.layers[row])):
                node = self.layers[row][col]
                node.set_output(None)

    # returns an array of node references that are above the current node in the tree
    def assign_parents(self, row, num_parents):
        if num_parents == 0:  # handle case for none gates
            return None

        # determine gate locations above the current one for potential parents
        available_rows = range(row)

        parents = []
        count = 0
        while count < num_parents:  # choose parents that are not None type

            r = sample(available_rows, 1)[0]

            available_cols = range(len(self.layers[r]))
            c = sample(available_cols, 1)[0]

            if self.layers[r][c].type != Gate.NONE:  # make sure chosen parent exists otherwise find another
                parents.append(self.layers[r][c])
                count += 1
            else:
                # parents.append(self.layers[0][0]) #give it default zero for now. might want to explore other behavior. *this performs worse for accuracy than just retrying another random parent
                # count+=1
                continue

        return parents

    #remove unused nodes in the tree
    def prune_tree(self):
        pass


    def calculate(self, input_values):
        if len(input_values) != len(self.layers[0]) - 2:
            raise Exception("wrong number of inputs")

        for x in range(2, len(self.layers[0])):  # set the input node values
            self.layers[0][x].set_output(input_values[x - 2])

        outputs = []
        for x in range(self.num_outputs):  # loop through ouputs and get the outputs
            outputs.append(self.layers[-1][x].get_output())  # this is recursive
        # print(outputs)
        return outputs

    # recursive helper function
    def draw_tree(self, current_node, canvas):
        gate_colors = {Gate.MAJORITY: "#9fe2bf", Gate.NOT: "#de3163", Gate.NONE: "#ffffff",
                       Gate.OUTPUT: "#a569bd",
                       Gate.INPUT: "#a569bd"}  # define how many inputs each gate type has
        size = 30
        space = 6  # multiple of size
        start_offset = 5

        x_val = (current_node.col * size * space) + (size + start_offset)
        y_val = (current_node.row * size * space) + (size + start_offset)

        canvas.create_oval(x_val - size, y_val - size, x_val + size, y_val + size, fill=gate_colors[current_node.type],
                           outline=gate_colors[current_node.type], width=3)

        if current_node.parents is not None:
            for p in current_node.parents:

                p_x = (p.col * size * space) + (size + start_offset)
                p_y = (p.row * size * space) + (size + start_offset)

                canvas.create_line(x_val, y_val, p_x, p_y, width=5, fill="#" + ("%06x" % randint(0, 0xFFFFFF)))
                self.draw_tree(p, canvas)

    # THIS BLOCKS FOREVER ONLY CALL ONCE AT END OF PROGRAM
    def visualize_tree(self):
        # init tk
        root = tkinter.Tk()

        # create canvas
        canvas = tkinter.Canvas(root, bg="white", height=1500, width=1500)

        # add to window and show
        canvas.pack()

        for output_node in self.layers[-1]:
            self.draw_tree(output_node, canvas)

        root.mainloop()