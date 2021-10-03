"""
The genetic_alg module contains the code to perform a genetic algorithm to find
optimal values for the expanded elo functions. The algorithm takes values set
randomly for the expanded elo functions for the population entities and uses
the percentage of games won from the prediction_expanded_stats as the fitness
function.

Usage
-----
Call genetic_algorithm() to run the algorithm. The function can take 2 inputs,
one for the population size (pop_size) and one for the number of generations run
(generations). Defaults to 100 pop_size and 100 generations.

Methods
-------
genetic_algorithm(int pop_size, int generations) ->
                                        list[list entity, float fitness_value]:
    function called to run the genetic algorithm. inputs determine the scope and
    depth of the algorithm.
_reproduce(list parent1, list parent2) -> list child:
    function takes in 2 list of weights and randomly selects gene from both
    parents or 'mutates' and takes a random gene.
_mutate(int index) -> int/float:
    index input determines which random function is called to represent mutation,
    calling the random function associated with which gene is being replaced.
_population_fitness(list entity) -> list[list entity, float fitness]:
    calculates the fitness value given the weights in an entity. returns the
    entity and the fitness value.
_population_fitnesses(list[list entity]) -> list[list[list entity, float fitness]]:
    calculates the fitness values for all entities in a population. returns a
    list of the entities and their fitness value.
_initial_population(int pop_size) -> list[entity]:
    returns a list of randomly generated entities (list of weights) of length
    pop_size.
_create_single() -> list:
    creates and returns a single, randomly generated entity (list of weights)
    to be used in a population.
_random_k() -> int:
    returns a random int to be used as a weight for the k-factor.
_random_rf() -> int:
    returns a random int to be used as a weight for the rating-factor.
_random_hfa() -> int:
    returns a random int to be used as a weight for the home field advantage.
_random_scale() -> float:
    returns a random float to be used as a weight for the seasonal scaling.
_random_playoff_multiplier() -> float:
    returns a random float to be used as a weight for the playoff multiplier.
"""

import math
from random import randint, random
from stat_eval import prediction_expanded_stats, get_accuracy

#WEIGHTS = ['k', 'rf', 'hfa', 'scale', 'pm']

#TODO: change random generated genes to SINGLE function
#TODO: error check pop size so pruning doesn't make len(pop) 0
def genetic_algorithm(pop_size=100, generations=100):
    """
    Genetic algorithm is the main function that is called to try and generate
    the ideal weights to be used in the elo calculations. The entities are
    a list of values representing the weights for the k-factor, rating-factor,
    home field advantage, seasonal scaling, and playoff_multiplier. The algorithm
    is run with a population of pop_size and generations number of times.

    :param pop_size: int value representing how many entities are in a population.
    :param generations: int value representing how many times the genetic algorithm
                        will run.

    :return list: returns list of lists, representing the final population made
                  up of the entity and it's associated fitness value.
    """
    #generate initial population
    population = _initial_population(pop_size)
    #amount to prune pop_fitness by
    prune_idx = 2*math.floor(pop_size/3)
    #find fitness of initial population and prune
    pop_fitness = _population_fitnesses(population)[:prune_idx]

    #run main algorithm loop
    for gen in range(0, generations):
        _print_gen_stats(pop_fitness, gen)
        new_population = []
        #elitism, add previous generation's best fitness valued entity
        new_population.append(pop_fitness[0][0])

        #start at 1 bc elitism already adds first entity to new pop.
        for _ in range(1, pop_size):
            #genetic selection
            parent1 = pop_fitness[randint(0, prune_idx-1)][0]
            parent2 = pop_fitness[randint(0, prune_idx-1)][0]
            #reproduce and add to new population
            child = _reproduce(parent1, parent2)
            new_population.append(child)

        #update population to new children generated in function
        population = new_population
        #find fitness of new population and prune so that only 2/3 remain
        pop_fitness = _population_fitnesses(population)[:prune_idx]

    _print_gen_stats(pop_fitness, generations)
    return pop_fitness

def _print_gen_stats(population, generation):
    #get best entity and fitness for print statement
    best_fitness = population[0].copy()
    best_fitness[1] = round(best_fitness[1], 5)
    #get worst entity and fitness for print statement
    worst_fitness = population[-1].copy()
    worst_fitness[1] = round(worst_fitness[1], 5)
    if generation == 0:
        print(f'Initial Generation: Best: {best_fitness} Worst: {worst_fitness}')
    else:
        print(f'Generation {generation}: Best: {best_fitness} Worst: {worst_fitness}')

def _reproduce(parent1, parent2):
    """
    Simulates reproduction between 2 entities. Instead of selecting a crossover
    point as traditionally is done, generates random number to decide. Each
    parent has a 45% chance of having their gene selected while there's a 10%
    chance of the gene mutating. Returns a new entity.

    :param parent1: list containing weights used for an entity of the population.
    :param parent2: list containing weights used for an entity of the population.

    :returns child: list containing weights used for an entity of the population.
    """
    child = []
    for index, (gene1, gene2) in enumerate(zip(parent1, parent2)):
        prob = random()
        if prob <= .45:
            child.append(gene1)
        elif prob <= .9:
            child.append(gene2)
        else:
            child.append(_mutate(index))
    return child

def _mutate(index):
    """
    Simulates a 'mutated gene' by taking which gene is being mutated and generating
    a new random value for that gene.

    :param index: int representing which index gene of an entity is being mutated.

    :return int/float: returns an int if indes is for k-factor, rating-factor,
                       or homefield advantage, and a float for the others
                       representing a new mutated gene.
    """
    if index == 0:
        return _random_k()
    if index == 1:
        return _random_rf()
    if index == 2:
        return _random_hfa()
    if index == 3:
        return _random_scale()
    return _random_playoff_multiplier()

def _population_fitness(entity):
    """
    Calculates the fitness value for a single entity using an evaluation of
    how many games are predicted right that are in the dataset.

    :param entity: a single entity made up of values of:
                   [k-factor, rating-factor, home field advantage, seasonal scaling,
                   playoff multiplier].

    :return list: a list containing the entity and it's fitness value.
    """
    predictions = prediction_expanded_stats(entity[0], entity[1], entity[2],\
                                                       entity[3], entity[4])[0]
    return [entity, get_accuracy(predictions)]

def _population_fitnesses(pop):
    """
    Calculates the fitness values for every entity in a population using an
    evaluation of how many games are predicted right that are in the dataset.

    :param pop: a list of entities representing a population. Each entity is a
                list made up of values of:
                [k-factor, rating-factor, home field advantage, seasonal scaling,
                 playoff multiplier].

    :return list: returns sorted list of lists, the inner list being a single
                  entity and it's associated fitness value.
    """
    pop_fitness = []
    for entity in pop:
        #run against every game and get percentage of games predicted right
        predictions = prediction_expanded_stats(entity[0], entity[1], entity[2],\
                                               entity[3], entity[4])[0]
        pop_fitness.append([entity, get_accuracy(predictions)])

    #Sort all values according to their fitness value.
    #IMPORTANT: entities in population are pruned later for reproduction, so a
    #change in ordering will cause the algorithm to choose non-ideal candidates
    #for reproduction.

    return sorted(pop_fitness, key=lambda x:x[1], reverse=True)

def _initial_population(pop_size):
    """
    Initializes a population to be used in the genetic algorithm. The population
    is determined on the input size of randomly created entities and returned
    as a list.

    :param pop_size: an integer value representing how many entities are in a
                     population.

    :return list:    returns a list of entities as an initial population.
    """
    pop = []
    for _ in range(pop_size):
        pop.append(_create_single())
    return pop

def _create_single():
    """
    Creates a single entity for a population. Entity consists of random numbers
    for each gene and is returned as a list.

    :return list: returns a list of random number representing a single entity.
    """
    k = _random_k()
    rating_factor = _random_rf()
    hfa = _random_hfa()
    scale = _random_scale()
    playoff_multiplier = _random_playoff_multiplier()
    return [k, rating_factor, hfa, scale, playoff_multiplier]

def _random_k():
    """
    Generates a random number for the k-factor in the elo calculation between
    1 and 1000. K-factor is a boundry on the max amount an elo can change in 1
    game.

    NOTE: if zero, ratings won't change after games.

    :return int: returns an int between 1 and 1000.
    """
    return randint(1, 1000)

def _random_rf():
    """
    Generates a random number for the rating-factor in the elo calculation between
    50 and 1000. The rating factor determines how much elo it takes to increase
    the percent chance of a winner by a factor of 10.

    NOTE: if changed, factors of below 50 tend to make the function too
    exponential to run.

    :return int: returns an int between 50 and 1000.
    """
    return randint(50, 10000)

def _random_hfa():
    """
    Generates a random number between 0 and 500 for the home field advantage,
    which is a flat elo increase for the home team.

    :return int: returns an int between 0 and 500.
    """
    return randint(0, 500)

def _random_scale():
    """
    Generates a random number between 0 and 100 to scale the teams elo after
    each season. The number is divided by 100 to create and return a float.

    :return float: returns an float between 0 and 1.
    """
    return randint(0, 100)/100

def _random_playoff_multiplier():
    """
    Generates a random number between 1 and 200 to scale the elo changes
    that result from playoff games. The number is divided by 100 to create and
    return a float.

    :return float: returns an float greater than 0 and <= 2.
    """
    return randint(1, 200)/100
genetic_algorithm(10,2)
