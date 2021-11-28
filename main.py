from random import sample, choices
from time import time
from Tree import Tree
from fitness_funcs import *
from multiprocessing import Pool, cpu_count
import pickle

def main():
    test_tree = Tree(3, 2)
    out = test_tree.calculate([False, False, True])
    if None in out:
        raise Exception("got none output")

max_score = 0
accuracy_dist = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}


def run_ga(fitness_f, num_levels, width, inputs, outputs, pop_size=100, reserve_size=10):
    max_score = 0
    num_searched = 0

    best = [None]
    reserve = []
    generation_count = 0
    while max_score < 1:
        start_time = time()
        population = []
        population += reserve
        avg_fitness = 0
        for x in range(pop_size):
            p1 = sample(best, 1)[0]
            p2 = sample(best, 1)[0]
            population.append(Tree(inputs, outputs, t1=p1, t2=p2, num_levels=num_levels, width=width))
        for x in range(pop_size // 10):  # keep introducing new ones
            population.append(Tree(inputs, outputs, num_levels=num_levels, width=width))


        for p in range(len(population)):
            score, subscore = fitness_f(population[p])
            population[p].score = score
            population[p].subscore = subscore
            avg_fitness+=score
            if score > max_score:
                max_score = score

            #print(population[p])
        num_searched += len(population)
        avg_fitness = avg_fitness / len(population)
        population.sort(key=lambda x: x.score, reverse=True)
        best = population[0:reserve_size]
        reserve = population[0:reserve_size]
        generation_count += 1
        print(f"Current Generation:{generation_count}, best accuracy:{max_score}, best tree: \n{best[0]} ")
        print(f"Average Fitness: {avg_fitness}")
        print(f"Time taken: {time() - start_time}")
        print(f"Number of circuits searched {num_searched}")

    fitness_f(best[0])
    return best[0], num_searched


def run_ga_mp(fitness_f, num_levels, width, inputs, outputs, pop_size=100, reserve_size=10):
    pool = Pool(processes=cpu_count())

    max_score = 0
    num_searched = 0

    best = [None]
    reserve = []
    generation_count = 0
    #while generation_count < 2000:
    while max_score < 1:
        start_time = time()
        population = []
        population += reserve
        avg_fitness = 0
        for x in range(pop_size):
            #p1 = sample(best, 1)[0]
            #p2 = sample(best, 1)[0]

            probs = list(range(1,pop_size+1)).reverse()
            p1 = choices(best, weights=probs, k=1)[0]
            p2 = choices(best, weights=probs, k=1)[0]

            population.append(Tree(inputs, outputs, t1=p1, t2=p2, num_levels=num_levels, width=width))
        for x in range(pop_size // 10):  # keep introducing new ones
            population.append(Tree(inputs, outputs, num_levels=num_levels, width=width))

        """
        for p in range(len(population)):
            score = fitness_f(population[p])
            avg_fitness+=score
            if score > max_score:
                max_score = score

            #print(population[p])
        """
        fitness_results = pool.map(fitness_f, population)
        unzipped_results = list(zip(*fitness_results))
        fitness_results = unzipped_results[0]
        subscores = unzipped_results[1]
        #print(fitness_results)
        #print(subscores)

        avg_fitness = sum(fitness_results)
        avg_fitness = avg_fitness / len(population)
        num_searched += len(population)
        for y in range(len(fitness_results)):
            population[y].score = fitness_results[y]
            population[y].subscores = subscores[y]

        population.sort(key=lambda x: x.score, reverse=True)
        if population[0].score > max_score:
            max_score = population[0].score
        best = population[0:reserve_size]
        reserve = population[0:reserve_size]
        generation_count += 1
        print(f"Current Generation:{generation_count}, best accuracy:{max_score}, best tree: \n{best[0]} ")
        print(f"Number of gates: {best[0].get_num_gates()}, Crit Path: {best[0].get_crit_path()}")
        print(f"Average Fitness: {avg_fitness}")
        print(f"Time taken: {time() - start_time}")
        print(f"Number of circuits searched {num_searched}")

    pool.close()
    fitness_f(best[0])
    return best[0], num_searched


def random_search(fitness_f, num_levels, width, inputs, outputs):
    max_score = 0
    num_searched = 0
    tree = None
    while max_score < 1:
        tree = Tree(inputs, outputs, num_levels=num_levels, width=width)
        fit = fitness_f(tree)
        if fit > max_score:
            max_score = fit
        num_searched += 1
        if num_searched % 500 == 0:
            print(f"Searched: {num_searched}, Max score: {max_score}")
    return tree, num_searched


def compare_methods():
    fitness_f = score_tree_fa
    inputs = fitness_f.inputs  # look at fitness function to determine inputs
    outputs = fitness_f.outputs  # look at  determine outputs
    num_levels = 7
    width = 7

    pop_size = 3000
    reserve_size = 300

    run_for = 10

    start_time = time()
    circuits_searched = 0
    for x in range(run_for):
        best_tree, num_searched = run_ga(fitness_f, num_levels, width, inputs, outputs, pop_size=pop_size, reserve_size=reserve_size)
        print(f"Finished {x}")
        circuits_searched+=num_searched
    print(f"Average Time GA non mp {run_for} trials: {(time() - start_time) / run_for}")
    print(f"Average number of ciruits searched {circuits_searched/run_for}")

    start_time = time()
    circuits_searched = 0
    for x in range(run_for):
        best_tree, num_searched = random_search(fitness_f, num_levels, width, inputs, outputs)
        print(f"Finished {x}")
        circuits_searched += num_searched
    print(f"Average Time Random Search {run_for} trials: {(time() - start_time) / run_for}")
    print(f"Average number of ciruits searched {circuits_searched / run_for}")

def run_search():
    fitness_f = score_tree_4bit_add
    inputs = fitness_f.inputs  # look at fitness function to determine inputs
    outputs = fitness_f.outputs  # look at  determine outputs
    num_levels = 30
    width = 30

    pop_size = 5000
    reserve_size = 500

    start_time = time()
    #best_tree = random_search(fitness_f, num_levels, width, inputs, outputs)
    best_tree = run_ga_mp(fitness_f, num_levels, width, inputs, outputs, pop_size=pop_size, reserve_size=reserve_size)
    best_tree = best_tree[0] #first element is the object
    print(f"Total time taken: {time() - start_time}")
    print(best_tree)
    with open("4bit_adder.pkl", "wb+") as f:
        pickle.dump(best_tree, f)
    best_tree.visualize_tree()


def average_search():
    fitness_f = score_tree_xor
    inputs = fitness_f.inputs  # look at fitness function to determine inputs
    outputs = fitness_f.outputs  # look at  determine outputs
    num_levels = 5
    width = 5

    pop_size = 500
    reserve_size = 50

    run_for = 10
    start_time = time()
    circuits_searched = 0
    for x in range(run_for):
        best_tree, num_searched = run_ga_mp(fitness_f, num_levels, width, inputs, outputs, pop_size=pop_size, reserve_size=reserve_size)
        print(f"Finished {x}")
        circuits_searched += num_searched
    print(f"Average Time Random Search {run_for} trials: {(time() - start_time) / run_for}")
    print(f"Average number of ciruits searched {circuits_searched / run_for}")



if __name__ == "__main__":
    #compare_methods()
    run_search()
    #average_search()
