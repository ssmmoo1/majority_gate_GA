#types: fixed input, majority, not, output
from random import sample
from enum import Enum


class Gate():
    MAJORITY = 1 #3:1 input majority gate
    NOT = 2 #1:1 not gate
    NONE = 3 #does no operation, has no input or output
    OUTPUT=4 #1 input it just outputs it again
    INPUT=5 #no input and 1 output, gates value is directly set by the testing code

    gate_inputs = {MAJORITY: 3, NOT: 1, NONE: 0, OUTPUT: 1,
                   INPUT: 0}  # define how many inputs each gate type has

    @staticmethod
    def get_random_gate():
        choices = [Gate.MAJORITY, Gate.NOT, Gate.NONE]
        return sample(choices,1)[0]


class Node:
    def __init__(self, type, parents=None, output=None, row=None, col=None):
        self.parents = parents
        self.type = type
        self._output = output
        self.row=row
        self.col=col


    def set_output(self, val):
        self._output = val

    def get_output(self):
        #cases that do not modify the output value, just return what it already has
        if self._output != None or self.type == Gate.INPUT:
            return self._output

        if len(self.parents) != Gate.gate_inputs[self.type]:
            raise Exception("Gate does not have the right number of inputs")

        #cases that need to calculate the output value and store it for future use
        elif self.type == Gate.MAJORITY: #calculate 3 input majority
            a = self.parents[0].get_output()
            b = self.parents[1].get_output()
            c = self.parents[2].get_output()

            self._output = (b and c) or (a and (b ^ c))


        elif self.type == Gate.NOT: #calculate not
            self._output = not self.parents[0].get_output()

        elif self.type == Gate.OUTPUT: #pass the parents output, used for the last layer
            self._output = self.parents[0].get_output()

        else: #all cases should be covered
            raise Exception("illegal node type")

        return self._output
