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


    ng = tree.get_num_gates() + 1
    tree.score = num_correct * 100 / ng
    return tree.score, tree.score
score_tree_xor.inputs = 2
score_tree_xor.outputs = 1

def score_tree_ha(tree):
    in1 = [False, True, False, True]
    in2 = [False, False, True, True]

    out1 = [False, True, True, False] #sum
    out2 = [False, False, False, True] #carry

    num_correct = 0
    output_subscores = [0,0]
    for x in range(len(in1)):
        tree.reset()
        outputs = tree.calculate([in1[x], in2[x]])
        if outputs[0] == out1[x]:
            num_correct+=1
            output_subscores[0]+=1
        if outputs[1] == out2[x]:
            num_correct+=1
            output_subscores[1]+=1

    tree.score = num_correct/(len(in1) * 2)
    output_subscores = [i / len(in1) for i in output_subscores]
    return tree.score, output_subscores
score_tree_ha.inputs = 2
score_tree_ha.outputs = 2

def score_tree_fa(tree):
    in1 = [False, True, False, True, False, True, False, True]
    in2 = [False, False, True, True, False, False, True, True]
    in3 = [False, False, False, False, True, True, True, True]

    out1 = [False, True, True, False, True, False, False, True] #sum
    out2 = [False, False, False, True, False, True, True, True] #carry

    num_correct = 0
    output_subscores = [0,0]
    for x in range(len(in1)):
        tree.reset()
        outputs = tree.calculate([in1[x], in2[x], in3[x]])
        if outputs[0] == out1[x]:
            num_correct+=1
            output_subscores[0]+=1
        if outputs[1] == out2[x]:
            num_correct+=1
            output_subscores[1]+=1

    tree.score = num_correct/(len(in1) * 2)
    output_subscores = [i / len(in1) for i in output_subscores]
    return tree.score, output_subscores
score_tree_fa.inputs = 3
score_tree_fa.outputs = 2


def gate_weight(num_correct):
    a = 7.594 * pow(10, -5)
    b = -0.00430
    c = 0.0190
    weight = a * pow(num_correct, 2) + (b * num_correct) + (c)
    weight = 0 if weight < 0 else weight
    return weight/4

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

    output_subscores = [i / len(in1) for i in output_subscores]
    ng = tree.get_num_gates()
    cp = tree.get_crit_path()
    """
    if num_correct == len(in1) * 3:
        print("**** accurate circuit")
        tree.score = 1 / (ng + cp + 1)
    else:
        #tree.score = num_correct / (len(in1) * 3)
        tree.score = (num_correct) - (gate_weight(num_correct) * ng)
    """
    if num_correct == len(in1) * 3:
        print("**** accurate circuit")
    tree.score = (num_correct) - (gate_weight(num_correct) * (cp))
    #tree.score = (num_correct)
    return tree.score, output_subscores
score_tree_2bit_add.inputs = 5
score_tree_2bit_add.outputs = 3





def score_tree_2bit_add_v2(tree):
    in1 = [False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True]
    in2 = [False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True]
    in3 = [False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True]
    in4 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
    in5 = [False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True]
    out1 = [False, True, True, False, False, True, True, False, True, False, False, True, True, False, False, True,
            False, True, True, False, False, True, True, False, True, False, False, True, True, False, False, True]
    out2 = [False, False, False, True, True, True, True, False, False, True, True, True, True, False, False, False,
            True, True, True, False, False, False, False, True, True, False, False, False, False, True, True, True]
    out3 = [False, False, False, False, False, False, False, True, False, False, False, False, False, True, True, True,
            False, False, False, True, True, True, True, True, False, True, True, True, True, True, True, True]

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

    output_subscores = [i / len(in1) for i in output_subscores]
    tree.score = num_correct / (len(in1) * 3)
    return tree.score, output_subscores
score_tree_2bit_add_v2.inputs = 5
score_tree_2bit_add_v2.outputs = 3



def score_tree_4bit_add(tree):
    in1 = [False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True,
           False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True] #cin
    in2 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True] #a0
    in3 = [False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True,
           False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True] #b0
    in4 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True] #a1
    in5 = [False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True,
           False, False, False, False, True, True, True, True, False, False, False, False, True, True, True, True] #b1
    in6 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True] #a2
    in7 = [False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True] #b2
    in8 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True] #a3
    in9 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True] #b3
    out1 = [False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True,
            True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True] #s0
    out2 = [False, False, False, True, True, True, True, False, False, False, False, True, True, True, True, False,
            False, False, False, True, True, True, True, False, False, False, False, True, True, True, True, False,
            False, True, True, True, True, False, False, False, False, True, True, True, True, False, False, False,
            False, True, True, True, True, False, False, False, False, True, True, True, True, False, False, False,
            True, True, True, False, False, False, False, True, True, True, True, False, False, False, False, True,
            True, True, True, False, False, False, False, True, True, True, True, False, False, False, False, True,
            True, False, False, False, False, True, True, True, True, False, False, False, False, True, True, True,
            True, False, False, False, False, True, True, True, True, False, False, False, False, True, True, True,
            False, False, False, True, True, True, True, False, False, False, False, True, True, True, True, False,
            False, False, False, True, True, True, True, False, False, False, False, True, True, True, True, False,
            False, True, True, True, True, False, False, False, False, True, True, True, True, False, False, False,
            False, True, True, True, True, False, False, False, False, True, True, True, True, False, False, False,
            True, True, True, False, False, False, False, True, True, True, True, False, False, False, False, True,
            True, True, True, False, False, False, False, True, True, True, True, False, False, False, False, True,
            True, False, False, False, False, True, True, True, True, False, False, False, False, True, True, True,
            True, False, False, False, False, True, True, True, True, False, False, False, False, True, True, True,
            False, False, False, True, True, True, True, False, False, False, False, True, True, True, True, False,
            False, False, False, True, True, True, True, False, False, False, False, True, True, True, True, False,
            False, True, True, True, True, False, False, False, False, True, True, True, True, False, False, False,
            False, True, True, True, True, False, False, False, False, True, True, True, True, False, False, False,
            True, True, True, False, False, False, False, True, True, True, True, False, False, False, False, True,
            True, True, True, False, False, False, False, True, True, True, True, False, False, False, False, True,
            True, False, False, False, False, True, True, True, True, False, False, False, False, True, True, True,
            True, False, False, False, False, True, True, True, True, False, False, False, False, True, True, True,
            False, False, False, True, True, True, True, False, False, False, False, True, True, True, True, False,
            False, False, False, True, True, True, True, False, False, False, False, True, True, True, True, False,
            False, True, True, True, True, False, False, False, False, True, True, True, True, False, False, False,
            False, True, True, True, True, False, False, False, False, True, True, True, True, False, False, False,
            True, True, True, False, False, False, False, True, True, True, True, False, False, False, False, True,
            True, True, True, False, False, False, False, True, True, True, True, False, False, False, False, True,
            True, False, False, False, False, True, True, True, True, False, False, False, False, True, True, True,
            True, False, False, False, False, True, True, True, True, False, False, False, False, True, True, True] #s1
    out3 = [False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, False,
            False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, False,
            False, False, False, False, False, True, True, True, True, True, True, True, True, False, False, False,
            False, False, False, False, False, True, True, True, True, True, True, True, True, False, False, False,
            False, False, False, True, True, True, True, True, True, True, True, False, False, False, False, False,
            False, False, False, True, True, True, True, True, True, True, True, False, False, False, False, False,
            False, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False,
            False, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False,
            True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, True,
            True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, True,
            True, True, True, True, True, False, False, False, False, False, False, False, False, True, True, True,
            True, True, True, True, True, False, False, False, False, False, False, False, False, True, True, True,
            True, True, True, False, False, False, False, False, False, False, False, True, True, True, True, True,
            True, True, True, False, False, False, False, False, False, False, False, True, True, True, True, True,
            True, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True,
            True, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True,
            False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, False,
            False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, False,
            False, False, False, False, False, True, True, True, True, True, True, True, True, False, False, False,
            False, False, False, False, False, True, True, True, True, True, True, True, True, False, False, False,
            False, False, False, True, True, True, True, True, True, True, True, False, False, False, False, False,
            False, False, False, True, True, True, True, True, True, True, True, False, False, False, False, False,
            False, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False,
            False, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False,
            True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, True,
            True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, True,
            True, True, True, True, True, False, False, False, False, False, False, False, False, True, True, True,
            True, True, True, True, True, False, False, False, False, False, False, False, False, True, True, True,
            True, True, True, False, False, False, False, False, False, False, False, True, True, True, True, True,
            True, True, True, False, False, False, False, False, False, False, False, True, True, True, True, True,
            True, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True,
            True, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True] #s2
    out4 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False,
            False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True,
            True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False,
            False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True,
            True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True,
            True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True,
            True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
            False, False, False, False, False, False, False, False, False, False, False, False, False, False, True,
            True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False,
            False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True,
            True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True,
            True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True,
            True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True,
            True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True,
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False,
            False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False,
            False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True,
            True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True,
            True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True,
            True, True, True, True, True, True, True] #s3
    out5 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False, True, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, False, False, False, False, False, True,
            True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True,
            True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True,
            True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True,
            True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True,
            True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True,
            True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False,
            False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
            True, True, False, False, False, False, False, False, False, False, False, False, False, True, True, True,
            True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
            False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True,
            True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False,
            False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True,
            True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False,
            False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
            True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, True,
            True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
            True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True,
            True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
            True, True, True, True, True] #cout

    num_correct = 0
    output_subscores = [0,0,0,0,0]
    for x in range(len(in1)):
        tree.reset()
        outputs = tree.calculate([in1[x], in2[x], in3[x], in4[x], in5[x], in6[x], in7[x], in8[x], in9[x]])

        if outputs[0] ==out1[x]:
            num_correct+=1
            output_subscores[0]+=1

        if outputs[1] == out2[x]:
            num_correct+=1
            output_subscores[1]+=1

        if outputs[2] == out3[x]:
            num_correct+=1
            output_subscores[2]+=1

        if outputs[3] == out4[x]:
            num_correct+=1
            output_subscores[3]+=1

        if outputs[4] == out5[x]:
            num_correct+=1
            output_subscores[4]+=1



    output_subscores = [i / len(in1) for i in output_subscores]
    tree.score = num_correct / (len(in1) * 5)
    return tree.score, output_subscores
score_tree_4bit_add.inputs = 9
score_tree_4bit_add.outputs = 5