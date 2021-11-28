from random import randint, sample, seed, uniform, sample, shuffle, triangular
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
        self.subscores = None

        assert (self.num_levels >= 3), "Must have at least 3 levels"  # 1 inputs, 1 gate, 1 output

        self.layers = [[None for col in range(self.width)] for row in range(self.num_levels)]  # init 2d array

        # setup input layer
        self.layers[0] = [Node(Gate.INPUT, output=False, row=0, col=0), Node(Gate.INPUT, output=True, row=0,
                                                                                  col=1)]  # create two extra nodes for a 1 and 0 constant values
        for n in range(num_inputs):
            self.layers[0].append(Node(Gate.INPUT, row=0, col=n + 2))  # create input nodes


        if t1 is not None and t2 is not None:
            self.layers[num_levels - 1] = [None] * num_outputs  # reinit this because output length may not be the same as the width
            out_list = list(range(num_outputs))
            shuffle(out_list)
            for n in out_list:  # randomize order the output subcircuits are copied in
                p_choice = sample([t1,t2], 1)[0]
                #p_choice = None
                #smaller = t1 if t1.subscores[n] < t2.subscores[n] else t2
                #larger = t1 if t1.subscores[n] >= t2.subscores[n] else t2
                #r_num = uniform(0,1)
                #cutoff = 1 / ( (larger.subscores[n] / smaller.subscores[n]) + 1)
                #p_choice = smaller if r_num < cutoff else larger

                self.gen_node_breed(num_levels - 1, n, p_choice)


            num_gates = 0
            for r in self.layers:
                for n in r:
                    if n is not None:
                        num_gates+=1

            num_gates = int(triangular(0, num_gates, num_gates / 10))
            for r in range(randint(0,int(num_gates*0.2))):
                flip = randint(0,1)
                if flip == 1:
                    self.mutate()
                else:
                    self.remove_gate()
            #self.prune_tree()

        #if not crossbreeding then randomly generate the middle and output layers
        else:
            # setup output and middle layers recursively
            self.layers[num_levels - 1] = [None] * num_outputs  # reinit this because output length may not be the same as the width
            for n in range(num_outputs):
                self.gen_node(num_levels-1, n, gate_type=Gate.OUTPUT)


    #recursively generate a tree to represent the circuit
    #should update self.layers. No return. Should be called explicitly on all output nodes
    def gen_node(self, row, col, gate_type=None):
        if row == 0: #hit an input node so stop
            return

        else: #if not an input node then need to generate a new node
            if gate_type is None: #get a random gate type not or maj
                gate_type = Gate.get_random_gate()

            parents = []
            for x in range(Gate.gate_inputs[gate_type]): #find the right number of parents
                available_rows = range(row)
                p_r = sample(available_rows, 1)[0]

                available_cols = range(len(self.layers[p_r]))
                p_c = sample(available_cols,1)[0]

                if self.layers[p_r][p_c] == None: #if the chosen parent hasn't been generated then generate the parent
                    self.gen_node(p_r, p_c)

                parents.append(self.layers[p_r][p_c]) #once generated add to parent list

            self.layers[row][col] = Node(gate_type, parents=parents, row=row, col=col)  #once enough parents are made, generate this node

    #basically the same as gen_node but copys the genetic_parent's gate types and connections
    def gen_node_breed(self, row, col, genetic_parent):
        if row == 0:
            return

        gate_type = genetic_parent.layers[row][col].type #set this gate's type
        parents = []
        for p in genetic_parent.layers[row][col].parents: #iterate through the input connections (parents). should follow the same as the genetic parent
            if self.layers[p.row][p.col] == None: #if the node hasn't been setup yet then generate it
                self.gen_node_breed(p.row, p.col, genetic_parent)

            parents.append(self.layers[p.row][p.col])

        self.layers[row][col] = Node(gate_type, parents=parents, row=row, col=col)

    def mutate(self):
        #gate wise mutations
        #flatten layers to make it easy to get random nodes
        flat_layers = []
        for r in self.layers[1:]:
            for n in r:
                if n is not None:
                    flat_layers.append(n)

        m_gate = sample(flat_layers,1)[0]

        available_rows = range(m_gate.row)
        r = sample(available_rows, 1)[0]

        available_cols = range(len(self.layers[r]))
        c = sample(available_cols, 1)[0]
        self.gen_node(r, c)

        m_gate.parents[randint(0,len(m_gate.parents)-1)] = self.layers[r][c]


    def mutate_connection(self):
        #choose random node

        #get nodes parent

        #insert a node at the row above chosen node

        #change parent to the new node

        #add original parent as a parent of the new node

        #fill in addition parents for the new node if needed (only for majority gate)
        pass

    def get_open_col(self, row):
        for col in range(len(self.layers[row])):
            if self.layers[row][col] == None:
                return col

        return None

    def remove_gate(self):
        #choose a random node


        available_rows = range(1,self.num_levels-1)
        r = sample(available_rows, 1)[0]

        available_cols = range(len(self.layers[r]))
        c = sample(available_cols, 1)[0]
        node = self.layers[r][c]
        if node is None:
            return
        #get its children
        children = []
        for r in self.layers[1:]:
            for c_node in r:
                if c_node is not None:
                    if node in c_node.parents:
                        children.append(c_node)

        #give all children the parent of the this nodes input

        for c in children:
            new_p = sample(node.parents, 1)[0]
            i = c.parents.index(node)
            c.parents[i] = new_p

        #remove node from 2d array
        self.layers[node.row][node.col] = None


    def prune_tree_helper(self, node):
        self.used_spots[node.row][node.col] = True
        if node.type == Gate.INPUT:
            return
        else:
            for p in node.parents:
                self.prune_tree_helper(p)

    def prune_tree(self):
        #removes nodes that are not in an output path
        self.used_spots = [[False for col in range(self.width)] for row in range(self.num_levels)]
        for c in range(len(self.layers[0])):
            self.used_spots[0][c] = True

        for node in self.layers[-1]:
            self.prune_tree_helper(node)


        for r in range(len(self.layers)):
            for c in range(len(self.layers[r])):
                if self.used_spots[r][c] == False:
                    self.layers[r][c] = None

        #print(self)


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
                if node is not None:
                    node.set_output(None)


    # returns a random node that is above the row
    def get_random_parent(self, row):
        # determine gate locations above the current one for potential parent
        p = None
        while p is None:

            available_rows = range(row)
            r = sample(available_rows, 1)[0]

            available_cols = range(len(self.layers[r]))
            c = sample(available_cols, 1)[0]
            p = self.layers[r][c]
        return p

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
        size = 20
        space = 3  # multiple of size
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
        canvas = tkinter.Canvas(root, bg="white", height=1500, width=2000)

        # add to window and show
        canvas.pack()

        for output_node in self.layers[-1]:
            self.draw_tree(output_node, canvas)

        root.mainloop()



    def get_num_gates(self):
        g_count  = 0
        for r in self.layers[1:-1]:
            for n in r:
                if n is not None:
                    g_count+=1
        return g_count


    def crit_path_helper(self, node, current_max):
        if node.type == Gate.INPUT:
            if current_max > self.crit_path:
                self.crit_path = current_max
            return

        for p in node.parents:
            self.crit_path_helper(p, current_max+1)


    def get_crit_path(self):
        self.crit_path = 0
        for node in self.layers[self.num_levels-1]:
            self.crit_path_helper(node, -1)

        return self.crit_path


    """ 
    def equal_helper(self, other_node):    
        if other_node.row == 0:
            return True
        
        if other_node.type is not self.layers[other_node.row][other_node.col].type:
            return False
        
        for other_p in other_node.parents:
            if
            
    
    def __eq__(self, other):
        for o in self.layers[-1]: #iterate through output layers
            if self.equal_helper(other.layers[self.layers-1][0]) == False:
                return False
        return True
    """