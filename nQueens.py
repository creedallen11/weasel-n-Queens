# -*- coding: utf-8 -*-
# Python 3.4*
'''
INPUT:
To run an nQueens problem with n queens I should be able to be run as follows in python:
import weasel_py3
weasel_py3.nQueens(8, 'realPop')

and also to do this at the command line:
python weasel_py3 8 realPop


OUTPUT:
Returns the sequence of y positions from left to right which are a solution as a list
e.g. return [7, 3, 0, 2, 5, 1, 6, 4] for 8-queens
'''

from random import choice, random, uniform, sample
import sys

def fitness(seq):
    'Fitness is the number of pairs of queens that are NOT attacking each other.'

    total_pairs = sum(n_set)  # of non attacking : # of total_pairs
    total = 0

    for i in range(len(seq)):
        for j in range(i +1, len(seq)):
            if seq[i] == seq[j] or ((j-i) == abs(seq[i] - seq[j])): 
                total += 1

    return (total_pairs - total)

def mutaterate(bestParent):
    '''
    Less mutation the closer the fit of the parent.
    This is not the most biologically realistic,
    but is decent to mimick T of simulated annealing.
    Performance is actually sensitive to below schedule
    '''
    #TODO: making this annealing temperature non-linear would likely improve performance
    return 1-((perfectfitness - fitness(bestParent)) / perfectfitness * (.9))

def mutate(sequence, rate): 
    return [(ch if random() <= rate else choice(n_set)) for ch in sequence]


def status_log(iterations, bestParent, rate):
    'prints progress'
    print ("Run %-4i had fitness=%4.1f%%, sequence= '%s', and mutation rate p=%-4f/char" %
           (iterations, fitness(bestParent)*100./perfectfitness, bestParent, 1-rate))


def mate(a, b):
    """
    Mates two parents via sexual reproduction (crossing over).
    Crossing over happens with ~p=0.7
    """
    place = 0
    if choice(range(10)) < 7:
        place = choice(n_set)
    else:
        return a, b
    return a[:place] + b[place:], b[:place] + a[place:]


def get_lucky(items):
    '''
    Chooses a random element from items,
    where items is a list of tuples in the form (item, weight).
    weight determines the probability of choosing its respective item.
    '''
    weight_total = sum((item[1] for item in items))
    n = uniform(0, weight_total)
    for item, weight in items:
        if n < weight:
            return item
        n = n - weight
    return item

def nQueens(n_size, pop_version='realPop'):
    '''
    Inputs:
    n_size as int (n x n board size), pop_version (realPop or pseudoPop)
    realPop is default

    Output:
    Returns the sequence of y positions from left to right which are a solution as a list
    e.g. return [7, 3, 0, 2, 5, 1, 6, 4] for 8-queens

    Example:
    nQueens(n_size=8, pop_version = 'realPop' or 'pseudoPop')
    '''

    global n_set, perfectfitness, total_pairs, iterations

    n_set = [x for x in range(n_size)] 
    perfectfitness = float(sum(n_set)) # n choose 2 (all pairs) is the num of pairs we want NOT attacking each other

    POP_SIZE = 100 # treat this like a parameter, select empirically if modifying the problem 
    bestParent = [choice(n_set) for _ in range(len(n_set))]
    center = int(POP_SIZE/2)
    total_pairs = float(sum(n_set)) # n choose 2
    iterations = 0


    while fitness(bestParent) != perfectfitness:
        rate = mutaterate(bestParent)
        iterations += 1
        if iterations % 250 == 0:
            status_log(iterations, bestParent, rate) 
        if pop_version == 'pseudoPop': # hacked up version by Dr Taylor
            # Pseudo-population section is a bit of a hack,is not really bio-realistic,
            # and not really a good population for many problems with local minima,
            # since a single parents produces an entire generation,
            # after which, only two single best individuals are breeding
            # to produce 1 offspring.

            children = [mutate(bestParent, rate) for _ in range(POP_SIZE)] + [bestParent]
            twentysomething1 = max(children[:center], key=fitness)
            twentysomething2 = max(children[center:], key=fitness)
            bestParent = max(mate(twentysomething1, twentysomething2), key=fitness)
        
        else: #book method
            if iterations == 1:
                population = [mutate(bestParent, rate) for _ in range(POP_SIZE)] + [bestParent]
            
            sexy_breeders = []
            for individual in population: 
                fitness_val = fitness(individual)
                pair = (individual, fitness_val/perfectfitness)
                sexy_breeders.append(pair) # tuple of individual and their fitness relative to perfect fitness  -> sexy_breeders

            population = []
            for _ in range(int(POP_SIZE/2)):
                parent1 = get_lucky(sexy_breeders)
                parent2 = get_lucky(sexy_breeders)
                child1, child2 = mate(parent1, parent2)
                population.append(mutate(child1, rate))
                population.append(mutate(child2, rate))

            bestParent = max(population, key=fitness) # find best based on key function fitness

    status_log(iterations, bestParent, rate)
    return bestParent

if __name__ == "__main__":
    total = len(sys.argv)
    if total == 3:
        nQueens(int(sys.argv[1]), str(sys.argv[2]))
    elif total == 2:
        nQueens(int(sys.argv[1]), 'pseudoPop')
    else:
        print('You supplied too many inputs and should read the docstring first!')