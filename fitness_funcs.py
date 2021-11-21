def score_tree_and(tree):
    in1 = [False, False, True, True]
    in2 = [False, True, False, True]

    out1 = [False, False, False, True]

    num_correct = 0
    for x in range(len(in1)):
        tree.reset()
        outputs = tree.calculate([in1[x], in2[x]])
        if outputs[0] == out1[x]:
            num_correct += 1

    tree.score = num_correct/len(in1)
    return tree.score
score_tree_and.inputs = 2
score_tree_and.outputs = 1

def score_tree_or(tree):
    in1 = [False, False, True, True]
    in2 = [False, True, False, True]

    out1 = [False, True, True, True]

    num_correct = 0
    for x in range(len(in1)):
        tree.reset()
        outputs = tree.calculate([in1[x], in2[x]])
        if outputs[0] == out1[x]:
            num_correct += 1

    tree.score = num_correct/len(in1)
    return tree.score
score_tree_or.inputs = 2
score_tree_or.outputs = 1

def score_tree_xor(tree):
    in1 = [False, False, True, True]
    in2 = [False, True, False, True]

    out1 = [False, True, True, False]

    num_correct = 0
    for x in range(len(in1)):
        tree.reset()
        outputs = tree.calculate([in1[x], in2[x]])
        if outputs[0] == out1[x]:
            num_correct += 1

    tree.score = num_correct/len(in1)
    return tree.score
score_tree_xor.inputs = 2
score_tree_xor.outputs = 1

def score_tree_ha(tree):
    in1 = [False, True, False, True]
    in2 = [False, False, True, True]

    out1 = [False, True, True, False] #sum
    out2 = [False, False, False, True] #carry

    num_correct = 0
    for x in range(len(in1)):
        tree.reset()
        outputs = tree.calculate([in1[x], in2[x]])
        if outputs[0] == out1[x] and outputs[1] == out2[x]:
            num_correct+=1

    tree.score = num_correct/len(in1)
    return tree.score
score_tree_ha.inputs = 2
score_tree_ha.outputs = 2

def score_tree_fa(tree):
    in1 = [False, True, False, True, False, True, False, True]
    in2 = [False, False, True, True, False, False, True, True]
    in3 = [False, False, False, False, True, True, True, True]

    out1 = [False, True, True, False, True, False, False, True] #sum
    out2 = [False, False, False, True, False, True, True, True] #carry

    num_correct = 0
    for x in range(len(in1)):
        tree.reset()
        outputs = tree.calculate([in1[x], in2[x], in3[x]])
        if outputs[0] == out1[x] and outputs[1] == out2[x]:
            num_correct+=1

    tree.score = num_correct/len(in1)
    return tree.score
score_tree_fa.inputs = 3
score_tree_fa.outputs = 2


def score_tree_2bit_add(tree):
    in1 = [False, True,  False, True,   False, True,  False, True,   False, True,  False, True,   False, True,  False, True,
           False, True,  False, True,   False, True,  False, True,   False, True,  False, True,   False, True,  False, True] #cin

    in2 = [False, False, True,  True,   False, False, True,  True,   False, False, True,  True,   False, False, True,  True,
           False, False, True,  True,   False, False, True,  True,   False, False, True,  True,   False, False, True,  True] #a0

    in3 = [False, False, False, False,  True,  True,  True,  True,   False, False, False, False,  True,  True,  True,  True,
           False, False, False, False,  True,  True,  True,  True,   False, False, False, False,  True,  True,  True,  True] #b0

    in4 = [False, False, False, False,  False, False, False, False,  True,  True,  True,  True,   True,  True,  True,  True,
           False, False, False, False,  False, False, False, False,  True,  True,  True,  True,   True,  True,  True,  True] #a1

    in5 = [False, False, False, False,  False, False, False, False,  False, False, False, False,  False, False, False, False,
           True,  True,  True,  True,   True,  True,  True,  True,   True,  True,  True,  True,   True,  True,  True,  True] #b1

    out1 = [False, True, True,  False,  True,  False, False, True,   False, True,  True,  False,  True,  False, False, True,
            False, True, True,  False,  True,  False, False, True,   False, True,  True,  False,  True,  False, False, True] #s0
    out2 = [False, False,False, True,   False, True,  True,  True,   True,  True,  True,  False,  True,  False, False, False,
            True,  True, True,  False,  True,  False, False, False,  False, False, False, True,   False, True,  True,  True] #s1
    out3 = [False, False,False, False,  False, False, False, False,  False, False, False, True,   False, True,  True,  True,
            False, False,False, True,   False, True,  True,  True,   True,  True,  True,  True,   True,  True,  True,  True] #cout

    num_correct = 0
    output_subscores = [0,0,0]
    for x in range(len(in1)):
        tree.reset()
        outputs = tree.calculate([in1[x], in2[x], in3[x], in4[x], in5[x]])

        if outputs[0] ==out1[x]:
            num_correct+=1
            output_subscores[0]+=1

        if outputs[1] == out2[x]:
            num_correct+=1
            output_subscores[1]+=1

        if outputs[2] == out3[x]:
            num_correct+=1
            output_subscores[2]+=1


    tree.score = num_correct / (len(in1) * 3)
    return tree.score
score_tree_2bit_add.inputs = 5
score_tree_2bit_add.outputs = 3